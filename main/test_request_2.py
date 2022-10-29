import json

import requests

data = {}
GwentUrl = "http://127.0.0.1:8081/version/api"
headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36+\
        (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400",
    "Content-Type": "application/json; charset=UTF-8"
}   
if __name__=="__main__":
    requests.adapters.DEFAULT_RETRIES = 5
    # ----------------------------------------------------------------

    response = requests.post(GwentUrl+"/getId",json=data,headers=headers)
    result = response.json()
    print(response.json())
    fp=open("main/resources/config/version.json","w",encoding="utf-16")
    print(json.dump(result,fp=fp,ensure_ascii=False))