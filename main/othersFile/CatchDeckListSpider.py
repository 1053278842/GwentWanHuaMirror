import json
import random
from multiprocessing import Pool

import requests


# 获取指定日期后的所有卡组
def getDeckIdsByDate(header,date):
    url = "https://www.playgwent.com/en/decks/api/guides/offset/0000/limit/500"
    response=requests.get(url=url,headers=header)
    req_json = response.json()
    result_deckIds = []
    count = 0
    for deck_info in req_json['guides']:
        if deck_info["createdAt"] > date:
            count += 1
            result_deckIds.append(deck_info["id"])
            if count>10:
                # pass
                break
    return result_deckIds

def getDeckInfoByDeckId(deckId):
    user_agent_list = ["Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0;) Gecko/20100101 Firefox/61.0",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36+\
                    (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400",
                    ]
    headers={}
    headers['User-Agent'] = random.choice(user_agent_list)
    deckId = deckId
    url="https://www.playgwent.com/en/decks/api/guides/"+str(deckId)
    response=requests.get(url=url,headers=headers)
    # print(response.text)
    req_json = response.json()
    temp_deck_info = {"sortedCtIds":[],}
    # 排序过的cards
    # 排序过的cards有两种存储
    # 1: ctId列表   2:字典
    if(isinstance(req_json["deck"]["srcCardTemplates"],dict)):
        for key,value in req_json["deck"]["srcCardTemplates"].items():
            temp_deck_info["sortedCtIds"].append(value)
    else:
        for cardTemplateId in req_json["deck"]["srcCardTemplates"]:
            temp_deck_info["sortedCtIds"].append(cardTemplateId)
    # leader
    temp_deck_info["leaderCtId"] = req_json["leaderId"]
    # stratagem
    temp_deck_info["stratagemCtId"] = req_json["stratagem"]["id"]
    # time
    temp_deck_info["time"] = req_json["modified"]
    # deckName
    temp_deck_info["deckName"] = req_json["name"]
    # deckAuthor
    temp_deck_info["deckAuthor"] = req_json["author"]
    # factionName
    temp_deck_info["deckId"] = req_json["id"]
    factionName = req_json["faction"]["slug"]
    factionId = 0
    if factionName == "monsters":
        factionId = 2
    elif factionName == "nilfgaard":
        factionId = 4
    elif factionName == "northernrealms":
        factionId = 8
    elif factionName == "scoiatael":
        factionId = 16
    elif factionName == "skellige":
        factionId = 32
    elif factionName == "syndicate":
        factionId = 64
    temp_deck_info["factionId"] = factionId
    print(temp_deck_info)
    return temp_deck_info

if __name__=="__main__":
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36+\
            (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400",
        "Content-Type": "application/json; charset=UTF-8"
    }
    requests.adapters.DEFAULT_RETRIES = 5
    # 开始日期,爬取的卡组从该日期往后开始！
    date = "2022-10-01T00:00:00+00:00"
    deckIds = getDeckIdsByDate(headers,date)
    print("新版本卡组库有效数量:",len(deckIds))
    # ----------------------------------------------------------------
    result_deckInfos = [int(x) for x in deckIds]
    pool = Pool(5)
    result = pool.map(getDeckInfoByDeckId,result_deckInfos)
    # for di in deckIds:
    #     break
    #     result_deckInfos.append(getDeckInfoByDeckId(int(di)))

    #保存
    fp=open("main/resources/data/decks.json","w",encoding="utf-32")
    print(json.dump(result,fp=fp,ensure_ascii=False))


    
