import tkinter as tk

import bean.global_var as global_var
import PanelGUI
import pymem
import services.CardService as cs
from enums.GameEnum import *
from GwentGUI import GwentGUI
from LoadingAnimGUI import AnimatedGif


class RequestManager():
    def __init__(self,our_root):
        self.root = our_root
        pass

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
        #
        print("这里发送battleInfo,只有该场比赛达成一定条件你才能看到这一句！")
        # print(self.root.responseManager.cardList.carriedCards)
        # print(type(self.root.responseManager.cardList.carriedCards))
