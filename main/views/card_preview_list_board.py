import tkinter as tk
import tkinter.font as tkFont
from tkinter import ALL, EventType, PhotoImage, ttk

import bean.global_var as global_var
import services.CardService as cService
import tools.FileTool as ft
from enums.GwentEnum import *
from PIL import Image, ImageFont, ImageTk
from tools.decorators import *


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
        self.cardEffectHeight = round(self.CARD_IMG_EFFECT_SIZE[1] * self.imgEffectScale)
        self.darkCardEffectColor = (14, 10, 6, 180)
        # row_padding  图片高（50）+图片自身的一定比率 * 自适应压缩比率
        self.canvas_row_padding = round((self.CARD_IMG_SIZE[1]*1.08)*self.imgScale)
        # 存储当前行信息
        self.orig_rows_infos = []
        # 存储发现的卡牌，映射信息
        self.discoveryMap = {}
        # 为牌组模式服务,只进不出的数据,解决基于内存的牌组数据源可能会因为对方现冥、回响等因素导致牌组减少、不全的问题
        self.deck_module_all_deck = {}
        self.insIdMapImageId = {}
        self.onceExistInCarriedCards = {}
        # module
        self.MODULE_PAGE_MAX = 2
        self.MODULE_PAGE_MAX = 0
        self.MODULE_PAGE_NORMAL = 0
        self.modulePage = self.MODULE_PAGE_NORMAL
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
        
        # self.root.bind('<Key>', self.updateData)

        # self.show_data_frame()

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
                        if value["PlayId"] != hex(self.root.responseManager.playerId):
                            continue
                        if value["Location"] == hex(Location.GRAVEYARD.value):
                            ctIds.append(value["Id"])
                        if value["Location"] == hex(Location.DECK.value):
                            sortByIndexDict[int(value["Index"],16)] = key

                    deckNums = len(sortByIndexDict.keys())-1

                    count = 0
                     # 如果都是在墓地中出现的牌，说明发现action指向的是墓地，过滤这种情况
                    discoverCardsLen = len(cardsDict.keys())
                    temp_count = 0
                    for key,value in cardsDict.items():
                        if value["Id"] in ctIds:
                            temp_count += 1
                    if discoverCardsLen == temp_count:
                        return

                    for key,value in cardsDict.items():
                        # 过滤到敌方卡牌,规避discoverAction指向创造词条的情况
                        if int(value["PlayId"],16) == self.root.responseManager.battInfo.topPlayerId:
                            print("检索到卡:",value["Id"],value["Name"])
                            if deckNums-count >= 0:
                                temp_key = sortByIndexDict[deckNums-count]
                                self.discoveryMap[temp_key] = value
                                count += 1
    
    def getCIdsForDeckModule(self):
        pass
        # self.isMain_update_deck_sort()
    
    def discoverCardMapCurrDeckData(self):
        for key,value in self.discoveryMap.items():
            if key in  self.curr_memo_cards.keys():
                cardUIData = global_var.get_value("AllCardDict")[str(value["Id"])]
                self.curr_memo_cards[key]["Id"] = value["Id"]
                self.curr_memo_cards[key]["Provision"] = cardUIData["provision"]
                self.curr_memo_cards[key]["Rarity"] = cardUIData["rarity"]
                self.curr_memo_cards[key]["FactionId"] = cardUIData["factionId"]
                self.curr_memo_cards[key]["Type"] = cardUIData["cardType"]
                self.curr_memo_cards[key]["Name"] = cardUIData["name"]
                self.curr_memo_cards[key]["BasePower"]  = cardUIData["power"] 

    def updateData(self):
        # print("日")
        origCardsInfo = {} 
        self.curr_memo_cards = cService.getMemoryCards()
        # 映射-发现池
        if self.CARD_DECK_INFO.isEnemy:
            self.fillDiscoveredCardOfBottomPlayerViewingAction()
            self.discoverCardMapCurrDeckData()

        self.battleCards = cService.filterCardsByDeckCondition(self.curr_memo_cards,self.CARD_DECK_INFO)

        self.carriedCards = {}
        self.carriedCards.update(self.onceExistInCarriedCards)
        self.carriedCards.update(self.curr_memo_cards)
        self.carriedCards = cService.filterCardsIntoCarriedCards(self.carriedCards,self.CARD_DECK_INFO)
        # 映射曾经存在于carriedCards中的卡牌数据
        self.carriedCards = cService.sort_cardTemplate_by_provision(self.carriedCards)
        self.carriedCards = cService.addStratagemCard(self.carriedCards,self.curr_memo_cards,self.root.responseManager.playerId)
        self.onceExistInCarriedCards = self.carriedCards

        self.currDeckData = {}
        if not self.CARD_DECK_INFO.isMain:
            self.cardsSource = self.battleCards
            for key,value in self.cardsSource.items():
                temp_dict = {}
                # temp_dict["insId"] = key
                temp_dict["ctId"] = value["Id"]
                temp_dict["isNotExist"] = False
                self.currDeckData[key] = temp_dict
        if self.CARD_DECK_INFO.isMain:
            self.cardsSource = self.carriedCards
            for key,value in self.cardsSource.items():
                temp_dict = {}
                location = self.curr_memo_cards[key]["Location"] 
                temp_dict["ctId"] = value["Id"]
                temp_dict["isNotExist"] = False
                if location != hex(Location.DECK.value) and location != hex(Location.HAND.value) and location != hex(Location.LEADER.value):
                    temp_dict["isNotExist"] = True
                self.currDeckData[key] = temp_dict

        
        # 初始化图片，以及建立映射源
        self.initImgPool(self.currDeckData,self.imgScale)
        # 映射imageId到更新数据
        for key_insId,value in self.currDeckData.items():
            value["imageId"] = self.insIdMapImageId[key_insId]
        # UI
        self.updateCardUI(self.currDeckData)
        self.updateCardExistEffectUI(self.currDeckData)
        self.setDeckStatus(self.currDeckData)
        self.after(400,self.updateData)

    # 设置卡组状态组[卡牌总数,单位数量,粮食]
    def setDeckStatus(self,currDeckData):
        total = 0
        unit = 0
        provision = 0
        cards = currDeckData
        for key,value in cards.items():
            currCardBaseData = self.curr_memo_cards[key]
            if value["isNotExist"]:
                continue
            temp_prov = currCardBaseData["Provision"]
            if CardType(currCardBaseData["Type"]) != CardType.LEADER:
                provision += temp_prov
                if CardType(currCardBaseData["Type"]) != CardType.STRATAGEM:
                    total += 1
            cardType = currCardBaseData["Type"]
            if cardType == CardType.UNIT.value :
                unit += 1
        self.root.responseManager.updateStatusBoard(total,unit,provision)
        

    def updateCardUI(self,deckData):
        uiCards = self.can_bg.find_withtag("UICard")
        for imageId in uiCards:
            self.can_bg.itemconfig(imageId, state = "hidden")
        count  = 0
        yOffset = 0
        for key,value in deckData.items():
            iId = key
            self.can_bg.itemconfig(value["imageId"], state = "normal")
            if len(self.can_bg.find_withtag(str(iId)+"hiddenCard")) > 0:
                row = self.can_bg.find_withtag(str(iId)+"hiddenCard")[0]
                self.can_bg.moveto(row,x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
            self.can_bg.moveto(value["imageId"],x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
            count += 1
            # 排除衍生物没有cardType
            cardInfo = self.curr_memo_cards[key]
            if CardType(cardInfo["Type"]) == CardType.LEADER:
                yOffset += 50
            elif CardType(cardInfo["Type"]) == CardType.STRATAGEM:
                yOffset += 7
    
    # 改为池创建
    def updateCardExistEffectUI(self,deckData):
        count  = 0
        yOffset = 0
        for key,value in deckData.items():
            iId = key
            if len(self.can_bg.find_withtag(str(iId)+"hiddenCard")) == 0:
                imgTk = ft.getDarkCardPreviewImgTk((self.cardImgWidth,self.cardEffectHeight),self.darkCardEffectColor)
                self.panel = tk.Label(master = self.root)
                self.panel.temp_img = imgTk
                self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*count+yOffset,
                anchor='nw',image=self.panel.temp_img, tags = (str(key)+"hiddenCard"),state="hidden")

            temp_list = self.can_bg.find_withtag(str(key)+"hiddenCard")
            if value["isNotExist"]:
                self.can_bg.itemconfig(temp_list[0], state = "normal")
            else:
                self.can_bg.itemconfig(temp_list[0], state = "hidden")

            cardInfo = self.curr_memo_cards[key]
            if CardType(cardInfo["Type"]) == CardType.LEADER:
                yOffset += 50
            elif CardType(cardInfo["Type"]) == CardType.STRATAGEM:
                yOffset += 7
            count+=1

    def initImgPool(self,data,scale_factor):
        for key_insId,value in data.items():
            s_insId = str(key_insId)
            s_ctId = str(value["ctId"])
            if int(s_ctId) != 0:
                cardUIData = global_var.get_value("AllCardDict")[s_ctId]
                cardData = {}
                cardData["Name"] = cardUIData["name"]
                cardData["Id"] = int(s_ctId)
                try:
                    cardData["Provision"] = cardUIData["provision"]
                    cardData["Type"] = cardUIData["cardType"]
                    cardData["Rarity"] = cardUIData["rarity"]
                    cardData["CurrPower"] = cardUIData["power"]
                    cardData["FactionId"] = cardUIData["factionId"]
                except KeyError:
                    cardData["Provision"] = self.curr_memo_cards[int(s_insId)]["Provision"]
                    cardData["Type"] = self.curr_memo_cards[int(s_insId)]["Type"]
                    cardData["Rarity"] = self.curr_memo_cards[int(s_insId)]["Rarity"]
                    cardData["CurrPower"] = self.curr_memo_cards[int(s_insId)]["BasePower"]
                    cardData["FactionId"] = self.curr_memo_cards[int(s_insId)]["FactionId"]
            else:
                cardData = {}
                cardData["Name"] = "未知"
                cardData["Id"] = 0
                cardData["Provision"] = self.curr_memo_cards[int(s_insId)]["Provision"]
                cardData["Type"] = self.curr_memo_cards[int(s_insId)]["Type"]
                cardData["Rarity"] = self.curr_memo_cards[int(s_insId)]["Rarity"]
                cardData["CurrPower"] = self.curr_memo_cards[int(s_insId)]["BasePower"]
                cardData["FactionId"] = self.curr_memo_cards[int(s_insId)]["FactionId"]

            if len(self.can_bg.find_withtag(s_insId+"InsId")) == 0:
                # 不存在池中则实例化一个进入池
                imgTk = ft.get_deck_preview_img(cardData,scale_factor)
                self.panel = tk.Label(master = self.root)
                self.panel.temp_img = imgTk
                imagId = self.can_bg.create_image(0,0,anchor='nw',image=self.panel.temp_img, 
                tags = (s_insId+"InsId","{0}-{1}ctId".format(s_insId,s_ctId),"UICard"),state = "hidden")
                self.insIdMapImageId[key_insId] = imagId
            if value["ctId"] == 0:
                # 未知卡，此时该卡需要更新
                pass
            else:
                insIds = self.can_bg.find_withtag("{0}InsId".format(s_insId)) 
                ctIdTags  = self.can_bg.find_withtag("{0}-{1}ctId".format(s_insId,s_ctId))
                # 还未从【未知】生成新的
                if len(ctIdTags) == 0 and len(insIds)!=0:
                    imgTk = ft.get_deck_preview_img(cardData,scale_factor)
                    self.panel = tk.Label(master = self.root)
                    self.panel.temp_img = imgTk
                    imageIds = insIds
                    if len(imageIds) != 0:
                        self.can_bg.itemconfig(imageIds[0],image=self.panel.temp_img,tags =(s_insId+"InsId","{0}-{1}ctId".format(s_insId,s_ctId),"UICard"))
                        self.discoveryMap[int(s_insId)] = cardData

    def ScrollEvent(self,event):
        MOVE_DELTA = 32
        yOffset = 0
        if self.CARD_DECK_INFO.isMain:
            yOffset = 4
        total = 0
        cards = self.currDeckData
        # cards = self.curr_memo_cards
        for key,value in cards.items():
            location = self.curr_memo_cards[key]["Location"]
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
                # self.isMain_update_deck_sort() if self.CARD_DECK_INFO.isMain else self.update_deck_sort()
                self.updateCardUI(self.currDeckData)
        else:
            # M-down
            if self.canvas_padding[1] > int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset)):
                rate = self.canvas_padding[1]/int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset))
                elasticityFactor = 1
                if rate > 0 and rate < 1: 
                    elasticityFactor = 1-rate
                self.canvas_padding[1] -= MOVE_DELTA * elasticityFactor
                # self.isMain_update_deck_sort() if self.CARD_DECK_INFO.isMain else self.update_deck_sort()
                self.updateCardUI(self.currDeckData)
        self.canvas_padding[1] = int(self.canvas_padding[1])
    
    def clear_deck_img(self):
        for img_id in self.can_bg.find_all():
            self.can_bg.delete(img_id)

    def resetType(self,CardDeckInfo):
        self.CARD_DECK_INFO = CardDeckInfo
        self.orig_rows_infos.clear()
        self.curr_memo_cards.clear()
        self.clear_deck_img()

        # 重置因为滚轮事件导致的img偏移
        self.canvas_padding[1] = 0
    
    def setCardDeckInfo(self,CardDeckInfo):
        self.CARD_DECK_INFO = CardDeckInfo
# ----------------------------------------------------------------
# 相关:【推荐卡组】
    def setShowRelateDeck(self):
        # BUG 不做分离的话，如果没有进入卡组模式，会缺少deck_module的数据...
        # TODO 卡组数据函数分离
        # 获取卡组数据
        # 分析卡组数据，提交数据
        # 获取数据库返回的数据 cts
        # 根据整理好的cts显示卡牌
        # 更新状态和临时数据存储
        playerDeckCtIds = []
        leaderCard = 0
        stratagemCard = 0
        allCardDict = global_var.get_value("AllCardDict")
        decks = global_var.get_value("decks")
        leaderCardDict = global_var.get_value("LeaderCardDict")
        for key,value in self.deck_module_all_deck.items():
            if value["type"] == CardType.LEADER.value:
                print(leaderCardDict[value["templateId"]]["factionId"])
            if value["type"] == CardType.STRATAGEM.value:
                pass
            playerDeckCtIds.append(value["templateId"])
####################################################################################################################
####################################################################################################################