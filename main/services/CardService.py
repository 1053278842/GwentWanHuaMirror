import bean.global_var as global_var
import dao.CardDao as cd
import pymem
import tools.MemoryTool as mt
from bean.BattleInfo import BattleInfo
from tools.decorators import *
from tools.decorators import get_time_consume
from tools.FileTool import *


def addStratagemCard(lackOfCards,origCards,playerId):
    stratagemCardData = {}
    for key,value in origCards.items():
        if value["Type"] == CardType.STRATAGEM.value and int(value["PlayId"],16) == playerId:
            stratagemCardData["key"] = key
            stratagemCardData["value"] = value
    if len(stratagemCardData.keys()) > 0:
        result = {}
        count = 0
        for key,value in lackOfCards.items():
            if count == 1:
                result[stratagemCardData["key"]] = stratagemCardData["value"]
            result[key] = value
            count += 1
        return result
    return lackOfCards
            

def getAddCard(newInsIds,origInsIds):
    # 刚刚减少的对象 在A里不在B里的对象
    # temp
    # for key,value in newInsIds.items():

    result_insIds = []
    for i in origInsIds:
        if i not in newInsIds:
            result_insIds.append(i)
    return result_insIds

def getRemoveCard(newInsIds,origInsIds):
    # 增加的对象     在B里不在A的对象
    result_insIds = []
    for i in newInsIds:
        if i not in origInsIds:
            result_insIds.append(i)
    return result_insIds

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

def getPlayerCarriedCarInsIds(playerId):
    ids = cardDao.getCardInsIdsWhenDeckInstance(pm,gi,playerId)
    return ids

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
    temp_sort_list = sorted(cts.items(),key=lambda x: (-x[1]["Provision"],x[1]["Id"]))
    result = {}
    for i in temp_sort_list:
        result[i[0]] = i[1]
    return result

def sort_cardTemplate_by_index(cts):
    #按照index升序排序卡组
    temp_sort_list = sorted(cts.items(),key = lambda x:(int(x[1]["Index"],16)))
    result = {}
    for i in temp_sort_list:
        result[i[0]] = i[1]
    return result 

def remove_card_by_playerId(cardDeckInfo,cts):
    results = []
    for ct in cts:
        if ct["CardId"] <= cardDeckInfo.maxCardNums and ct["CardId"] >= cardDeckInfo.minCardNums:
            results.append(ct)
    return results

# 此函数过滤会导致间谍、位移卡不能很好的记录
# 会记录到衍生卡
def removeOtherPlayerCardContainDerivation(cardDeckInfo,cts):
    results = {}
    for key,value in cts.items():
        if value["PlayId"] == hex(cardDeckInfo.playerId):
            results[key] = value
    return results

# 此函数过滤会导致衍生卡不能被记录
# 会记录到原始的卡组
def removeOtherPlayerCardNoDerivative(cardDeckInfo,cts):
    results = {}
    for key,value in cts.items():
        if value["InstanceId"] <= cardDeckInfo.maxCardNums and value["InstanceId"] >= cardDeckInfo.minCardNums:
            results[key] = value
    return results

def filter_cardTemplate_by_location(location,cts):
    # 保留Location的牌
    results = []
    for ct in cts:
        if ct["Location"] == location.value:
            results.append(ct)
    return results

# 我方指定场地、手卡等地的卡，包含衍生卡
def filterCardsByDeckCondition(cts,deckCondition):
    # # 对象化的数据源
    # cts = get_all_cardTemplates()
    # 去除AI的卡组
    cts = removeOtherPlayerCardContainDerivation(deckCondition,cts)
    if deckCondition.isSortByIndex:
        #按照index升序排序卡组
        cts = sort_cardTemplate_by_index(cts)
    else:
        #按照provision,id降序排序卡组
        cts = sort_cardTemplate_by_provision(cts)
    # filter 条件过滤
    cts = filterCardsTypeAndLocation(deckCondition,cts)
    return cts

# 不含衍生物和未知卡牌的未排序过的原始牌库中的卡
def filterCardsIntoCarriedCards(cts,deckCondition):
    cts = removeOtherPlayerCardNoDerivative(deckCondition,cts)
    # filter 条件过滤
    cts = filterCardsTypeAndLocation(deckCondition,cts,isContainHeaderCard=True)
    # 去掉未知卡
    cts = filterUnknownCard(cts)
    return cts

def getMemoryCards():
    cts = get_all_cardTemplates()
    # 封装为返回类型
    result_dict = pack_cardTemplate(cts)
    return result_dict

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

def filterUnknownCard(cts):
    results = {}
    for key,value in cts.items():
        if value["Id"] != 0:
            results[key] = value
    return results

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

def filterCardsTypeAndLocation(cardDeckInfo,cts,isContainHeaderCard=False):
    results = {}
    for key,value in cts.items():
        if isContainHeaderCard:
            if value["Type"] == CardType.LEADER.value or value["Type"] == CardType.STRATAGEM.value:
                results[key] = value
                continue
        if value["Rarity"] == cardDeckInfo.rarity.value or cardDeckInfo.rarity == Rarity.ALL:
            if value["Type"] == cardDeckInfo.cardType.value or cardDeckInfo.cardType == CardType.ALL:
                if isContainHeaderCard:
                    results[key] = value
                    continue
                if int(value["Location"],16) == cardDeckInfo.location.value or int(value["Location"],16) == cardDeckInfo.secLocation.value:
                    results[key] = value
    pass
    return results

# 将ct对象集封装为dict格式的对象,主键为card实例化的id
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
    # cardDict = getCardDataJsonDict()
    global_var.set_value("AllCardDict",getCardDataJsonDict())
    cardDict =  global_var.get_value("AllCardDict")

    global_var.set_value("LeaderCardDict",getLeaderCardDataJsonDict())
    global_var.set_value("decks",getDeckDataJsonDict())
    # cardDict =  global_var.get_value("LeaderCardDict")

# 该语句会有三种情况
# True/False/报错
def isExistGameInstance():
    # try:
    giAdd = cardDao.getGameInstance()
    typeName = cardDao.getAddTypeName(giAdd,2)
    if("GameInstance" in typeName):
        return True
    # except Exception as e:
    #     return e
        return False
    return False

if __name__ =='__main__':
    main()