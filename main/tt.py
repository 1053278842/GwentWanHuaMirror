import pymem
import services.CardService
from dao.CardDao import *
from enums.ERequestAction import *
from services.CardService import *
from tools.FileTool import *


# 获取程式模块基址
def get_baseAddress():
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll
    global cardDao
    cardDao = CardDao(pm,baseAddress)
    global app
    app = read_int64(pm,baseAddress+0x32b53e0,[0xb8,0x0])
    global gi
    gi = cardDao.getGameInstance()
    global gc
    gc = read_int64(pm,gi+0x20,[])
    print("gc:",hex(gc))


if __name__ == "__main__":
    get_baseAddress()
    # 获得Card
    cardsAdd = cardDao.getAllCardsByGI(gi)
    cts = []
    cardDict = getCardDataJsonDict()
    # print("#######################################")
    # 实例化CardTemplate和Card,并建立关系
    # for i in range(0,64):
    #     startAdd = 0x1fbc1aea030+0x18*i
    #     nameAdd = read_int64(pm,startAdd,[0x10,0x20,0x0])
    #     # print(hex(nameAdd+0x10))
    #     name = read_Type_Name(pm,nameAdd)
    #     print(name + " " + hex( read_int64(pm,startAdd,[0x10])))
    player1managerAdd = read_int64(pm,gi+0x20,[0x60,0x18,0x20,0x28,0x50,0x10])
    nums = read_int64(pm,player1managerAdd+0x18,[])
    for i in range(0,nums):
        insId = read_memory_bytes(pm,player1managerAdd+0x20+i*0x2,2)
        print(insId)
    player2managerAdd = read_int64(pm,gi+0x20,[0x60,0x18,0x28,0x28,0x50,0x10])
    print(hex(player1managerAdd),nums)
    print(hex(player2managerAdd))
