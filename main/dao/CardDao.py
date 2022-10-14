import binascii

from enums.ERequestAction import *
from tools.decorators import *
from tools.MemoryTool import *


class CardDao():

    def __init__(self, pm, baseAddress):
        self.pm = pm
        self.baseAddress=baseAddress

    def getCardTemplateByCard(self,card):
        return read_int64(self.pm,card+0x48,[])

    # 返回GameInstance对象地址(10进制)
    def getGameInstance(self):
        # 10.8 32a9090
        # 10.9 32af668
        # 10.10 32e7390
        # 10.10 热修1 32b53e0
        # 10.10 热修2 32bda60
        gameInstanceAdd = read_int64(self.pm,self.baseAddress+0x32bda60,[0xb8,0x0,0x38])
        return gameInstanceAdd
    
    def getLocalPlayerId(self,pm,giAdd):
        return read_multi_bytes(pm,giAdd+0x20,[0x60,0x29],0x1)

    def getBottomPlayerId(self,pm,giAdd):
        return read_multi_bytes(pm,giAdd+0x20,[0x60,0x2A],0x1)
    
    def getTopPlayerId(self,pm,giAdd):
        return read_multi_bytes(pm,giAdd+0x20,[0x60,0x2B],0x1)

    def getCurrPlayerId(self,pm,giAdd):
        return read_multi_bytes(pm,giAdd+0x20,[0x60,0x2c],0x1)


    def getPlayerEnableActionsStatus(self,pm,giAdd,playerId):
        playersArrayAdd =read_multi_bytes(self.pm,giAdd+0x20,[0x60,0x18],0x8)
        playerActionStatusCode = read_multi_bytes(pm,playersArrayAdd+0x18+int(playerId)*0x8,[0x30,0x1c],0x4)
        return playerActionStatusCode
    
    def cardListAddToDict(self,pm,gi,cardListAdd):
        listStructAdd = read_int64(pm,cardListAdd+0x10,[])
        num = read_memory_bytes(pm,listStructAdd+0x18,0x8)
        cts = []
        for i in range(0,num):
            cardAdd = read_memory_bytes(pm,listStructAdd+0x20+i*0x8,0x8)
            if cardAdd == 0:
                break
            cardTemplate = self.getCardTemplateByCard(cardAdd)
            ct_dict = self.initCtData(pm,cardTemplate,cardAdd)
            cts.append(ct_dict)
        return cts
    
    # 高耦合
    def initCtData(self,pm,ctAdd,cardAdd):
        result = {}

        # CardTemplate
        result["Id"]         = read_memory_bytes(pm,ctAdd+0x10,0x8)
        result["FactionId"]  = read_memory_bytes(pm,ctAdd+0x40,0x4)
        result["Rarity"]     = read_memory_bytes(pm,ctAdd+0x21,0x3)
        result["Provision"]  = read_memory_bytes(pm,ctAdd+0x5c,0x4)
        result["Type"]       = read_memory_bytes(pm,ctAdd+0x49,0x3)

        # Card
        result["PlayId"]     = read_memory_bytes(pm,cardAdd+0x5c,0x4)
        result["Location"]   = read_memory_bytes(pm,cardAdd+0x60,0x4)
        result["Index"]      = read_memory_bytes(pm,cardAdd+0x64,0x4)
        result["Address"]    = cardAdd
        result["CardId"]     = read_memory_bytes(pm,cardAdd+0x58,0x4)
        result["FromPlayerId"] = read_memory_bytes(pm,cardAdd+0x78,0x1)
        # CardData
        result["BasePower"]  = read_multi_bytes(pm,cardAdd+0xA0,[0x20,0x18],0x4)
        result["CurrPower"]  = read_multi_bytes(pm,cardAdd+0xA0,[0x20,0x1C],0x4)

        return result

    def getViewingCards(self,pm,gi):
        # getP1Status()
        # 0x20: GameController
        # 0x98: RequestManager
        # 0x18: Requests (List<ARequestAction>)
        # 0x10: list of requests
        add = read_int64(pm,gi+0x20,[0x98,0x18,0x10])

        # 0x18: list.size
        # 0x18+0x8: list.head
        size = read_int64(pm,add+0x18,[])
        for i in range(1,size+1):
            actionObjAdd = read_int64(pm,add+0x18+0x8*i,[])
            if actionObjAdd != 0:
                ########################
                ## ARequestAction 
                # 0x0 对象详细信息【dll,类型名】    # 区分用
                # 根据0x0 判别对象
                objDetailedInfo = read_int64(pm,actionObjAdd+0x0,[])
                typeName = read_Type_Name(pm,objDetailedInfo)
                if typeName != ActionName.REQUEST_CARD_CHOICES_ACTION.value:
                    continue
                    print("【警告】未检测到RequestCardChoicesAction事件!",typeName)
                elif typeName == ActionName.REQUEST_CARD_CHOICES_ACTION.value:
                    ##########################
                    # 0x58(8) validChoices  # 没法区分敌我牌，创造关键词等情况
                    validChoiceCardsAdd = read_memory_bytes(pm,actionObjAdd+0x58,0x8)
                    return validChoiceCardsAdd
        return 0

    # 获取allCards 根据GameInstance
    def getAllCardsByGI(self,gameInstanceAdd):
        cardsAdd = read_int64(self.pm,gameInstanceAdd+0x20,[0x70,0x28])
        # AddressToString(cardsAdd,1)
        cardNums = read_int64(self.pm,cardsAdd+0x18,[])
        cards=[]
        for i in range(0,cardNums-1):
            try:
                card = read_int64(self.pm,cardsAdd+0x28+i*0x8,[])
                if(card == 0):
                    break
                cards.append(card)
            except Exception:
                print("【异常】终止导出allCards")
                break
        return cards

    # 获取到对象的类型名
        # len 默认值2 意味返回2行即16个hex长度的ascii码
        # len 指定返回ascii长度,len(1)=int64=8个hex长
        # return 函数类型
    def getAddTypeName(self,address,len=1):
        if(len < 1):
            print("len长度不合法!已经终止getAddTypeName()")
            return
        result_name = ""
        for i in range(0, len):
            temp_add = read_int64(self.pm,address,[0x10,i*0x8])
            temp_add_hex = hex(temp_add)
            temp_add_hex_no_header = temp_add_hex[2:]
            result_name+=str(binascii.a2b_hex(temp_add_hex_no_header)[::-1],"utf8")
        return result_name
    
    def getPlayerManagerByGi(self,gi):
        cm = read_int64(self.pm,gi+0x20,[0x60,0x18,0x20])
        return cm

