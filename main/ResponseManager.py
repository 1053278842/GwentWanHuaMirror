import bean.global_var as global_var
import services.CardService as cs
from bean.CardDeckTypeInfo import CardDeckTypeInfo
from enums.GwentEnum import *
from RequestManager import RequestManager


class ResponseManager(object):

    def __init__(self,isEnemy):
        # pass
        self.CARD_DECK_INFO = self.set_card_deck_info(isEnemy)
        self.CARD_DECK_INFO[1].isActive = True
        self.DEFAULT_CARD_DECK_INFO = self.CARD_DECK_INFO[1]
        # 初始化
        self.requestManager = RequestManager()

    def set_card_deck_info(self,isEnemy):
        result_list = []
        if not isEnemy:
            result_list.append(CardDeckTypeInfo("我  ·  卡  组",Location.DECK,isSortByIndex=False,dataModule=1,isMain=True,buttonName="卡组")) 
            result_list.append(CardDeckTypeInfo("我  ·  牌  库",Location.DECK,buttonName="牌库"))
            result_list.append(CardDeckTypeInfo("我  ·  墓  场",Location.GRAVEYARD,buttonName="墓场"))
            result_list.append(CardDeckTypeInfo("我  ·  放  逐",Location.VOID,buttonName="放逐"))
            # result_list.append(CardDeckTypeInfo("我  的  放  逐  池",Location.VOID,buttonName="卡组"))
            result_list.append(CardDeckTypeInfo("我  ·  手  卡",Location.HAND,buttonName="手牌"))
            result_list.append(CardDeckTypeInfo("我  ·  战  场  卡",Location.RANGED,buttonName="场地",secLocation=Location.MELEE))
        else:
            result_list.append(CardDeckTypeInfo("敌  ·  卡  组",Location.DECK,isSortByIndex=False,dataModule=1,isMain=True,buttonName="卡组",isEnemy = True)) 
            result_list.append(CardDeckTypeInfo("敌  ·  牌  库",Location.DECK,buttonName="牌库",isEnemy = True))
            result_list.append(CardDeckTypeInfo("敌  ·  墓  场",Location.GRAVEYARD,buttonName="墓场",isEnemy = True))
            result_list.append(CardDeckTypeInfo("敌  ·  放  逐",Location.VOID,buttonName="放逐",isEnemy = True))
            result_list.append(CardDeckTypeInfo("敌  ·  手  卡",Location.HAND,buttonName="手牌",isEnemy = True))
            result_list.append(CardDeckTypeInfo("敌  ·  战  场  卡",Location.RANGED,buttonName="场地",secLocation=Location.MELEE,isEnemy = True))
        return result_list

    def register(self,bg,title,module,status,cardList):
        self.bg = bg
        self.title = title
        self.module = module
        self.status = status
        self.cardList = cardList
    
########################################################################
## 初始化数据
########################################################################

    # 获取p1/p2相关数据【当前P,我的P】
    def getCurrBattleInfo(self):
        self.battInfo = cs.getCurrBattleInfo()
        return 0

    # 获取当前用户的操作状态
    def getPlayerActionsCode(self):
        # 只由敌方玩家响应管理器响应
        # 只捕捉底部玩家的操作
        if self.battInfo.localPlayerId != self.playerId:
            statusCode = cs.getPlayerEnableActionsStatus(self.battInfo.localPlayerId)
            return statusCode
        else:
            return 0

    def setPlayerId(self):
        card_deck_info = self.cardList.CARD_DECK_INFO
        playerId = self.battInfo.topPlayerId
        # 响应管理器也暂存一个用户id方便标识
        if card_deck_info.isEnemy:
            playerId = self.battInfo.topPlayerId
            self.playerId = self.battInfo.topPlayerId
            self.enemyPlayerId = self.battInfo.bottomPlayerId
        else:
            playerId = self.battInfo.bottomPlayerId
            self.playerId = self.battInfo.bottomPlayerId
            self.enemyPlayerId = self.battInfo.topPlayerId

        # 批量该玩家，防止按钮一点又跑到p1。
        for cdi in self.CARD_DECK_INFO:
            cdi.playerId = playerId

        # print(card_deck_info.playerId,card_deck_info.isEnemy)
        self.cardList.setCardDeckInfo(card_deck_info)
    
    def setDeckInfo(self,playerId):
        temp_dict = cs.getDeckInfo(playerId)
        m_playerCardNums = temp_dict["totalCardNums"]
        m_isDefensive = temp_dict["isDefensive"]
        m_leaderIndex = temp_dict["leaderIndex"]
        if playerId == 1:
            playerId =2 
        elif playerId == 2:
            playerId = 1

        temp_dict = cs.getDeckInfo(playerId)
        e_playerCardNums = temp_dict["totalCardNums"]
        e_isDefensive = temp_dict["isDefensive"]  
        e_leaderIndex = temp_dict["leaderIndex"]

        # 范围
        insIds = cs.getPlayerCarriedCarInsIds(self.playerId)
        self.maxCardNums = max(insIds)
        self.minCardNums = min(insIds) -1

        # if m_leaderIndex > e_leaderIndex:
        #     self.maxCardNums = m_playerCardNums + e_playerCardNums
        #     self.minCardNums = m_leaderIndex
        # else:
        #     self.maxCardNums = e_leaderIndex - 1
        #     self.minCardNums = m_leaderIndex
        
        for cdi in self.CARD_DECK_INFO:
            cdi.maxCardNums = self.maxCardNums
            cdi.minCardNums = self.minCardNums

        m_MaxCardNums = m_playerCardNums
        print("leaderIndex",m_leaderIndex,e_leaderIndex)
        print("【{0}】 | ".format(playerId),"CardMinIndex:",self.minCardNums,"CardMaxIndex:",self.maxCardNums)
        # self.allCardNums = m_playerCardNums+e_playerCardNums


########################################################################
## 响应事件
########################################################################

    # 开始获取数据等新
    def startDataLoop(self):
        self.getCurrBattleInfo()
        self.setPlayerId()
        self.setDeckInfo(self.playerId)
        self.cardList.updateData()
        # 初始化箭头显示
        self.cardList.setDefaultPage()
        # # 初始化decks.json文件
        # battleInfo = cs.getBattleInfo()
        # factionId_1 = battleInfo["players"][0]["faction_id"]
        # factionId_2 = battleInfo["players"][1]["faction_id"]
        # result = self.requestManager.getDecks(factionId_1)
        
        # result2 = self.requestManager.getDecks(factionId_2)
        # for dict_row in result2:
        #     result.append(dict_row)
        # global_var.set_value("decks",result)


    # 更新status
    def updateStatusBoard(self,total,unit,provision):
        self.status.update_data(total,unit,provision)
    
    # 根据card_deck_info 对象，更新当前筛选条件
    def resetShowListCondition(self,card_deck_info):
        self.cardList.setDefaultPage()
        self.cardList.resetType(card_deck_info)
        self.title.updateText(card_deck_info)
        self.status.update_data(0,0,0)

    # 点击箭头时，卡牌列表转为显示相关卡组
    def setCardListShowRelatedDeck(self,direct):
        # for widget in self.cardList.winfo_children():
        #     widget.destroy()
        self.cardList.setArrowModule(direct)
        # self.cardList.setShowRelateDeck(direct)
    
    def setTileText(self,text):
        self.title.setTitle(text)

