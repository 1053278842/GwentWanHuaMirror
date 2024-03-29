import datetime
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ALL, EventType, PhotoImage, ttk

import bean.global_var as global_var
import services.CardService as cService
import tools.FileTool as ft
from enums.GwentEnum import *
from PIL import Image, ImageFont, ImageTk
from tools.decorators import *
from views.list_board.DeckTips import *


## 图片列表卡组
class card_preview_list_board(tk.Frame):
    
    def __init__(self, root):
        super().__init__(master = root)
        self.root = root

        self.CARD_IMG_SIZE = (400,50)
        self.CARD_IMG_EFFECT_SIZE = (291,38)

        # label list padding
        self.canvas_padding = [int(self.root.WIN_WIDTH*0.07),round(self.root.WIN_WIDTH*20/338)]
        
        # img scale  指定宽度/图片宽度 400
        self.cardImgWidth = self.root.WIN_WIDTH-self.canvas_padding[0]*2
        self.imgScale = (self.cardImgWidth) / self.CARD_IMG_SIZE[0]
        self.imgEffectScale = (self.cardImgWidth) / self.CARD_IMG_EFFECT_SIZE[0]
        self.cardEffectHeight = round(self.CARD_IMG_EFFECT_SIZE[1] * self.imgEffectScale)
        self.darkCardEffectColor = (14, 10, 6, 150)
        self.excessCardEffectColor = (32, 0, 6, 180)
        # row_padding  图片高（50）+图片自身的一定比率 * 自适应压缩比率
        self.canvas_row_padding = round((self.CARD_IMG_SIZE[1]*1.08)*self.imgScale)
        # 存储当前行信息
        self.currDeckData={}
        # 存储发现的卡牌，映射信息
        self.discoveryMap = {}
        # 为牌组模式服务,只进不出的数据,解决基于内存的牌组数据源可能会因为对方现冥、回响等因素导致牌组减少、不全的问题
        self.deck_module_all_deck = {}
        self.insIdMapImageId = {}
        self.onceExistInCarriedCards = {}
        # module
        self.MODULE_PAGE_MAX = 5
        self.MODULE_PAGE_MIN = 0
        self.MODULE_PAGE_NORMAL = 0
        self.modulePage = self.MODULE_PAGE_NORMAL
        self.isShowRelationDeck = False
        # self.root.responseManager.title.disableArrows()
        # self.root.responseManager.title.showOneArrow(True)
        # 当前预测卡组
        self.forecastDeck = {}
        self.forecastDeck["deckName"] = ""
        self.forecastDeck["deckAuthor"] = ""
        self.forecastDeck["differenceDays"] = 0
        self.forecastDeck["repeatRate"] = 0
        self.forecastDeck["sortedCards"] = {}
        # 预测卡组-禁识之瓶启封的映射
        self.specialMapJSZPQF = {}
        # 预测卡组的自动刷新依据：carried的len
        self.carriedLazyLen = 0
        # 高级设置
        global_config = ft.getGlobalConfig()
        self.comparativeForecast = global_config['comparative']
        self.sortingRealLibrary = global_config['sorting']
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
        self.root.bind('<MouseWheel>',self.ScrollEvent)
        # self.root.bind('<Enter>', self.resetCurrDeckData) # 按下回车
        # self.root.bind('<Key>', self.updateData)

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
                            print("检索到卡:",value["Id"],value["Name"],value["Index"])
                            if deckNums-count >= 0:
                                temp_key = sortByIndexDict[deckNums-count]
                                self.discoveryMap[temp_key] = value
                                count += 1
                    # 禁识之瓶 张数》25 and playID = 自己
                    if len(cardsDict.keys()) >= 25 :
                        pass
                        # self.specialMapJSZPQF.update(cardsDict)

    def getCIdsForDeckModule(self):
        pass
    
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

    def setBattleCardsModuleDataToUI(self,cardsSource):
        currDeckData = {}
        for key,value in cardsSource.items():
            temp_dict = {}
            # temp_dict["insId"] = key
            temp_dict["ctId"] = value["Id"]
            temp_dict["excess"] = False
            temp_dict["isNotExist"] = False
            currDeckData[key] = temp_dict
        return currDeckData

    def setCarriedCardModuleDataToUI(self,cardsSource):
        currDeckData = {}
        for key,value in cardsSource.items():
            temp_dict = {}
            temp_dict["ctId"] = value["Id"]
            temp_dict["excess"] = False
            temp_dict["isNotExist"] = self.isPlayedCard(key)
            currDeckData[key] = temp_dict
        return currDeckData

    def isPlayedCard(self,key):
        location = self.curr_memo_cards[key]["Location"] 
        if location != hex(Location.DECK.value) and location != hex(Location.HAND.value) and location != hex(Location.LEADER.value):
            return True
        return False

    def setAddedCardData(self,previousData,currData):
        self.anim_list_insId = []
        for dataKey in currData:
            if dataKey not in list(previousData.keys()):
                self.anim_list_insId.append(dataKey)
        self.currDeckData = currData


    def updateData(self):
        # print("日")
        origCardsInfo = {} 
        self.curr_memo_cards = cService.getMemoryCards()
        # 映射-发现池
        if self.CARD_DECK_INFO.isEnemy:
            self.fillDiscoveredCardOfBottomPlayerViewingAction()
            self.discoverCardMapCurrDeckData()
        # 映射替换replace
        self.battleCards = {}
        self.battleCards.update(self.curr_memo_cards)
        self.battleCards = cService.filterCardsByDeckCondition(self.battleCards,self.CARD_DECK_INFO)
        for key,value in self.onceExistInCarriedCards.items():
            if key in  self.battleCards.keys():
                cardUIData = global_var.get_value("AllCardDict")[str(value["Id"])]
                self.battleCards[key]["Id"] = value["Id"]
                self.battleCards[key]["Provision"] = cardUIData["provision"]
                self.battleCards[key]["Rarity"] = cardUIData["rarity"]
                self.battleCards[key]["FactionId"] = cardUIData["factionId"]
                self.battleCards[key]["Type"] = cardUIData["cardType"]
                self.battleCards[key]["Name"] = cardUIData["name"]
                self.battleCards[key]["BasePower"]  = cardUIData["power"] 
        # 映射补充add
        self.carriedCards = {}
        self.carriedCards.update(self.curr_memo_cards)
        self.carriedCards.update(self.onceExistInCarriedCards)
        self.carriedCards = cService.filterCardsIntoCarriedCards(self.carriedCards,self.CARD_DECK_INFO)
        # 映射曾经存在于carriedCards中的卡牌数据
        self.carriedCards = cService.sort_cardTemplate_by_provision(self.carriedCards)
        self.carriedCards = cService.addStratagemCard(self.carriedCards,self.curr_memo_cards,self.root.responseManager.playerId)
        self.onceExistInCarriedCards.update(self.carriedCards)

        # carriedCards变动时刷新卡组预测
        if self.modulePage != self.MODULE_PAGE_NORMAL:
            if self.carriedLazyLen != len(self.carriedCards):
                self.carriedLazyLen = len(self.carriedCards)
                self.setShowPage(self.modulePage)

        if not self.isShowRelationDeck:
            if self.CARD_DECK_INFO.dataModule == 0 :
                previousData = self.currDeckData
                currData = self.setBattleCardsModuleDataToUI(self.battleCards)
                self.currDeckData = currData
                self.setAddedCardData(previousData,currData)
            if self.CARD_DECK_INFO.dataModule == 1 :
                previousData = self.currDeckData
                currData = self.setCarriedCardModuleDataToUI(self.carriedCards)
                self.currDeckData = currData
                self.setAddedCardData(previousData,currData)

        else:
           
            self.currDeckData = {}
            if self.comparativeForecast:
                # 两个格式要一样
                self.currDeckData = self.getComparativeForecast(self.forecastDeck["sortedCards"],self.setCarriedCardModuleDataToUI(self.carriedCards))
            else:
                self.currDeckData = self.forecastDeck["sortedCards"]
            #######
            self.clearCarriedCardsStatus()
            # 可以分辨多余
            for key,value in self.currDeckData.items():
                # value['excess'] = False
                for carried_key,carried_value in self.carriedCards.items():
                    if carried_value["Id"] == value["ctId"] :
                        if "temp_existed" not in carried_value.keys():
                            carried_value['temp_existed'] = False
                        if not carried_value['temp_existed'] and self.isPlayedCard(carried_key):
                            value["isNotExist"] = True
                            carried_value['temp_existed'] = True
                            break
            # return currDeckData
        # 初始化图片，以及建立映射源
        self.initImgPool(self.currDeckData,self.imgScale)
        # 映射imageId到更新数据
        for key_insId,value in self.currDeckData.items():
            value["imageId"] = self.insIdMapImageId[key_insId]
        # UI
        for insId in self.anim_list_insId:
            self.anim_img_tips(insId, TipsType.WHITE)
        self.updateCardUI(self.currDeckData)
        self.updateCardExistEffectUI(self.currDeckData)
        self.setDeckStatus()
        self.after(400,self.updateData)

    def getComparativeForecast(self,forecastDeck,carriedDeck):
        comparativeCardStartIndex = 4000
        result = {}
        differenceList = []
        fdIds = []
        cdIds = []
        for key,value in forecastDeck.items():
            value["excess"] = False
            value['provision'] = global_var.get_value("AllCardDict")[str(value["ctId"])]['provision']
            fdIds.append(value["ctId"])
        for key,value in carriedDeck.items():
            value["excess"] = True
            cdIds.append(value["ctId"])

        commons = self.getCommonArray(cdIds,fdIds)
        ourAddDiffs = self.getDiffArray(cdIds,fdIds)
        enemyAddDiffs = self.getDiffArray(fdIds,cdIds)
        count = 0
        for ctId in ourAddDiffs:
            cardType = global_var.get_value("AllCardDict")[str(ctId)]['cardType']
            # name = global_var.get_value("AllCardDict")[str(ctId)]['name']
            if CardType(cardType) == CardType.STRATAGEM or CardType(cardType) == CardType.LEADER:
                continue
            key = comparativeCardStartIndex+count
            count += 1
            value = {
                'ctId': ctId,
                'provision' : global_var.get_value("AllCardDict")[str(ctId)]['provision'],
                'isNotExist' : False,
                'excess': True,
                'highlightType' : 2
            }
            result[key] = value
        for ctId in enemyAddDiffs:
            cardType = global_var.get_value("AllCardDict")[str(ctId)]['cardType']
            excess = True
            if CardType(cardType) == CardType.STRATAGEM or CardType(cardType) == CardType.LEADER:
                excess = False
            key = comparativeCardStartIndex+count
            count += 1
            value = {
                'ctId': ctId,
                'provision' : global_var.get_value("AllCardDict")[str(ctId)]['provision'],
                'isNotExist' : False,
                'excess': excess,
                'highlightType' : 1
            }
            result[key] = value
        for ctId in commons:
            key = comparativeCardStartIndex+count
            count += 1
            value = {
                'ctId': ctId,
                'provision' : global_var.get_value("AllCardDict")[str(ctId)]['provision'],
                'isNotExist' : False,
                'excess': False,
            }
            result[key] = value
        # 重新排序
        temp_sort_list = sorted(result.items(),key = lambda x: (-x[1]["provision"],x[1]["ctId"],-x[0]))
        # 调整策略卡位置
        last_data = temp_sort_list[len(temp_sort_list)-1]
        # 预测模式下，不会出现衍生物
        if last_data[1]['provision'] == 0:
            temp_sort_list.remove(last_data)
            temp_sort_list.insert(1,last_data)
        result = {}
        for i in temp_sort_list:
            result[i[0]] = i[1]
        return result

    # 设置卡组状态组[卡牌总数,单位数量,粮食]
    def setDeckStatus(self):
        total = 0
        unit = 0
        provision = 0
        cards = self.currDeckData
        highlight = self.root.responseManager.highlight

        for key,value in cards.items():

            if value['excess'] == True:
                if value['highlightType'] != 1:
                    continue
            if value["ctId"] == 0 :
                continue
            currCardBaseData = global_var.get_value("AllCardDict")[str(value["ctId"])]
            if value["isNotExist"] and (not self.CARD_DECK_INFO.isEnemy or self.isShowRelationDeck) and not highlight:
                continue
            temp_prov = currCardBaseData["provision"]
            if CardType(currCardBaseData["cardType"]) != CardType.LEADER:
                provision += temp_prov
                if CardType(currCardBaseData["cardType"]) != CardType.STRATAGEM:
                    total += 1
            cardType = currCardBaseData["cardType"]
            if cardType == CardType.UNIT.value :
                unit += 1
        self.root.responseManager.updateStatusBoard(total,unit,provision,highlight)
        
    def createDeckTipsPro(self):
        line_marginX = round(self.canvas_padding[0] + self.canvas_padding[0]/3)
        line_padY = round(self.root.WIN_WIDTH*0.0147928)
        nextCoordsY = 0
        fontSize_deckName = round(self.root.WIN_WIDTH*0.053)    #18
        # TODO 耦合
        fontSize_Author = round(self.root.WIN_WIDTH*0.038)      #13
        fontSize_RepeatRate = round(self.root.WIN_WIDTH*0.038)
        ################################################################   
        nextCoordsY += self.canvas_padding[1]
        width =  self.root.WIN_WIDTH - line_marginX*2
        # height = self.canvas_padding[1]+74*self.cardImgWidth/1053+(fontSize_deckName)*1.3+line_padY+(fontSize_Author)*1.3+(fontSize_RepeatRate)*1.3-74*self.cardImgWidth/1053
        height = round(self.root.WIN_WIDTH*0.24319)

        self.deckProfile = ft.get_imgTk_xy(r"main/resources/images/deck_preview/bg-mon-dark2.png",width,height)
        # self.deckProfile = ft.get_imgTk_xy(r"main/resources/images/deck_preview/LeaderFactionBg/64.png",width,height)
        self.deckProfileBg = self.can_bg.create_image(line_marginX,nextCoordsY + 74*self.cardImgWidth/1053/2, 
            anchor='nw' , image = self.deckProfile,tags="TipsUI")
        line_marginX += self.canvas_padding[0]/1.8
        ################################################################    
        # separator
        self.separator_top = ft.get_img_resized(r"main/resources/images/deck_preview/separator_1.png",self.cardImgWidth/1053)
        self.sep_top = self.can_bg.create_image(self.canvas_padding[0],nextCoordsY, 
            anchor='nw' , image = self.separator_top,tags="TipsUI")
        
        nextCoordsY += 74*self.cardImgWidth/1053
        deckName = self.forecastDeck["deckName"]
        self.temp_deckNameUIText = ft.getTextImg(self.cardImgWidth,(230,187,84),deckName,fontSize_deckName)
        self.textDeckName = self.can_bg.create_image(line_marginX,nextCoordsY,
        anchor="nw",tags=("TipsUI"),image=self.temp_deckNameUIText)
        ################################################################
        nextCoordsY += (fontSize_deckName)*1.3+line_padY
        deckAuthor = self.forecastDeck["deckAuthor"]
        differenceDays = self.forecastDeck["differenceDays"]
        deckAuthor = "作  者:  " + deckAuthor + "   {0}天前创建".format(differenceDays) 
        #image
        self.authorPrefixImg = ft.get_imgTk_xy(r"main/resources/images/deck_preview/AuthorPrefix.png",self.root.WIN_WIDTH*0.05,self.root.WIN_WIDTH*0.05)
        self.authorPrefix = self.can_bg.create_image(line_marginX,nextCoordsY+round((fontSize_Author)*1.3/2), 
            anchor='w' , image = self.authorPrefixImg,tags="TipsUI")
        self.temp_deckAuthorUIText = ft.getTextImg(round(self.cardImgWidth*0.91),(217, 216, 203),deckAuthor,fontSize_Author)
        self.textAuthorName = self.can_bg.create_image(line_marginX+self.cardImgWidth,nextCoordsY,
        anchor="ne",tags="TipsUI",image=self.temp_deckAuthorUIText)
        ################################################################################################
        nextCoordsY += (fontSize_Author)*1.3+line_padY/2
        content = self.forecastDeck["repeatRate"]
        content = "准确率:  {0}% ".format(round(content*100,1)) 
        #image
        self.authorPrefixImg_Red = ft.get_imgTk_xy(r"main/resources/images/deck_preview/AuthorPrefix_Red.png",self.root.WIN_WIDTH*0.05,self.root.WIN_WIDTH*0.05)
        self.authorPrefix_red = self.can_bg.create_image(line_marginX,nextCoordsY+fontSize_RepeatRate*1.3/2, 
            anchor='w' , image = self.authorPrefixImg_Red,tags="TipsUI")
        
        self.temp_deckRepeatRateUIText = ft.getTextImg(round(self.cardImgWidth*0.91),(217, 216, 203),content,fontSize_Author)
        self.textRepeatRateText = self.can_bg.create_image(line_marginX+self.cardImgWidth,nextCoordsY,
        anchor="ne",tags="TipsUI",image=self.temp_deckRepeatRateUIText)
        # self.tt = self.can_bg.create_text(self.can_size[0]/2,self.can_size[1]/2,text = content)
        # separator
        nextCoordsY += (fontSize_RepeatRate)*1.3
        self.separator_bottom = ft.get_img_resized(r"main/resources/images/deck_preview/separator_1.png",self.cardImgWidth/1053)
        self.sep_bottom = self.can_bg.create_image(self.canvas_padding[0],nextCoordsY,anchor='nw' , image = self.separator_bottom,tags="TipsUI")
        
    def resetRepeatRateUiText(self,num):
        print("更新重复率！")
        try:
            # TODO 耦合
            fontSize_deckName = round(self.root.WIN_WIDTH*0.053)    #18
            fontSize_Author = round(self.root.WIN_WIDTH*0.038)      #13

            num = self.forecastDeck["repeatRate"]
            deckName = self.forecastDeck["deckName"]
            deckAuthor = self.forecastDeck["deckAuthor"]
            differenceDays = self.forecastDeck["differenceDays"]

            self.temp_deckNameUIText = ft.getTextImg(self.cardImgWidth,(230,187,84),deckName,fontSize_deckName)
            self.can_bg.itemconfig(self.textDeckName,image = self.temp_deckNameUIText)
            ################################################################
            deckAuthor = "作  者:  " + deckAuthor + "   {0}天前创建".format(differenceDays) 
            #image
            self.authorPrefixImg = ft.get_imgTk_xy(r"main/resources/images/deck_preview/AuthorPrefix.png",self.root.WIN_WIDTH*0.05,self.root.WIN_WIDTH*0.05)
            self.can_bg.itemconfig(self.authorPrefix,image = self.authorPrefixImg)
            self.temp_deckAuthorUIText = ft.getTextImg(round(self.cardImgWidth*0.91),(217, 216, 203),deckAuthor,fontSize_Author)
            self.can_bg.itemconfig(self.textAuthorName,image = self.temp_deckAuthorUIText)
            ################################################################################################
            content = "准确率:  {0}% ".format(round(num*100,1)) 
            self.temp_deckRepeatRateUIText = ft.getTextImg(round(self.cardImgWidth*0.91),(217, 216, 203),content,fontSize_Author)
            self.can_bg.itemconfig(self.textRepeatRateText,image = self.temp_deckRepeatRateUIText )
        except Exception:
            pass
        
    def updateShowDeckTips(self):
        line_marginX = round(self.canvas_padding[0] + self.canvas_padding[0]/3)
        line_padY = round(self.root.WIN_WIDTH*0.0147928)
        nextCoordsY = 0
        fontSize_deckName = round(self.root.WIN_WIDTH*0.053)    #18
        fontSize_Author = round(self.root.WIN_WIDTH*0.038)      #13
        fontSize_RepeatRate = round(self.root.WIN_WIDTH*0.038)
        ################################################################   
        nextCoordsY += self.canvas_padding[1]
        width =  self.root.WIN_WIDTH - line_marginX*2
        # height = self.canvas_padding[1]+74*self.cardImgWidth/1053+(fontSize_deckName)*1.3+line_padY+(fontSize_Author)*1.3+(fontSize_RepeatRate)*1.3-74*self.cardImgWidth/1053
        height = round(self.root.WIN_WIDTH*0.24319)

        if len(self.can_bg.find_withtag("TipsUI")) == 0:
            self.createDeckTipsPro()
        else:
            self.can_bg.moveto(self.deckProfileBg,x=round(line_marginX),y=round(nextCoordsY + 74*self.cardImgWidth/1053/2))
            line_marginX += round(self.canvas_padding[0]/1.8)
            ################################################################    
            # separator
            self.can_bg.moveto(self.sep_top,x=self.canvas_padding[0],y=nextCoordsY)
            
            nextCoordsY += round(74*self.cardImgWidth/1053)
            self.can_bg.moveto(self.textDeckName,x=line_marginX,y=nextCoordsY)
            ################################################################
            nextCoordsY += round((fontSize_deckName)*1.3+line_padY)
            #image
            self.can_bg.moveto(self.authorPrefix ,x=line_marginX,y=nextCoordsY)
            self.can_bg.moveto(self.textAuthorName,x=round(line_marginX+self.root.WIN_WIDTH*0.075),y=nextCoordsY)
            ################################################################################################
            nextCoordsY += round((fontSize_Author)*1.3+line_padY/2)
            #image
            self.can_bg.moveto(self.authorPrefix_red,x=line_marginX,y=nextCoordsY)
            self.can_bg.moveto(self.textRepeatRateText,x=round(line_marginX+self.root.WIN_WIDTH*0.075),y=nextCoordsY)
            # self.can_bg.itemconfig(self.temp_deckRepeatRateUIText, state = "hidden")
            # separator
            nextCoordsY += round((fontSize_RepeatRate)*1.3)
            self.can_bg.moveto(self.sep_bottom,x=self.canvas_padding[0],y=nextCoordsY)
        return round(height*1.2)
        # return round(height+74*self.cardImgWidth/1053)

    def updateCardUI(self,deckData):
        uiCards = self.can_bg.find_withtag("UICard")
        for imageId in uiCards:
            self.can_bg.itemconfig(imageId, state = "hidden")
        count  = 0
        yOffset = 0

        if self.isShowRelationDeck:
            self.yOffset = self.updateShowDeckTips()
            yOffset += self.yOffset
            
        for key,value in deckData.items():
            iId = key
            self.can_bg.itemconfig(value["imageId"], state = "normal")
            if len(self.can_bg.find_withtag(str(iId)+"hiddenCard")) > 0:
                row = self.can_bg.find_withtag(str(iId)+"hiddenCard")[0]
                self.can_bg.moveto(row,x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
            self.can_bg.moveto(value["imageId"],x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
            # tipsEffect
            if len(self.can_bg.find_withtag(str(iId)+"effect_tips")) > 0:
                row = self.can_bg.find_withtag(str(iId)+"effect_tips")[0]
                self.can_bg.itemconfig(row,state="normal")
                self.can_bg.moveto(row,x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count+yOffset)
                
            count += 1
            # 排除衍生物没有cardType
            if value["ctId"] == 0:
                continue
            cardInfo = global_var.get_value("AllCardDict")[str(value["ctId"])]
            if CardType(cardInfo["cardType"]) == CardType.LEADER:
                yOffset += round(self.root.WIN_WIDTH*0.1479289) #50
            elif CardType(cardInfo["cardType"]) == CardType.STRATAGEM:
                yOffset += round(self.root.WIN_WIDTH**0.0207)  #7
    
    def anim_img_tips(self,insId,tipsType,anim_time=2500):
        # leader不做效果，应为要特殊适配大小
        try:
            if insId != 0 and self.currDeckData[insId]["ctId"]!=0:
                cardInfo = global_var.get_value("AllCardDict")[str(self.currDeckData[insId]["ctId"])]
                if CardType(cardInfo["cardType"]) == CardType.LEADER:
                    return 0
        except KeyError:
            pass
        count = 0
        try:
            count = list(self.currDeckData.keys()).index(insId)
        except Exception:
            return 0
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
        row_id = self.can_bg.create_image(0,0,image=self.panel.temp_img,
            tags = (str(insId)+"effect_tips","effect_tips"),state = "hidden")
        self.root.after(anim_time,self.anim_img_tips_hidden,row_id)
        
    def anim_img_tips_hidden(self,img_id):
        self.can_bg.delete(img_id)
    
    def hiddenAllEffectUI(self):
        effectUIs = self.can_bg.find_withtag("EffectUI")
        for effectUI in effectUIs:
            self.can_bg.itemconfig(effectUI, state = "hidden")
    
    def clearTipsUI(self):
        for imgId in self.can_bg.find_withtag("TipsUI"):
            try:
                self.can_bg.itemconfig(imgId, state = "hidden")
            except Exception:
                pass

    def showTipsUI(self):
        for imgId in self.can_bg.find_withtag("TipsUI"):
            try:
                self.can_bg.itemconfig(imgId, state = "normal")
            except Exception:
                pass
            # self.can_bg.delete(imgId)

    def updateCardExistEffectUI(self,deckData):
        self.hiddenAllEffectUI()
        count  = 0
        yOffset = 0

        if self.isShowRelationDeck:
            yOffset += self.yOffset

        for key,value in deckData.items():
            iId = key
            if len(self.can_bg.find_withtag(str(iId)+"hiddenCard")) == 0:
                color = self.darkCardEffectColor
                # if self.isShowRelationDeck and value["excess"]:
                #     color = self.excessCardEffectColor
                imgTk = ft.getDarkCardPreviewImgTk((self.cardImgWidth,self.cardEffectHeight),color)
                self.panel = tk.Label(master = self.root)
                self.panel.temp_img = imgTk
                self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*count+yOffset,
                anchor='nw',image=self.panel.temp_img, tags = (str(key)+"hiddenCard","EffectUI"),state="hidden")

            temp_list = self.can_bg.find_withtag(str(key)+"hiddenCard")
            if value["isNotExist"]:
                self.can_bg.itemconfig(temp_list[0], state = "normal")
            else:
                self.can_bg.itemconfig(temp_list[0], state = "hidden")

            # 排除衍生物没有cardType
            if value["ctId"] == 0:
                continue
            cardInfo = global_var.get_value("AllCardDict")[str(value["ctId"])]
            if CardType(cardInfo["cardType"]) == CardType.LEADER:
                yOffset += round(self.root.WIN_WIDTH*0.1479289) #50
            elif CardType(cardInfo["cardType"]) == CardType.STRATAGEM:
                yOffset += round(self.root.WIN_WIDTH**0.0207)  #7
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
                cardData["Provision"] = cardUIData["provision"]
                cardData["Type"] = cardUIData["cardType"]
                cardData["Rarity"] = cardUIData["rarity"]
                cardData["CurrPower"] = cardUIData["power"]
                cardData["FactionId"] = cardUIData["factionId"]
            else:
                cardData = {}
                cardData["Name"] = "未知"
                cardData["Id"] = 0
                cardData["Provision"] = self.curr_memo_cards[int(s_insId)]["Provision"]
                cardData["Type"] = self.curr_memo_cards[int(s_insId)]["Type"]
                cardData["Rarity"] = self.curr_memo_cards[int(s_insId)]["Rarity"]
                cardData["CurrPower"] = self.curr_memo_cards[int(s_insId)]["BasePower"]
                cardData["FactionId"] = self.curr_memo_cards[int(s_insId)]["FactionId"]
            try:
                cardData['Excess'] = value["excess"]
            except KeyError:
                cardData['Excess'] = False
            if cardData['Excess']:
                cardData['HighlightType'] = value["highlightType"]


            if len(self.can_bg.find_withtag(s_insId+"InsId")) == 0:
                # 不存在池中则实例化一个进入池
                # 多余的卡牌 即被excess标记的卡会有特殊样式
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
        if self.CARD_DECK_INFO.dataModule == 1:
            yOffset += 4
        if self.isShowRelationDeck:
            yOffset += 4
        total = 0
        cards = self.currDeckData
        total = len(self.currDeckData.keys())+3
        maxNum = int(self.can_size[1]/self.canvas_row_padding)
        if event.delta > 0 :
            # M-up
            if self.canvas_padding[1] < int((1.5) * self.canvas_row_padding):
                rate = self.canvas_padding[1]/int((1.5) * self.canvas_row_padding)
                elasticityFactor = 1
                if rate > 0 and rate < 1: 
                    elasticityFactor = 1-rate
                self.canvas_padding[1] += MOVE_DELTA*elasticityFactor
                self.updateCardUI(self.currDeckData)
        else:
            # M-down
            if self.canvas_padding[1] > int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset)):
                rate = self.canvas_padding[1]/int(-self.canvas_row_padding * (total-maxNum+yOffset if total > maxNum else self.canvas_padding[1]/self.canvas_row_padding+yOffset))
                elasticityFactor = 1
                if rate > 0 and rate < 1: 
                    elasticityFactor = 1-rate
                self.canvas_padding[1] -= MOVE_DELTA * elasticityFactor
                self.updateCardUI(self.currDeckData)
        self.canvas_padding[1] = int(self.canvas_padding[1])
    
    def clear_deck_img(self):
        for img_id in self.can_bg.find_all():
            self.can_bg.delete(img_id)

    def resetType(self,CardDeckInfo):
        self.isShowRelationDeck = False
        self.CARD_DECK_INFO = CardDeckInfo
        self.root.responseManager.setTileText(CardDeckInfo.titleName)
        self.curr_memo_cards.clear()
        self.clear_deck_img()

        # 重置因为滚轮事件导致的img偏移
        self.canvas_padding[1] = 0
    
    def setCardDeckInfo(self,CardDeckInfo):
        self.CARD_DECK_INFO = CardDeckInfo
