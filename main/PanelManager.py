import tkinter as tk

import bean.global_var as global_var
import GwentMirror
import pymem
import services.CardService as cs
from enums.GameEnum import *
from GwentGUI import GwentGUI
from LoadingAnimGUI import AnimatedGif
from RequestManager import RequestManager


class PanelManager():
    def __init__(self,root):
        #检查进程是否启动
        if not self.checkProgramIsRunning():
            GwentMirror.tips_show("警告","检测到游戏未启动!")
            GwentMirror.destroy()
        else:
            GwentMirror.show()

        cs.main()
        
        self.root = root
        self.opponentPanel = None
        self.ourPanel = None

        # 对象
        self.reqManager = RequestManager(self.ourPanel)
        # Loop状态
        self.ourPanelSearching = False
        self.oppPanelSearching = False
        # request 状态
        self.sentRequest = False
        # 游戏的状态
        self.runningProcess = False
        self.existingGI = False
        self.runningBattle = False
        self.checkGwentStatusLoop()
        self.checkGameEndedLoop()
        self.checkGameRunningLoop()

        #
        global_var.set_value("isActive",False)

    # 维护游戏的运行状态
    def checkGwentStatusLoop(self):
        cs.refreshGI()
        self.checkGwentStatus()
        self.root.after(1000,self.checkGwentStatusLoop)
    def checkGwentStatus(self):
        self.runningProcess = self.checkProgramIsRunning()
        if self.runningProcess:
            self.existingGI = cs.isExistGameInstance()
            if self.existingGI:
                self.runningBattle = cs.getGameStatus() != EGameStatus.ENDED and cs.getGameStatus() != EGameStatus.ENDING
            else:
                self.existingGI = False
                self.runningBattle = False
        else:
            self.runningProcess = False
            self.existingGI = False
            self.runningBattle = False
        
    # 检查游戏进程是否启动
    def checkProgramIsRunning(self):
        try:
            pm = pymem.Pymem("Gwent.exe")
            pymem.process.module_from_name(
                pm.process_handle,"GameAssembly.dll"
            ).lpBaseOfDll
        except Exception:
            print("启动失败，请检查启动游戏是否启动!")
            return False
        return True
    
    def asyncOurPanel(self,coords):
        if self.existingGI and self.runningBattle:   
            if self.ourPanel == None:         
                self.root.after_cancel(self.asyncOurPanel)
                self.ourPanelSearching = False
                global_var.get_value("panel_root").ourCbTextVar.set("关 闭")
                self.ourPanel = tk.Toplevel()
                GwentGUI(self.ourPanel,coords,isEnemy=False)
                global_var.set_value("isActive",True)
                self.ourPanel.mainloop()
        else:
            global_var.get_value("panel_root").ourCbTextVar.set("关 闭 (检索中...)")
            if self.ourPanelSearching:
                self.ourPanelSearching = True
                self.root.after(600,self.asyncOurPanel,coords)

    def openOurPanel(self,root,coords):
        # 前提：process已经启动
            # gi存在且runningBattle -> 生成
            # gi存在not runningBattle -> 等待生成
            # gi不存在 -> 等待生成
        # process 不存在，报错tips
        if self.runningProcess:
            self.ourPanelSearching = True
            self.asyncOurPanel(coords)
        else:
            GwentMirror.tips_no_gwent()

    def closeOurPanel(self):
        if self.ourPanel != None:
            self.ourPanel.destroy()
            self.ourPanel = None
        self.ourPanelSearching = False
        self.root.after_cancel(self.asyncOurPanel)

    # ----------------------------------------------------------------
    # 敌人的窗口
    def asyncOppPanel(self,coords):
        if self.existingGI and self.runningBattle:
            if self.opponentPanel == None:
                self.root.after_cancel(self.asyncOppPanel)
                self.oppPanelSearching = False
                global_var.get_value("panel_root").oppCbTextVar.set("关 闭")
                self.opponentPanel = tk.Toplevel()
                GwentGUI(self.opponentPanel,coords,isEnemy=True)
                global_var.set_value("isActive",True)
                self.opponentPanel.mainloop()
        else:
            global_var.get_value("panel_root").oppCbTextVar.set("关 闭 (检测中...)")
            if self.oppPanelSearching:
                self.oppPanelSearching = True
                self.root.after(400,self.asyncOppPanel,coords)

    def openOpponentPanel(self,root,coords):
        if self.runningProcess:
            self.oppPanelSearching = True
            self.asyncOppPanel(coords)
        else:
            GwentMirror.tips_no_gwent()
        
    def closeOpponentPanel(self):
        if self.opponentPanel != None:
            self.opponentPanel.destroy()
            self.opponentPanel = None
        self.oppPanelSearching = False
        self.root.after_cancel(self.asyncOppPanel)
    
    # # 该函数要在游戏启动、gameInstance可以检测到后运行
    def checkGameEndedLoop(self):
        if self.runningProcess and self.existingGI:
            if not self.runningBattle:
                self.closeOurPanel()
                self.closeOpponentPanel()
                if not self.sentRequest:
                    self.sentRequest = True
                    battleInfo = cs.getBattleInfo()
                    self.reqManager.sendBattleInfo(battleInfo)
            else:
                self.sentRequest = False
        self.root.after(1000,self.checkGameEndedLoop)
    
    def checkGameRunningLoop(self):
        # 第一前提:存在该游戏进程
        if self.runningProcess:
            # 第二前提: 玩家处于战斗之外,还未进入牌局游戏
            if not self.existingGI:
                # 第三前提,按钮已经是按下状态
                ourButtonPressed = int(global_var.get_value("panel_root").ourPlayerCBVar.get())
                oppButtonPressed = int(global_var.get_value("panel_root").opponentPlayerCBVar.get())
                if ourButtonPressed == 1:
                    if not self.ourPanelSearching:
                        GwentMirror.toggleOurCardPanel()
                else:
                    global_var.get_value("panel_root").ourCbTextVar.set("开 启")
                if oppButtonPressed == 1:
                    if not self.oppPanelSearching:
                        GwentMirror.toggleOpponentCardPanel()
                else:
                    global_var.get_value("panel_root").oppCbTextVar.set("开 启")
        self.root.after(1000,self.checkGameRunningLoop)

    # loop 循环函数
    # runningProcess and isExistGameInstance and runningBattle == ENDED
    #   core:sent()
    #   isSent = False
    # else runningBattle != ENDED or ENDING:
    #   isSent = True


