import services.CardService as cs
from bean.CardDeckTypeInfo import CardDeckTypeInfo
from enums.GwentEnum import *


class ResponseManager(object):

    def __init__(self,isEnemy):
        # pass
        self.CARD_DECK_INFO = self.set_card_deck_info(isEnemy)
        self.CARD_DECK_INFO[1].isActive = True
        self.DEFAULT_CARD_DECK_INFO = self.CARD_DECK_INFO[1]

    def set_card_deck_info(self,isEnemy):
        result_list = []
        if not isEnemy:
            result_list.append(CardDeckTypeInfo("我  ·  卡  组",Location.DECK,isSortByIndex=False,isMain=True,buttonName="卡组")) 
            result_list.append(CardDeckTypeInfo("我  ·  牌  库",Location.DECK,buttonName="牌库"))
            result_list.append(CardDeckTypeInfo("我  ·  墓  场",Location.GRAVEYARD,buttonName="墓场"))
            result_list.append(CardDeckTypeInfo("我  ·  放  逐",Location.VOID,buttonName="放逐"))
            # result_list.append(CardDeckTypeInfo("我  的  放  逐  池",Location.VOID,buttonName="卡组"))
            result_list.append(CardDeckTypeInfo("我  ·  手  卡",Location.HAND,buttonName="手牌"))
            result_list.append(CardDeckTypeInfo("我  ·  战  场  卡",Location.RANGED,buttonName="场地",secLocation=Location.MELEE))
        else:
            result_list.append(CardDeckTypeInfo("敌  ·  卡  组",Location.DECK,isSortByIndex=False,isMain=True,buttonName="卡组",isEnemy = True)) 
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

    def setPlayerId(self):
        card_deck_info = self.cardList.CARD_DECK_INFO
        playerId = self.battInfo.topPlayerId
        if card_deck_info.isEnemy:
            playerId = self.battInfo.topPlayerId
        else:
            playerId = self.battInfo.bottomPlayerId
        # 批量该玩家，防止按钮一点又跑到p1。
        for cdi in self.CARD_DECK_INFO:
            cdi.playerId = playerId

        print(card_deck_info.playerId,card_deck_info.isEnemy)
        self.cardList.setCardDeckInfo(card_deck_info)

########################################################################
## 响应事件
########################################################################

    # 开始获取数据等新
    def startDataLoop(self):
        self.getCurrBattleInfo()
        self.setPlayerId()
        self.cardList.show_data_frame()

    # 更新status
    def updateStatusBoard(self,total,unit,provision):
        self.status.update_data(total,unit,provision)
    
    # 根据card_deck_info 对象，更新当前筛选条件
    def resetShowListCondition(self,card_deck_info):
        self.cardList.resetType(card_deck_info)
        self.title.updateText(card_deck_info)
        self.status.update_data(0,0,0)