# ----------------------------------------------------------------
    # 相关:计算重合率高的卡组-核心函数
    def getRelevantDeck(self,index):
        # 预测卡组源的CtIds列表
        currDeckCtIds = []
        # 映射禁识之瓶:启封
        self.temp_dict = {}
        self.temp_dict.update(self.carriedCards)
        if len(self.specialMapJSZPQF.keys()) > 0:
            self.temp_dict = {}
            self.temp_dict.update(self.specialMapJSZPQF)
        for key,value in self.temp_dict.items():
            currDeckCtIds.append(value["Id"])
        # 根据factionId初步过滤卡组数据库
        factionId = cService.getFactionId(self.root.responseManager.playerId)
        filterFactionDeck = cService.getDeckByFactionId(factionId,global_var.get_value("decks"))
        temp_sort_list = cService.getSortedDeckByRepeated(currDeckCtIds,filterFactionDeck)
        maxIndex = len(temp_sort_list)-1 
        if maxIndex > 0:
            if index > maxIndex:
                index = maxIndex
            if maxIndex < 0:
                # TODO 未找到需要卡组
                pass
        return temp_sort_list[index]
            
    def clearCarriedCardsStatus(self):
        for key,value in self.carriedCards.items():
            try:
                self.carriedCards[key]["temp_existed"] = False
            except KeyError:
                pass

    def setShowPage(self,pageIndex):
        if pageIndex == self.MODULE_PAGE_NORMAL:
            self.setDefaultPage()
        else:
            # 根据pageIndex设置数据
            self.clearCarriedCardsStatus()
            self.showTipsUI()
            self.isShowRelationDeck = True
            
            relevantDeck = self.getRelevantDeck(pageIndex - 1)
            self.setForecastDeck(relevantDeck)
            self.resetRepeatRateUiText(self.forecastDeck["repeatRate"])
            self.root.responseManager.setTileText("相 似 卡 组 - {0}".format(pageIndex))

    def setForecastDeck(self,relevantDeck):
        count = 2000
        index = 0 # 只用来记录确立移动stratagem的位置
        showData = {}
        mostRelevantDeck = relevantDeck["sortedCtIds"]
        allCardMap = global_var.get_value("AllCardDict")
        mostRelevantDeck_Sort = sorted(mostRelevantDeck,key=lambda x: (-allCardMap[str(x)]["provision"],x))
        for ctId in mostRelevantDeck_Sort:
            count += 1
            index += 1
            # 将stratagem卡移到位置二
            if index == 2:
                for temp_ctId in reversed(mostRelevantDeck_Sort):
                    if CardType(global_var.get_value("AllCardDict")[str(temp_ctId)]["cardType"]) == CardType.STRATAGEM:
                        showData[count] = {"ctId":temp_ctId,"name":global_var.get_value("AllCardDict")[str(temp_ctId)]["name"], "isNotExist":False}
                        count += 1
                        break
            if CardType(global_var.get_value("AllCardDict")[str(ctId)]["cardType"]) == CardType.STRATAGEM:
                continue
            # 正常存储
            showData[count] = {"ctId":ctId,"name":global_var.get_value("AllCardDict")[str(ctId)]["name"], "isNotExist":False}

        self.forecastDeck["sortedCards"] = showData
        deckTimeFormat = self.transStrTimeToStamp(relevantDeck['time'],"%Y-%m-%dT%H:%M:%S.000+00:00")
        nowTimeFormat = datetime.datetime.now()
        differenceDays = (nowTimeFormat-deckTimeFormat).days
        self.forecastDeck["differenceDays"] = differenceDays
        self.forecastDeck["deckName"] = self.shortenText(relevantDeck['deckName'],26)
        self.forecastDeck["deckAuthor"] = self.shortenText(relevantDeck['deckAuthor'],14)
        self.forecastDeck["repeatRate"] = relevantDeck['repeatRate']

        self.currDeckData = self.forecastDeck["sortedCards"]

    # 相关:【推荐卡组】
    # 点击事件的入口函数
    def setArrowModule(self,direct):
        self.clearTipsUI()
        self.isShowRelationDeck = True
        # self.CARD_DECK_INFO.dataModule = 3
        if direct < 0:
            #left
            self.modulePage -= 1 if self.modulePage > self.MODULE_PAGE_MIN else 0
        elif direct > 0:
            # right
            self.modulePage += 1 if self.modulePage < self.MODULE_PAGE_MAX else 0

        if self.modulePage >= self.MODULE_PAGE_MAX:
            self.modulePage = self.MODULE_PAGE_MAX
            self.root.responseManager.title.disableArrows()
            self.root.responseManager.title.showOneArrow(True)
            self.canvas_padding[1] = 0
        elif self.modulePage <= self.MODULE_PAGE_MIN:
            self.modulePage = self.MODULE_PAGE_MIN
            self.root.responseManager.title.disableArrows()
            self.root.responseManager.title.showOneArrow(False)
            self.canvas_padding[1] = 0
        else:
            self.root.responseManager.title.ableArrows()
        self.setShowPage(self.modulePage)

    def setDefaultPage(self):
        self.clearTipsUI()
        self.isShowRelationDeck = False
        self.resetType(self.CARD_DECK_INFO)
        self.modulePage = self.MODULE_PAGE_NORMAL
        self.root.responseManager.title.disableArrows()
        self.root.responseManager.title.showOneArrow(False)


    def shortenText(self,text,length):
        if len(text) >= length:
            return text[:length-3] + "..."
        else :
            return text

    def transStrTimeToStamp(self,time,format):
        # if format == "yyyy-MM-dd HH:mm:ss":
        return datetime.datetime.strptime(time,format)
    
    def getDiffArray(self,source,target):
        result = []
        clone_target = target[:]
        for i in source:
            if i not in clone_target:
                result.append(i)
            else:
                clone_target.remove(i)
        return result
    
    def getCommonArray(self,source,target):
        result = []
        clone_target = target[:]
        for i in source:
            if i in clone_target:
                result.append(i)
                clone_target.remove(i)
        return result
####################################################################################################################
####################################################################################################################
