import pymem
from tools.FileTool import *
from dao.CardDao import *
from services.CardService import *
import services.CardService
from enums.ERequestAction import *
# 高耦合
def initCtData(pm,ctAdd,cardAdd):
    result = {}
    result["Id"]         = read_memory_bytes(pm,ctAdd+0x10,0x8)
    # result["Name"]       =cardDict[str(ct.id)]['name']
    result["FactionId"]  = read_memory_bytes(pm,ctAdd+0x40,0x4)
    result["Rarity"]     = read_memory_bytes(pm,ctAdd+0x21,0x3)
    result["Provision"]  = read_memory_bytes(pm,ctAdd+0x5c,0x4)
    result["Type"]       = read_memory_bytes(pm,ctAdd+0x49,0x3)
    result["PlayId"]     = read_memory_bytes(pm,cardAdd+0x5c,0x4)
    result["Location"]   = read_memory_bytes(pm,cardAdd+0x60,0x4)
    result["Index"]      = read_memory_bytes(pm,cardAdd+0x64,0x4)
    result["Address"]    = cardAdd
    result["CardId"]     = read_memory_bytes(pm,cardAdd+0x58,0x4)
    # CardData
    result["BasePower"]  = read_multi_bytes(pm,cardAdd+0xA0,[0x20,0x18],0x4)
    result["CurrPower"]  = read_multi_bytes(pm,cardAdd+0xA0,[0x20,0x1C],0x4)

    return result
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

def pack_cardTemplate(cts):
    cardDict = getCardDataJsonDict()
    # 装载结果
    count = 0 
    result_dict = {}
    for ct in cts:
        count += 1
        temp_dict = {}
        key                     = ct["CardId"]
        temp_dict["InstanceId"] = ct["CardId"]
        temp_dict["Id"]         = ct["Id"]
        temp_dict["Name"]       = "未知"
        if ct["Id"] != 0 and ct["CardId"] !=0 : 
            temp_dict["Name"]       = cardDict[str(ct["Id"])]['name']
        temp_dict["FactionId"]  = ct["FactionId"]
        temp_dict["Rarity"]     = ct["Rarity"]
        temp_dict["Provision"]  = ct["Provision"]
        temp_dict["Type"]       = CardType(ct["Type"])
        temp_dict["PlayId"]     = hex(ct["PlayId"])
        temp_dict["Location"]   = hex(ct["Location"])
        temp_dict["Index"]      = hex(ct["Index"])
        temp_dict["Address"]    = hex(ct["Address"])
        temp_dict["BasePower"]      = ct["BasePower"] 
        temp_dict["CurrPower"]      = ct["CurrPower"] 

        result_dict[key]=temp_dict
            # print(temp_dict["Name"],temp_dict["Location"],temp_dict["Type"],temp_dict["Rarity"])
                # Test
            # print(temp_dict["Address"],temp_dict["Name"] )
            # print(read_multi_bytes(pm,cardAdd+0x18,[0x10,0x10],0x4))
    return result_dict

def printList(list):
    print(list["InstanceId"],list["PlayId"],list["Name"],list["Type"],list["Location"],list["Address"],list["Index"])

def cardListToString(cardListAdd):
    listStructAdd = read_int64(pm,cardListAdd+0x10,[])
    num = read_memory_bytes(pm,listStructAdd+0x18,0x8)
    cts = []
    for i in range(0,num):
        cardAdd = read_memory_bytes(pm,listStructAdd+0x20+i*0x8,0x8)
        if cardAdd == 0:
            break
        cardTemplate = cardDao.getCardTemplateByCard(cardAdd)
        ct_dict = initCtData(pm,cardTemplate,cardAdd)
        cts.append(ct_dict)

    # sort_cardTemplate_by_provision(cts)
    result_dict = pack_cardTemplate(cts)
    p1_d =[]
    p2_d =[]
    for key in result_dict:
        if int(result_dict[key]["PlayId"],16) == 1:
            p1_d.append(result_dict[key])
        else:
            p2_d.append(result_dict[key])
    print("#####################################")
    print("P111111")
    for list in p1_d:
        printList(list)
    print("#####################################")
    print("P2222222")
    for list in p2_d:
        printList(list)
    print(len(p2_d))
    print("#####################################")

