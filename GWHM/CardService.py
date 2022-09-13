from CardDao import *
from Bean.CardTemplate import CardTemplate
from Bean.Card import Card
import pymem
from FileTool import *

def get_all_cardTemplates():
    
    cardsAdd = cardDao.getAllCardsByGI(gi)
    cardObjs = []
    cts = []
    # 实例化CardTemplate和Card,并建立关系
    for cardAdd in cardsAdd:
        cardTemplate = cardDao.getCardTemplateByCard(cardAdd)
        ct = initCardTemplate(cardTemplate)

        cardObj = Card()
        fillObjAttr(cardObj,cardAdd)
        cardObj.cardTemplate = ct
        cardObj._baseAddress = cardAdd
        ct._card = cardObj
        ct._baseAddress = cardTemplate

        cardObjs.append(cardObj)
        cts.append(ct)

    return cts

def sort_cardTemplate_by_provision(cts):
    #按照provision,id降序排序卡组
    for i in range(len(cts)-1):
        for j in range(len(cts) - i - 1):
            if cts[j].provision < cts[j + 1].provision:
                cts[j],cts[j+1] = cts[j+1],cts[j]
            elif cts[j].provision == cts[j + 1].provision:
                if cts[j].id > cts[j + 1].id:
                    cts[j],cts[j+1] = cts[j+1],cts[j]

def sort_cardTemplate_by_index(cts):
    #按照index升序排序卡组
    for i in range(len(cts)-1):
        for j in range(len(cts) - i - 1):
            if cts[j].card.position_index > cts[j + 1].card.position_index:
                cts[j],cts[j+1] = cts[j+1],cts[j]

def remove_card_by_playerId(playerId,cts):
    results = []
    for ct in cts:
        if ct.card.position_playerId == playerId:
            results.append(ct)
    return results

def filter_cardTemplate_by_location(location,cts):
    # 保留Location的牌
    results = []
    for ct in cts:
        if ct.card.position_location == location.value:
            results.append(ct)
    return results

def get_my_deck_cards(location,playerId):
    # 对象化的数据源
    cts = get_all_cardTemplates()
    #按照provision,id降序排序卡组
    sort_cardTemplate_by_provision(cts)
    # 去除AI的卡组
    cts = remove_card_by_playerId(playerId,cts)
    #按照index升序排序卡组
    sort_cardTemplate_by_index(cts)
    # 保留Location的牌
    cts = filter_cardTemplate_by_location(location,cts)
    # 封装为返回类型
    result_list = pack_cardTemplate(cts)
    return result_list

def get_my_all_cards(playerId):
    # 对象化的数据源
    cts = get_all_cardTemplates()
    #按照provision,id降序排序卡组
    sort_cardTemplate_by_provision(cts)
    # 去除AI的卡组
    cts = remove_card_by_playerId(playerId,cts)
    #按照index升序排序卡组
    sort_cardTemplate_by_index(cts)
    # 封装为返回类型
    result_dict = pack_cardTemplate(cts)
    return result_dict

# 将ct对象集封装为dict格式的对象,主键为card实例化的id
def pack_cardTemplate(cts):
    cardDict = getCardDataJsonDict()
    # 装载结果
    count = 0 
    result_dict = {}
    for ct in cts:
        count += 1
        if ct.id != 0 and ct.card.id !=0 : 
            temp_dict = {}
            temp_dict["Id"]=ct.id
            temp_dict["Name"]=cardDict[str(ct.id)]['name']
            temp_dict["FactionId"]=ct.factionId
            temp_dict["Rarity"]=ct.rarity
            temp_dict["Provision"]=ct.provision
            temp_dict["PlayId"]=hex(ct.card.position_playerId)
            temp_dict["Location"]=hex(ct.card.position_location)
            temp_dict["Index"]=hex(ct.card.position_index)
            temp_dict["Address"]=hex(ct.card._baseAddress)
            result_dict[ct.card.id]=temp_dict
    return result_dict

def initCardTemplate(cardTemplateAdd):
    ct = CardTemplate()
    fillObjAttr(ct,cardTemplateAdd)
    return ct
    
def fillObjAttr(obj,base):
    attrList = list(obj.__dict__.keys())
    attrValueList = list(obj.__dict__.values())
    for i in range(0,len(attrList)):
        attr = attrList[i]
        value = attrValueList[i]
        if i == 0 :
            will_set_value = read_memory_bytes(pm,base+value,0x8)
            setattr(obj,attr,will_set_value)
        else :
            length = value-attrValueList[i-1]
            will_set_value = read_memory_bytes(pm,base+value,length)
            setattr(obj,attr,will_set_value)
        # print(attr[1:],":",hex(will_set_value))
        # break

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
    cardDao = CardDao(pm,baseAddress)
    global gi
    gi = cardDao.getGameInstance()

if __name__ =='__main__':
    main()