import pymem
import services.CardService
from dao.CardDao import *
from enums.ERequestAction import *
from enums.GameEnum import *
from enums.GwentEnum import *
from services.CardService import *
from tools.FileTool import *


        # return value
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

def getOwnerPlayerId():
    localUserId = hex(read_multi_bytes(pm,gi+0x20,[0x60,0x29],0x1))
    bottomPlayerId = hex(read_multi_bytes(pm,gi+0x20,[0x60,0x2A],0x1))
    currentPlayerId = hex(read_multi_bytes(pm,gi+0x20,[0x60,0x2C],0x1))
    print(localUserId,bottomPlayerId,currentPlayerId)

def getP1Status():
    p1 = read_multi_bytes(pm,gi+0x28,[0x28,0x1c],0x4)
    print("p1-add:",hex(read_int64(pm,gi+0x28,[0x28])))
    print("p1-status:",p1)


if __name__ == "__main__":
    get_baseAddress()
    # 获得Card
    cardsAdd = cardDao.getAllCardsByGI(gi)
    cts = []
    cardDict = getCardDataJsonDict()
    ##
    getOwnerPlayerId()
    # print("#######################################")
    print("GI:",hex(gi))
    print("GameStatus:",EGameStatus(read_multi_bytes(pm,gi+0x20,[0xe8],1)))
    print("################################")
    roundInfosAdd = read_multi_bytes(pm,gi+0x20,[0x68,0x18],0x8)
    print("RoundInfo[]:",hex(read_multi_bytes(pm,gi+0x20,[0x68,0x18],0x8)))
    for i in range(0,3):
        print("\tindex:",hex(read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x10],0x4)))
        left_score = read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x18,0x20],0x4)
        right_score = read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x18,0x24],0x4)
        print("\tscores:{0}-{1}".format(left_score, right_score))
        print("\tstartingPlayerId:",hex(read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x20],0x1)))
        print("\twinnerId:",hex(read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x21],0x1)))
        print("\tturnIndex:",hex(read_multi_bytes(pm,roundInfosAdd+0x20+i*0x8,[0x24],0x4)))
        print("")

    print("################################")
    print("currRoundIndex:",hex(read_multi_bytes(pm,gi+0x20,[0x68,0x20],0x4)))
    print("winner_playId:",hex(read_multi_bytes(pm,gi+0x20,[0x68,0x24],0x1)),"#3=平局")
    print("EndGameReason:",EGameEndReason(read_multi_bytes(pm,gi+0x20,[0x68,0x25],0x1)))
    
    
    print("EGameMode:",EGameMode(read_memory_bytes(pm,gi+0x38,1)))
    print("GameId:",read_multi_bytes(pm,gi+0x28,[0x48],8))
    print("EBattleType:",EBattleType(read_multi_bytes(pm,gi+0x28,[0x58],1)))
    
    # player的rank、level、MMR、Name等
    # player deck、factionId
    # print("pasdfaed:",hex(read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20,0x60,0x10],0x8)))
    print("")

    print("p2Add",hex(read_int64(pm,gi+0x28,[0x28,0x38])))
    for i in range(0,2):
        print(i,"############")
        nameAdd = read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x10],0x8)
        print("nameAdd",hex(nameAdd))
        print("p{0}-name-add:".format(i+1),read_String(pm,nameAdd))
        print("p{0}-serviceId:".format(i+1),read_int64(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x18]))
        # titleName = read_int64(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x20])
        # print("p{0}-title:".format(i+1),read_String(pm,titleName))
        # print("p{0}-level:".format(i+1),read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x30],0x4))
        print("p{0}-ParagonLevel:".format(i+1),read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x34],0x4))
        print("p{0}-MMR:".format(i+1),read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x38],0x4))
        print("p{0}-rank:".format(i+1),read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x60,0x3c],0x4))
        print("p{0}-factionId:".format(i+1), read_multi_bytes(pm,gi+0x20,[0x60,0x18,0x20+i*0x8,0x28,0x10],0x4))
        cardListAdd = read_int64(pm,gi+0x28,[0x28-i*0x8,0x38,0x28,0x10])
        nums = read_int64(pm,cardListAdd+0x18,[])
        result = []
        for i in range(0,nums):
            ctId = read_memory_bytes(pm,cardListAdd+0x20+i*0x8,0x4)
            if ctId != 0:
                result.append(ctId)
        print(result)

