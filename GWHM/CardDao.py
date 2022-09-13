import binascii
from MemoryTool import *

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
        gameInstanceAdd = read_int64(self.pm,self.baseAddress+0x032af668,[0xb8,0x0,0x38])
        return gameInstanceAdd

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
            # AddressToString(card,1)
        # print("成功获取",len(cards),"个Card对象地址",)
        return cards
        
    # 获取CardManager根据GameController
    def getCardManagerByGC(self,gameController):
        cm = read_int64(self.pm,gameController+0x70,[])
        # AddressToString(cm)
        return cm

    # 返回GameInstance下的GameController对象地址
    def getGameControllerByGameInstance(self,gi):
        gc = read_int64(self.pm,gi+0x20,[])
        # AddressToString(gc)
        return gc


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