if __name__ == "__main__":
    get_baseAddress()
    # 获得Card
    cardsAdd = cardDao.getAllCardsByGI(gi)
    cts = []
    cardDict = getCardDataJsonDict()
    # print("#######################################")
    # 实例化CardTemplate和Card,并建立关系
    for cardAdd in cardsAdd:
        cardTemplate = cardDao.getCardTemplateByCard(cardAdd)
        ct_dict = initCtData(pm,cardTemplate,cardAdd)
        cts.append(ct_dict)
    sort_cardTemplate_by_provision(cts)
    result_dict = pack_cardTemplate(cts)
    p1_d =[]
    p2_d =[]
    for key in result_dict:
        if int(result_dict[key]["PlayId"],16) == 1:
            p1_d.append(result_dict[key])
        else:
            p2_d.append(result_dict[key])
    print("#####################################")
    print("P111111")

    for list in p1_d:
        printList(list)
    print("#####################################")
    print("P2222222")
    for list in p2_d:
        printList(list)
    print(len(p2_d))
    print("#####################################")
    print("展示pool")
    print("CardManger-Add:",hex(read_multi_bytes(pm,gi+0x20,[0x70],0x8)))
    pool_add = read_multi_bytes(pm,gi+0x20,[0x70,0x38,0x10],0x8)
    # print(pool_add)
    addlist = [
        0x2687185e000,0x2687185e240,0x2687185e480,0x2687185e900,0x2687185ed80,0x26871855000,0x26871855480,0x26871855b40
    ]
    cts = []
    print("Pool_ADD",hex(pool_add))
    num = read_int64(pm,pool_add+0x18,[])

    # print(num)
    for i in range(0,num):
        # temp_card_add = addlist[i]
        temp_card_add = pool_add + 0x20 +0x8 * i
        value = read_int64(pm,temp_card_add,[])
        # print(hex(temp_card_add),hex(value))
        if value != 0x0:
            cardTemplate = cardDao.getCardTemplateByCard(value)
            if cardTemplate != 0:
                ct_dict = initCtData(pm,cardTemplate,value)
                cts.append(ct_dict)
            else:
                print(cardTemplate)

    sort_cardTemplate_by_provision(cts)
    result_dict = pack_cardTemplate(cts)
    for key in result_dict:
        printList(result_dict[key])

        # if result_dict[key]["PlayId"] == "0x2":
        #     printList(result_dict[key])

    # print("####################")
    # getOwnerPlayerId()
    # print("####################")
    
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
            # 0x38(4) id       # 暂时无用
            # 0x3c(1) playerId # 【有用】
            # 0x3d(1) canAutoDestroy # 暂时无用
            # 0x3e(1) expired   # 暂时无用
            # 0x3f(1) canCancel # 暂时无用
            
            # 根据0x0 判别对象
            objDetailedInfo = read_int64(pm,actionObjAdd+0x0,[])
            typeName = read_Type_Name(pm,objDetailedInfo)
            if typeName != ActionName.REQUEST_CARD_CHOICES_ACTION.value:
                continue
                print("未检测到RequestCardChoicesAction事件!",typeName)
            id = read_memory_bytes(pm,actionObjAdd+0x38,0x4)
            playerId = read_memory_bytes(pm,actionObjAdd+0x3c,0x1)
            canAutoDestroy = read_memory_bytes(pm,actionObjAdd+0x3d,0x1)
            expired = read_memory_bytes(pm,actionObjAdd+0x3E,0x1)
            canCancel = read_memory_bytes(pm,actionObjAdd+0x3f,0x1)
            requestId = read_memory_bytes(pm,actionObjAdd+0x40,0x2)
            print("ARequestActionAdd:")
            print("playerId:{1}".
            format(id,playerId,canAutoDestroy,expired,canCancel,hex(actionObjAdd)))

            ##########################
            # 0x40(2) RequestId     # 暂时无用
            # 0x42(1) ERequestChoiceType # 【有用】
            # 0x44(4) MinChoices    # 暂时无用
            # 0x48(4) MaxChoices    # 暂时无用
            # 0x4c(1) proceedWithZeroChoice # 暂时无用
            # 0x4d(1) revealChoices # 暂时无用
            # 0x50(8) originalValidChoices #多人没用
            # 0x58(8) validChoices
            requestId = read_memory_bytes(pm,actionObjAdd+0x40,0x2)
            eRequestChoiceType = read_memory_bytes(pm,actionObjAdd+0x42,0x1)
            minChoice = read_memory_bytes(pm,actionObjAdd+0x44,0x4)
            maxChoice = read_memory_bytes(pm,actionObjAdd+0x48,0x4)
            proceedWithZeroChoice = read_memory_bytes(pm,actionObjAdd+0x4c,0x1)
            revealChoices = read_memory_bytes(pm,actionObjAdd+0x4d,0x1)
            print(ChoiceType(eRequestChoiceType))
            # print("requestId:{0},minChoice:{2},maxChoice:{3},canZeroChoice:{4},revealChoices:{5}".
            # format(id,ChoiceType(eRequestChoiceType),minChoice,maxChoice,proceedWithZeroChoice,revealChoices))
            originalValidChoices = read_memory_bytes(pm,actionObjAdd+0x50,0x8)
            validChoices = read_memory_bytes(pm,actionObjAdd+0x58,0x8)
            print("validChoices",hex(validChoices))
            cardListToString(validChoices)

 
    
    
