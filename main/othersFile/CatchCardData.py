import json
import os
import sys

import requests

os.path.join(os.path.dirname(__file__), '../')
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from tools import FileTool as ft


def writeCardInfoJson(headers):
    cn_map = ft.getCardDataJsonDict()
    url="https://www.playgwent.com/en/decks/api/builder/search?&faction=0,1,2,3,4,5,6&limit=3000&offset=0"
    response=requests.get(url=url,headers=headers)
    req_json = response.json()
    all_cardInfos_dict = cn_map
    for cardInfo in req_json:
        ctId = cardInfo["_id"]
        factionId = cardInfo["_source"]["faction"]
        rarity_web = cardInfo["_source"]["rarity"]
        provision = cardInfo["_source"]["provisions_cost"]
        cardType = cardInfo["_source"]["type"]
        # en_name = cardInfo["_source"]["translations"]["en"]["name"]
        # en_fluff = cardInfo["_source"]["translations"]["en"]["fluff"]
        # en_tooltip = cardInfo["_source"]["translations"]["en"]["tooltip"]
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
        # all_cardInfos_dict[ctId]["en_name"]=en_name
        # all_cardInfos_dict[ctId]["en_fluff"]=en_fluff
        # all_cardInfos_dict[ctId]["en_tooltip"]=en_tooltip
    
    with open(r'main/resources/config/card_json.json', 'w',encoding='utf-8') as write_f:
        write_f.write(json.dumps(all_cardInfos_dict,indent=4,ensure_ascii=False))

if __name__=="__main__":
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
    }
    # 开始日期,爬取的卡组从该日期往后开始！
    # date = "2022-10-01T00:00:00+00:00"
    # deckIds = getDeckIdsByDate(headers,date)
    # print("新版本卡组库有效数量:",len(deckIds))
    # ----------------------------------------------------------------
    writeCardInfoJson(headers)

    # #保存
    # fp=open("main/resources/data/decks.json","w",encoding="utf-8")
    # print(json.dump(result_deckInfos,fp=fp,ensure_ascii=False))


    
