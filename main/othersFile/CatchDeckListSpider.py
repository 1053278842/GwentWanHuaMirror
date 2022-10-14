import json
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
            if count>50:
                # pass
                break
    return result_deckIds

def getDeckInfoByDeckId(deckId):
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
    temp_deck_info["factionName"] = req_json["faction"]["slug"]
    temp_deck_info["deckId"] = req_json["id"]
    print(temp_deck_info)
    return temp_deck_info

if __name__=="__main__":
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36+\
            (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400",
        "Content-Type": "application/json; charset=UTF-8"
    }
    # 开始日期,爬取的卡组从该日期往后开始！
    date = "2022-10-01T00:00:00+00:00"
    deckIds = getDeckIdsByDate(headers,date)
    print("新版本卡组库有效数量:",len(deckIds))
    # ----------------------------------------------------------------
    result_deckInfos = []
    for di in deckIds:
        result_deckInfos.append(getDeckInfoByDeckId(int(di)))

    #保存
    fp=open("main/resources/data/decks.json","w",encoding="utf-8")
    print(json.dump(result_deckInfos,fp=fp,ensure_ascii=False))


    
