import json
import tkinter as tk

import bean.global_var as global_var
import GwentMirror
import pymem
import requests
import services.CardService as cs
import tools.FileTool as FT
from enums.GameEnum import *
from LoadingAnimGUI import AnimatedGif


class RequestManager():
    def __init__(self,our_root=None):
        self.root = our_root
        global_config = FT.getGlobalConfig()
        self.url = global_config["url"]
        self.headers={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36+\
                (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3766.400 QQBrowser/10.6.4163.400",
            "Content-Type": "application/json; charset=UTF-8"
        }


    def sendBattleInfo(self,battleInfo):
        print("winnerId:{0}|player1_name:{1}|player2_name{2}".format(
        battleInfo["winner_playId"],battleInfo["players"][0]["player_name"],
        battleInfo["players"][1]["player_name"]))
        # 暂时不做游戏结束原因 中掉线、超时 等数据的筛选 TODO 需测试
        # 防止意外调用

        gameStatus = battleInfo["GameStatus"]
        if EGameStatus(gameStatus) == EGameStatus.RUNNING or EGameStatus(gameStatus) == EGameStatus.UNINIT:
            return
        gameMode = battleInfo["GameMode"] 
        # pva、观众的情况下过滤
        if EGameMode(gameMode) == EGameMode.SinglePlayer or EGameMode(gameMode) == EGameMode.Spectator:
            return
        battleType = battleInfo["BattleType"]
        if EBattleType(battleType) == EBattleType.Friend or EBattleType(battleType) == EBattleType.Arena or \
            EBattleType(battleType) == EBattleType.ArenaV2:
            return
        
        print("这里发送battleInfo,只有该场比赛达成一定条件你才能看到这一句！")
        self.postBattleInfo(battleInfo)
        print(battleInfo)
        # print(self.root.responseManager.cardList.carriedCards)
        # print(type(self.root.responseManager.cardList.carriedCards))

    def getDecks(self):
        url = self.url+"/deck/api/getDecks"
        response=requests.get(url=url,headers=self.headers,timeout=30)
        result = response.json()
        print("更新:本地库中将有{0}个卡组".format(len(result)))
        return result
    
    def getVersion(self):
        url = self.url+"/version/api/getId"
        response=requests.post(url=url,headers=self.headers,timeout=30)
        result = response.json()
        return result

    def postBattleInfo(self,battleInfo):
        try:
            requests.post(self.url+"/battle/api/save",json=battleInfo,headers=self.headers)
        except Exception:
            print("发送对局信息失败!")

    def updateDecks(self):
        # 检查当前decks文件的更新状态
        # 获取服务器decks表中的更新状态
        # 比较是否更新
        # 请求更新，写入到decks中
        try:
            result = self.getDecks()
            fp=open("main/resources/data/decks.json","w",encoding="utf-16")
            json.dump(result,fp=fp,ensure_ascii=False)
        except Exception:
            print("获取decks失败!未成功写入decks.json")
            pass

    def updateVersion(self):
        try:
            result = self.getVersion()
            fp=open("main/resources/config/version.json","w",encoding="utf-16")
            print(json.dump(result,fp=fp,ensure_ascii=False))
        except Exception:
            print("请求VERSION失败!未成功写入version.json")
            raise