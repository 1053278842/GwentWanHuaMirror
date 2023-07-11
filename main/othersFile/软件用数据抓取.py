import json
import math
import os
import sys
from multiprocessing import Pool

import requests

os.path.join(os.path.dirname(__file__), '../')
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from tools import FileTool as ft


def writeCardInfoJson(headers):
    cn_map = ft.getCardDataJsonDict()
    url="https://www.playgwent.com/en/decks/builder/api/search?&faction=0,1,2,3,4,5,6&limit=100&offset=0"
    response=requests.get(url=url,headers=headers)
    req_json = response.json()
    all_cardInfos_dict = cn_map
    for cardInfo in req_json:
        ctId = cardInfo["_id"]
        factionId = cardInfo["_source"]["faction"]
        rarity_web = cardInfo["_source"]["rarity"]
        provision = cardInfo["_source"]["provisions_cost"]
        cardType = cardInfo["_source"]["type"]
        power = cardInfo["_source"]["power"]
        factionId = int(math.pow(2,int(factionId)))
        
        rarity = 1
        if rarity_web == 25:
            rarity = 8
        elif rarity_web == 20:
            rarity = 4
        elif rarity_web == 15:
            rarity = 22
        all_cardInfos_dict[ctId]["factionId"]=factionId
        all_cardInfos_dict[ctId]["rarity"]=rarity
        all_cardInfos_dict[ctId]["provision"]=provision
        all_cardInfos_dict[ctId]["cardType"]=cardType
        all_cardInfos_dict[ctId]["power"]=power
    
    leaderJson = ft.getLeaderCardDataJsonDict()
    for key,value in leaderJson.items():
        all_cardInfos_dict[key] = value
        # all_cardInfos_dict["power"] = 0


    with open(r'main/resources/config/card_json.json', 'w',encoding='utf-8') as write_f:
        write_f.write(json.dumps(all_cardInfos_dict,indent=4,ensure_ascii=False))

def getDriverCardInfo(ctId):
    result={}
    result[str(ctId)] = all_cardInfos_dict[str(ctId)]
    url="https://www.playgwent.com/en/decks/builder/api/search?id="+str(ctId)
    response=requests.get(url=url,headers=headers)
    print("t:",response)
    req_json = response.json()
    response.close()
    for cardInfo in req_json:
        ctId = cardInfo["_id"]
        factionId = cardInfo["_source"]["faction"]
        rarity_web = cardInfo["_source"]["rarity"]
        provision = cardInfo["_source"]["provisions_cost"]
        cardType = cardInfo["_source"]["type"]
        power = cardInfo["_source"]["power"]
        factionId = int(math.pow(2,int(factionId)))
        
        rarity = 1
        if rarity_web == 25:
            rarity = 8
        elif rarity_web == 20:
            rarity = 4
        elif rarity_web == 15:
            rarity = 22
        result[ctId]["factionId"]=factionId
        result[ctId]["rarity"]=rarity
        result[ctId]["provision"]=provision
        result[ctId]["cardType"]=cardType
        result[ctId]["power"]=power
    print(result)
    return result

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
}
cn_map = ft.getCardDataJsonDict16()
all_cardInfos_dict = cn_map

if __name__=="__main__":


    cardDict = open("main/resources/config/card_json.json", "r",encoding="utf-8")
    card_list = json.loads(cardDict.read())


    # writeCardInfoJson(headers)
    # 分析衍生卡
    deriveCards = {}
    for key,value in cn_map.items():
        if len(value.keys()) < 8:
            deriveCards[key] = value
    driverCardIds = [ int(ctId) for ctId in deriveCards.keys()]
    print(driverCardIds)
    pool = Pool(4)
    result = {}
    result = pool.map(getDriverCardInfo, driverCardIds)
    result_dict = {}

    for card in result:
        for key,value in card.items():
            all_cardInfos_dict[key] = value

    with open(r'main/resources/config/card_json.json', 'w',encoding='utf-8') as write_f:
        write_f.write(json.dumps(all_cardInfos_dict,indent=4,ensure_ascii=False))