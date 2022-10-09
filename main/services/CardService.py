import ctypes
import tools.MemoryTool as mt
import dao.CardDao as cd
from tools.decorators import get_time_consume
import pymem
from tools.FileTool import *
from tools.decorators import *
from bean.Bs import Bs
from bean.PS import Ps
from bean.Pi import Pi
from bean.Bd import Bd
from bean.Bss import Bss
from bean.Card import Card
from bean.Cd import Cd
from bean.BattleInfo import BattleInfo

def getCurrBattleInfo():
    battleInfo = BattleInfo()
    battleInfo.currPlayerId = cardDao.getCurrPlayerId(pm,gi)
    battleInfo.bottomPlayerId = cardDao.getBottomPlayerId(pm,gi)
    battleInfo.topPlayerId = cardDao.getTopPlayerId(pm,gi)
    battleInfo.localPlayerId = cardDao.getLocalPlayerId(pm,gi)
    return battleInfo

def getPlayerEnableActionsStatus(playerId):
    return cardDao.getPlayerEnableActionsStatus(pm,gi,playerId)

def getViewingCards():
    validChoiceCardListAdd = cardDao.getViewingCards(pm,gi)
    cts = []
    if validChoiceCardListAdd != 0:
        cts = cardDao.cardListAddToDict(pm,gi,validChoiceCardListAdd)
    result_dict = pack_cardTemplate(cts)
    return result_dict

def getDeckInfo(playerId):
    count=0
    isDefensive = False
    leaderIndex = 0
    cts = get_all_cardTemplates()
    for cardInfoDict in cts:
        if cardInfoDict["PlayId"] == playerId:
            count+=1
            if cardInfoDict["Type"] == CardType.LEADER.value:
                leaderIndex = cardInfoDict["CardId"]
        if cardInfoDict["Type"] == CardType.STRATAGEM.value:
            isDefensive = True

    totalCardNums = count
    return {"totalCardNums": totalCardNums, "isDefensive": isDefensive,"leaderIndex":leaderIndex}

def get_all_cardTemplates():
    
    cardsAdd = cardDao.getAllCardsByGI(gi)
    cts = []
    # cardDict = getCardDataJsonDict()
    # 实例化CardTemplate和Card,并建立关系
    for cardAdd in cardsAdd:
        cardTemplate = cardDao.getCardTemplateByCard(cardAdd)
        ct_dict = cardDao.initCtData(pm,cardTemplate,cardAdd)
        cts.append(ct_dict)

    return cts

def sort_cardTemplate_by_provision(cts):
    #按照provision,id降序排序卡组
    for i in range(len(cts)-1):
        for j in range(len(cts) - i - 1):
            if cts[j]["Provision"] < cts[j + 1]["Provision"]:
                cts[j],cts[j+1] = cts[j+1],cts[j]
            elif cts[j]["Provision"] == cts[j + 1]["Provision"]:
                if cts[j]["Id"] > cts[j + 1]["Id"]:
                    cts[j],cts[j+1] = cts[j+1],cts[j]

def sort_cardTemplate_by_index(cts):
    #按照index升序排序卡组
    for i in range(len(cts)-1):
        for j in range(len(cts) - i - 1):
            if cts[j]["Index"] > cts[j + 1]["Index"]:
                cts[j],cts[j+1] = cts[j+1],cts[j]

def remove_card_by_playerId(cardDeckInfo,cts):
    results = []
    for ct in cts:
        if ct["CardId"] <= cardDeckInfo.maxCardNums and ct["CardId"] >= cardDeckInfo.minCardNums:
            results.append(ct)
    return results

def filter_cardTemplate_by_location(location,cts):
    # 保留Location的牌
    results = []
    for ct in cts:
        if ct["Location"] == location.value:
            results.append(ct)
    return results

def get_my_all_cards(cardDeckInfo):
    # 对象化的数据源
    cts = get_all_cardTemplates()
    #按照provision,id降序排序卡组
    sort_cardTemplate_by_provision(cts)
    # 去除AI的卡组
    cts = remove_card_by_playerId(cardDeckInfo,cts)
    #按照index升序排序卡组
    if cardDeckInfo.isSortByIndex:
        sort_cardTemplate_by_index(cts)
    # filter 条件过滤
    cts = filterCards(cardDeckInfo,cts)
    # 封装为返回类型
    result_dict = pack_cardTemplate(cts)
    return result_dict

def filterCards(cardDeckInfo,cts):
    results = []
    for ct in cts:
        # 如果条件中任一不是all，则过滤掉Leader牌和战略牌
        if cardDeckInfo.rarity != Rarity.ALL or cardDeckInfo.cardType != CardType.ALL:
            if ct["Type"] == CardType.LEADER.value or ct["Type"] == CardType.STRATAGEM.value:
                continue
        if ct["Rarity"] == cardDeckInfo.rarity.value or cardDeckInfo.rarity == Rarity.ALL:
            if ct["Type"] == cardDeckInfo.cardType.value or cardDeckInfo.cardType == CardType.ALL:
                results.append(ct)
    return results

# 将ct对象集封装为dict格式的对象,主键为card实例化的id
# TODO cardDict的获取是IO密集型，需要改为全局变量
def pack_cardTemplate(cts):
    
    # 装载结果
    count = 0 
    result_dict = {}
    for ct in cts:
        count += 1
        temp_dict = {}
        key                     = ct["CardId"]
        temp_dict["Id"]         = ct["Id"]              # 视为templateId
        temp_dict["Name"]       = "【未知!】"
        if ct["Id"] != 0 and ct["CardId"] !=0 : 
            try:
                temp_dict["Name"]       = cardDict[str(ct["Id"])]['name']
            except Exception:
                temp_dict["Id"] = 0
                temp_dict["Name"]       = "【未更新该卡牌卡画!】"
        temp_dict["FactionId"]  = ct["FactionId"]
        temp_dict["Rarity"]     = ct["Rarity"]
        temp_dict["Provision"]  = ct["Provision"]
        temp_dict["Type"]       = ct["Type"]  
        temp_dict["PlayId"]     = hex(ct["PlayId"])
        temp_dict["Location"]   = hex(ct["Location"])
        temp_dict["Index"]      = hex(ct["Index"])
        temp_dict["Address"]    = hex(ct["Address"])
        temp_dict["FromPlayerId"]    = ct["FromPlayerId"]
        temp_dict["BasePower"]  = ct["BasePower"] 
        temp_dict["CurrPower"]  = ct["CurrPower"] 
        temp_dict["InstanceId"]  = key

        result_dict[key]=temp_dict
    return result_dict



# 获取程式模块基址
def get_baseAddress():
    global pm
    global baseAddress
    pm = pymem.Pymem("Gwent.exe")
    baseAddress = pymem.process.module_from_name(
        pm.process_handle,"GameAssembly.dll"
    ).lpBaseOfDll

def main():
    get_baseAddress()
    global cardDao
    cardDao = cd.CardDao(pm,baseAddress)
    global gi
    gi = cardDao.getGameInstance()
    global cardDict
    cardDict = getCardDataJsonDict()

if __name__ =='__main__':
    main()