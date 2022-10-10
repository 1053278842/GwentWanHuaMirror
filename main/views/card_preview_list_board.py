from itertools import count
import tkinter as tk
from tkinter import ttk, ALL, EventType
import tools.FileTool as ft
from tools.decorators import *
import services.GwentService as service
import services.CardService as cService
from enums.GwentEnum import *
from tkinter import PhotoImage
from PIL import Image, ImageTk, ImageFont
import copy
import tkinter.font as tkFont

## 图片列表卡组
class card_preview_list_board(tk.Frame):

    def __init__(self, root):
        super().__init__(master = root)
        self.root = root

        self.CARD_IMG_SIZE = (400,50)
        self.CARD_IMG_EFFECT_SIZE = (291,38)

        # label list padding
        # TODO RESIZE 20和高度关联
        self.canvas_padding = [int(self.root.WIN_WIDTH*0.07),20]
        
        # img scale  指定宽度/图片宽度 400
        self.cardImgWidth = self.root.WIN_WIDTH-self.canvas_padding[0]*2
        self.imgScale = (self.cardImgWidth) / self.CARD_IMG_SIZE[0]
        self.imgEffectScale = (self.cardImgWidth) / self.CARD_IMG_EFFECT_SIZE[0]
        # row_padding  图片高（50）+图片自身的一定比率 * 自适应压缩比率
        self.canvas_row_padding = round((self.CARD_IMG_SIZE[1]*1.08)*self.imgScale)
        # 存储当前行信息
        self.orig_rows_infos = []
        # 存储发现的卡牌，映射信息
        self.discoveryMap = {}
        # 为牌组模式服务,只进不出的数据,解决基于内存的牌组数据源可能会因为对方现冥、回响等因素导致牌组减少、不全的问题
        self.deck_module_all_deck = {}
        # 显示类型
        self.CARD_DECK_INFO = self.root.responseManager.DEFAULT_CARD_DECK_INFO

        self.can_size = [self.root.WIN_WIDTH,self.root.MID_HEIGHT + (self.root.TOP_HEIGHT+self.root.MID_HEIGHT+self.root.BOTTOM_HEIGHT)*0.04]


        self.create_page()
    
    def getHeight(self):
        return self.can_size[1]     

    def create_page(self):
        self.can_bg = tk.Canvas(self,bg='#000000',width = self.can_size[0], height = self.can_size[1] ,highlightthickness=0,highlightcolor="green")
        self.can_bg.pack()
        # 绑定事件
        self.can_bg.bind('<MouseWheel>',self.ScrollEvent)

        # self.show_data_frame()

    # 设置卡组状态组[卡牌总数,单位数量,粮食]
    def set_deck_status(self):
        total = 0
        unit = 0
        provision = 0
        cards = self.curr_memo_cards
        for iId in cards:
            location = cards[iId]["Location"]
            if location == hex(self.CARD_DECK_INFO.location.value) or location == hex(self.CARD_DECK_INFO.secLocation.value) or self.CARD_DECK_INFO.isMain:
                total += 1
                temp_prov = cards[iId]["Provision"]
                provision += temp_prov
                cardType = cards[iId]["Type"]
                if cardType == CardType.UNIT.value :
                    unit += 1
        self.root.responseManager.updateStatusBoard(total,unit,provision)

    def delay_delete_data(self,delete_row_info,row_info_dict):
        if len(self.can_bg.find_withtag(str(row_info_dict["row"])+"effect_tips")) == 0:
            if delete_row_info in self.orig_rows_infos:
                self.orig_rows_infos.remove(delete_row_info)
                self.can_bg.itemconfig(row_info_dict["row"],state="hidden")

     
    def remove_component(self,remove_card_id_list):
        will_delete_row_infos = []
        for row_info in self.orig_rows_infos:
            instanceId = row_info["instanceId"]
            if instanceId in remove_card_id_list:
                will_delete_row_infos.append(row_info)
        # 不影响遍历的情况下删除
        for delete_row_info in will_delete_row_infos:
            anim_time = 1000
            if len(self.can_bg.find_withtag(str(delete_row_info["row"])+"effect_tips")) == 0:
                row        = delete_row_info["row"]
                instanceId = delete_row_info["instanceId"]
                self.can_bg.after(anim_time,self.delay_delete_data,delete_row_info,delete_row_info)
                # print("删除行:",row,self.curr_memo_cards[instanceId]["Name"],delete_row_info)
                # 隐藏行
                
                self.remove_tips_item(row,anim_time)

    def add_component(self,add_card_id_list):
        for iId in add_card_id_list:
            template_id = self.curr_memo_cards[iId]["Id"]
            card_index = int(self.curr_memo_cards[iId]["Index"],16)
            array_index = add_card_id_list.index(iId)
            tagName = str(iId) + "card"
            temp_list = self.can_bg.find_withtag(tagName)
            if len(temp_list) == 0:
                print("【ERROR ERROR ERROR ERROR】 add 失败!")
                return 0
            row = temp_list[0]
            # 激活
            self.can_bg.itemconfig(row, state = "normal")
            self.can_bg.moveto(row,self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*array_index)
            # 数据存储更新..
            temp_row_dict = {"row":row,"instanceId":iId,"templateId":template_id,"isFlashing":False,"rowId":row}
            self.orig_rows_infos.insert(array_index,temp_row_dict)
            # print("添加行:",array_index,self.curr_memo_cards[iId]["Name"],temp_row_dict,self.curr_memo_cards[iId]["Location"])
            self.add_tips_item(row)

    def get_orig_deck_iIds(self):
        temp_list = []
        for row_info in self.orig_rows_infos:
            temp_list.append(row_info["instanceId"])
        return temp_list

     
    def init_img_pool(self,curr_memo_cards,scale_factor):
        for key in curr_memo_cards:
            curr_card = curr_memo_cards[key]
            if len(self.can_bg.find_withtag(str(key)+"card")) == 0:
                # 不存在池中则实例化一个进入池
                imgTk = ft.get_deck_preview_img(curr_card,scale_factor)
                self.panel = tk.Label(master = self.root)
                self.panel.temp_img = imgTk
                self.can_bg.create_image(0,0,anchor='nw',image=self.panel.temp_img, 
                tags = (str(key)+"card","{0}-{1}ctId".format(str(key),str(curr_card["Id"]))),state = "hidden")

            if curr_card["Id"] == 0:
                # 未知卡，此时该卡需要更新
                pass
            else:
                insIds = self.can_bg.find_withtag("{0}card".format(str(key))) 
                ctIdTags  = self.can_bg.find_withtag("{0}-{1}ctId".format(str(key),str(curr_card["Id"])))
                # 还未从【未知】生成新的
                if len(ctIdTags) == 0 and len(insIds)!=0:
                    imgTk = ft.get_deck_preview_img(curr_card,scale_factor)
                    self.panel = tk.Label(master = self.root)
                    self.panel.temp_img = imgTk
                    imageIds = insIds
                    if len(imageIds) != 0:
                        self.can_bg.itemconfig(imageIds[0],image=self.panel.temp_img,tags =(str(key)+"card","{0}-{1}ctId".format(str(key),str(curr_card["Id"]))))
                        self.discoveryMap[key] = curr_card

    def fillDiscoveredCardOfBottomPlayerViewingAction(self):
        # 捕获用户操作想吃什么？
        statusCode = self.root.responseManager.getPlayerActionsCode()
        if statusCode != 0:
            # check检视动作
            MAX_STATUS_CODE = int(0x100)
            MIN_STATUS_CODE = int(0x80)
            if statusCode < MAX_STATUS_CODE and statusCode >= MIN_STATUS_CODE:
                # 获取检视敌方的卡牌list
                cardsDict = cService.getViewingCards()

                if len(cardsDict.keys()) > 0:
                    ctIds = []
                    sortByIndexDict = {}
                    for key,value in self.curr_memo_cards.items():
                        if value["Location"] == hex(Location.GRAVEYARD.value):
                            ctIds.append(value["Id"])
                        if value["Location"] == hex(Location.DECK.value):
                            sortByIndexDict[int(value["Index"],16)] = key

                    deckNums = len(sortByIndexDict.keys())-1

                    count = 0
                    for key,value in cardsDict.items():
                        # 过滤到敌方卡牌
                        if int(value["PlayId"],16) == self.root.responseManager.battInfo.topPlayerId:
                            # 和墓地卡、放逐池、场上卡进行cardTemplateId比对。
                            # 不在其内的过滤出来，即为对方卡组的卡
                            if value["Id"] in ctIds:
                                print("发现中已存在：",key,value["Id"],value["Name"])
                                continue
                            print("检索到卡:",value["Id"],value["Name"])
                            if deckNums-count >= 0:
                                temp_key = sortByIndexDict[deckNums-count]
                                self.discoveryMap[temp_key] = value
                                count += 1
        
        for key,value in self.discoveryMap.items():
            if key in  self.curr_memo_cards.keys():
                curr_value = self.curr_memo_cards[key]
                value["Location"] = curr_value["Location"]
                value["Index"]  = curr_value["Index"]
                value["CurrPower"]  = curr_value["CurrPower"]
                value["BasePower"]  = curr_value["BasePower"]
                self.curr_memo_cards[key] = value
        
    def show_data_frame(self):
        if self.CARD_DECK_INFO.isMain:
            self.show_main_deck()
            return 0 

        scale_factor = self.imgScale
        # print(scale_factor)
        # 分别获取当前软件中row的instanceId集，以及游戏内存中的instanceId
        curr_deck_iIds = self.get_orig_deck_iIds()
        self.curr_memo_cards = service.get_my_all_cards(self.CARD_DECK_INFO)
        # 从这开始
        self.fillDiscoveredCardOfBottomPlayerViewingAction()
        self.init_img_pool(self.curr_memo_cards,scale_factor)
        # 过滤出需要增加或删除的数据 instanceId
        remove_card_id_list  = service.get_deck_remove_cards(self.curr_memo_cards,curr_deck_iIds,self.CARD_DECK_INFO)
        add_card_id_list     = service.get_deck_add_cards(self.curr_memo_cards,curr_deck_iIds,self.CARD_DECK_INFO)        
        if len(remove_card_id_list) == 0 and len(add_card_id_list) == len(remove_card_id_list) and not self.CARD_DECK_INFO.isMain:
            self.move_component()
        else:
            # 更新卡组状态
            self.set_deck_status()
        # 删除多余的图片
        self.remove_component(remove_card_id_list)
        # 增加新加入的图片
        self.add_component(add_card_id_list)
        # 获取需要移动位置的图片
        self.update_deck_sort()
        # 循环收集curr_memo_cards并00
        # 处理add和remove
       
        self.after(400,self.show_data_frame)
    
    def show_main_deck(self):
        if not self.CARD_DECK_INFO.isMain:
            for row_info in self.main_deck_row_infos:
                self.can_bg.itemconfig(row_info["row"], state = "hidden")
            self.show_data_frame()
            return 0 
        # 从这开始
        scale_factor = self.imgScale
        # 分别获取当前软件中row的instanceId集，以及游戏内存中的instanceId
        self.main_deck_row_infos = []
        self.curr_memo_cards = service.get_my_all_cards(self.CARD_DECK_INFO)
        self.fillDiscoveredCardOfBottomPlayerViewingAction()
        self.init_img_pool(self.curr_memo_cards,scale_factor)

        # 映射补全在牌组模式下出现的卡牌
        for key,value in self.deck_module_all_deck.items():
            if key in self.curr_memo_cards.keys():
                value["Location"] = self.curr_memo_cards[key]["Location"]
                value["Index"]  = self.curr_memo_cards[key]["Index"]
                value["CurrPower"]  = self.curr_memo_cards[key]["CurrPower"]
                value["BasePower"]  = self.curr_memo_cards[key]["BasePower"]
                self.curr_memo_cards[key] = value
        temp_sort_list = sorted(self.curr_memo_cards.items(),key=lambda x: (-x[1]["Provision"],x[1]["Id"]))
        self.curr_memo_cards.clear()
        for i in temp_sort_list:
            self.curr_memo_cards[i[0]] = i[1]

        index = 0
        for iId in self.curr_memo_cards:
            # TODO BUG 策略卡的变形无法记录！！比如瓶中灵策略卡会直接变身为瓶中灵
            # 过滤开局后产生的卡
            temp_dict = self.curr_memo_cards[iId]
            if iId > self.root.responseManager.maxCardNums or iId < self.root.responseManager.minCardNums:
                continue
            # if temp_dict["FromPlayerId"] == self.root.responseManager.enemyPlayerId:
            #     # 特例法典，会改变自身的playerId
            #     if temp_dict["Id"] != 203103:
            #         continue
            if temp_dict["Id"] == 0:
                continue
            self.deck_module_all_deck[iId] = temp_dict
            template_id = temp_dict["Id"]
            temp_location = temp_dict["Location"]
            # 甄别已经打出的卡
            temp_isExist = True
            self.curr_memo_cards[iId]["temp_isExist"] = True
            if temp_location != hex(Location.DECK.value) and temp_location != hex(Location.HAND.value) and temp_location != hex(Location.LEADER.value):
                temp_isExist = False
                self.curr_memo_cards[iId]["temp_isExist"] = False
            card_type = temp_dict["Type"]
            tagName = str(iId) + "card"
            temp_list = self.can_bg.find_withtag(tagName)
            if len(temp_list) > 0:
                row = temp_list[0]
            else:
                continue
            temp_row_dict = {"row":row,"instanceId":iId,"templateId":template_id,"isFlashing":False,"type":card_type,"isExist":temp_isExist}

            self.main_deck_row_infos.insert(index,temp_row_dict)
            index += 1

        # 优化策略卡的位置
        for row in self.main_deck_row_infos:
            if row["type"] == CardType.STRATAGEM.value:
                stratagem_row_info = row
                stratagem_row_info["isExist"]=True
                self.main_deck_row_infos.remove(row)
                self.main_deck_row_infos.insert(1,stratagem_row_info)
            if row["type"] == CardType.LEADER.value:
                leader_row_info = row
                leader_row_info["isExist"]=True
                self.main_deck_row_infos.remove(row)
                self.main_deck_row_infos.insert(0,leader_row_info)
        # 显示
        self.isMain_update_deck_sort()

        # 更新状态
        total = 0
        unit = 0
        provision = 0
        # 这里的main_deck_row_infos已经被过滤过，就是最终显示的列表数据源
        for row_info in self.main_deck_row_infos:
            if not self.CARD_DECK_INFO.isEnemy:
                if not row_info["isExist"]:
                    continue
            if row_info["type"] != CardType.LEADER.value:
                temp_prov = self.curr_memo_cards[row_info["instanceId"]]["Provision"]
                provision += temp_prov
                if row_info["type"] != CardType.LEADER.value and row_info["type"] != CardType.STRATAGEM.value:
                    total += 1
            cardType = self.curr_memo_cards[row_info["instanceId"]]["Type"]
            if cardType == CardType.UNIT.value :
                unit += 1
        self.root.responseManager.updateStatusBoard(total,unit,provision)
        self.after(400,self.show_main_deck)

    def isMain_update_deck_sort(self):
        count  = 0
        yOffset = 0
        for row_info in self.main_deck_row_infos:
            self.can_bg.itemconfig(row_info["row"], state = "normal")
            if not row_info["isExist"]:
                temp_list = self.can_bg.find_withtag(str(row_info["instanceId"])+"hiddenCard")
                if len(temp_list) < 1:
                    img = Image.new("RGBA", (290,37),(14, 10, 6, 180))
                    imgTk = ImageTk.PhotoImage(img)
                    self.panel = tk.Label(master = self.root)
                    self.panel.temp_img = imgTk
                    self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*count+yOffset,
                    anchor='nw',image=self.panel.temp_img, tags = (str(row_info["instanceId"])+"hiddenCard"))
            else:
                temp_list = self.can_bg.find_withtag(str(row_info["instanceId"])+"hiddenCard")
                if len(temp_list) >0:
                    self.can_bg.delete(temp_list[0])

            iId = row_info["instanceId"]
            if len(self.can_bg.find_withtag(str(iId)+"hiddenCard")) > 0:
                row = self.can_bg.find_withtag(str(iId)+"hiddenCard")[0]
                self.can_bg.moveto(row,x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
            self.can_bg.moveto(row_info["row"],x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)

            # 特殊格式
            if row_info["type"] == CardType.LEADER.value:
                yOffset += 50
            if row_info["type"] == CardType.STRATAGEM.value:
                yOffset += 7

            count += 1

    def ScrollEvent(self,event):
        MOVE_DELTA = 32
        yOffset = 0
        if self.CARD_DECK_INFO.isMain:
            yOffset = 4
        total = 0
        cards = self.curr_memo_cards
        for iId in cards:
            location = cards[iId]["Location"]
            if location == hex(self.CARD_DECK_INFO.location.value) or location == hex(self.CARD_DECK_INFO.secLocation.value) or self.CARD_DECK_INFO.isMain:
                total += 1
        maxNum = int(self.can_size[1]/self.canvas_row_padding)
        if event.delta > 0 :
            # M-up
            if self.canvas_padding[1] < int((1.5) * self.canvas_row_padding):
                rate = self.canvas_padding[1]/int((1.5) * self.canvas_row_padding)
                elasticityFactor = 1
                if rate > 0 and rate < 1: 
                    elasticityFactor = 1-rate
                self.canvas_padding[1] += MOVE_DELTA*elasticityFactor
                self.isMain_update_deck_sort() if self.CARD_DECK_INFO.isMain else self.update_deck_sort()
        else:
            # M-down
            if self.canvas_padding[1] > int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset)):
                rate = self.canvas_padding[1]/int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset))
                elasticityFactor = 1
                if rate > 0 and rate < 1: 
                    elasticityFactor = 1-rate
                self.canvas_padding[1] -= MOVE_DELTA * elasticityFactor
                self.isMain_update_deck_sort() if self.CARD_DECK_INFO.isMain else self.update_deck_sort()
        self.canvas_padding[1] = int(self.canvas_padding[1])
    

    def move_component(self):
        original_iId_list = self.get_orig_deck_iIds()
        new_iId_list = []
        for card_instance_id in self.curr_memo_cards:
            if (self.curr_memo_cards[card_instance_id]["Location"] == hex(self.CARD_DECK_INFO.location.value) or
             self.curr_memo_cards[card_instance_id]["Location"] == hex(self.CARD_DECK_INFO.secLocation.value)):
                new_iId_list.append(int(card_instance_id))

        is_reload_param = False
        for i in range(0,len(original_iId_list)):
            if original_iId_list[i] != new_iId_list[i]:
                is_reload_param = True
                print("重置触发条件")

        if not is_reload_param:
            return 0
        print("重设！","new:",len(new_iId_list),"orig:",len(self.orig_rows_infos))
        self.reorder_data_and_anim(new_iId_list)

    def reorder_data_and_anim(self,new_iId_list):
        orig_list = copy.copy(self.orig_rows_infos)
        temp_list = []
        for new_iId in new_iId_list:
            # 顺带执行动画
            for orig_row_info in self.orig_rows_infos:
                if orig_row_info["instanceId"] == new_iId:
                    temp_list.append(orig_row_info)
                    self.orig_rows_infos.remove(orig_row_info)
                    break
        self.orig_rows_infos = temp_list

        new_list = copy.copy(self.orig_rows_infos)
        moved_row_id = self.get_moved_row(orig_list,new_list)
        self.anim_img_tips(moved_row_id,TipsType.WHITE)

        # 更新卡组状态
        self.set_deck_status()

    def get_moved_row(self,orig_list,new_list):
        moved_row_id = 0
        for i in range(0,len(orig_list)):
            if i+1 < len(orig_list):
                if orig_list[i+1]["row"] == new_list[i]["row"]:
                    moved_row_id = orig_list[i]["row"]
                    break
                else:
                    moved_row_id = new_list[i]["row"]
                    break
        return moved_row_id
    

    def add_tips_item(self,row):
        self.anim_img_tips(row,TipsType.ADD)

    def remove_tips_item(self,row,anim_time):
        self.anim_img_tips(row,TipsType.REMOVE,anim_time)


    def anim_img_tips(self,row,tipsType,anim_time=2500):
        count = 0
        iId = 0
        for row_info in self.orig_rows_infos:
            if row_info["row"] == row:
                iId = row_info["instanceId"]
                break
            count += 1
        if tipsType == TipsType.ADD:
            path = r"main/resources/images/deck_preview/BLUE_FRAME.png"
        elif tipsType == TipsType.REMOVE:
            path = r"main/resources/images/deck_preview/PURPLE_FRAME.png"
        elif tipsType == TipsType.MOVE:
            path = r"main/resources/images/deck_preview/BLUE_FRAME.png"
        elif tipsType == TipsType.WHITE:
            path = r"main/resources/images/deck_preview/WHITE_FRAME.png"
       
        imgTk = ft.get_img_resized(path,self.imgEffectScale)
        self.panel = tk.Label(master = self.root)
        self.panel.temp_img = imgTk
        row_id = self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*count,
        anchor='nw',image=self.panel.temp_img,tags = (str(iId)+"effect_tips","effect_tips"))
        self.root.after(anim_time,self.anim_img_tips_hidden,row_id)
        
    def anim_img_tips_hidden(self,img_id):
        self.can_bg.delete(img_id)

     
    def update_deck_sort(self):
        count  = 0
        for row_info in self.orig_rows_infos:
            iId = row_info["instanceId"]
            if len(self.can_bg.find_withtag(str(iId)+"effect_tips")) > 0:
                row = self.can_bg.find_withtag(str(iId)+"effect_tips")[0]
                self.can_bg.moveto(row,x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count)
            self.can_bg.moveto(row_info["row"],x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count)
            count += 1

    def clear_deck_img(self):
        for img_id in self.can_bg.find_all():
            self.can_bg.delete(img_id)

    # @moved_element: 要移动的row对象中card的instanceId
    # @moved_to_index: 要移动到的新下标位置      
    # @row_dict: 行信息字典，包含row对象id,template_id,instanceId，Name       
    def anim_move_one_row(self,moved_element,moved_to_index):
        orig_index = 0
        orig_row = 0
        for row_dict in self.orig_rows_infos:
            if row_dict["instanceId"] == moved_element:
                orig_index = self.orig_rows_infos.index(row_dict)
                orig_row = row_dict["row"]
                break
        # 目标row移至下标处
        times = moved_to_index-orig_index
        self.can_bg.move(orig_row,0,self.canvas_row_padding * times)

    def resetType(self,CardDeckInfo):
        self.CARD_DECK_INFO = CardDeckInfo
        self.orig_rows_infos.clear()
        self.curr_memo_cards.clear()
        self.clear_deck_img()

        # 重置因为滚轮事件导致的img偏移
        self.canvas_padding[1] = 0
    
    def setCardDeckInfo(self,CardDeckInfo):
        self.CARD_DECK_INFO = CardDeckInfo
####################################################################################################################
####################################################################################################################