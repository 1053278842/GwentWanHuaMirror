import tkinter as tk

import bean.global_var as global_var
import PanelGUI
import pymem
import services.CardService as cs
from enums.GameEnum import *
from GwentGUI import GwentGUI
from LoadingAnimGUI import AnimatedGif


class PanelManager():
    def __init__(self,root):
        cs.main()
        self.root = root
        self.opponentPanel = None
        self.ourPanel = None
        # 游戏的状态
        self.runningProcess = False
        self.existingGi = False
        self.runningBattle = False
        self.checkGwentStatus()
        #
        global_var.set_value("isActive",False)

    # 维护游戏的运行状态
    def checkGwentStatusLoop(self):
        self.checkGwentStatus()
        self.root.after(1000,self.checkGwentStatus)
    def checkGwentStatus(self):
        self.runningProcess = self.checkProgramIsRunning()
        if self.runningProcess:
            self.existingGi = cs.isExistGameInstance()
            if self.existingGi:
                self.runningBattle = cs.getGameStatus() != EGameStatus.ENDED and cs.getGameStatus() != EGameStatus.ENDING
            else:
                self.existingGi = False
                self.runningBattle = False
        else:
            self.runningProcess = False
            self.existingGi = False
            self.runningBattle = False
        
    def isExistCheck(self,root,coords,fuc):
        isRunning = self.checkProgramIsRunning()
        if not isRunning:
            PanelGUI.tips_no_gwent()
            return False
        result = True
        try:
            result = cs.isExistGameInstance()
            if cs.getGameStatus() != EGameStatus.ENDED and cs.getGameStatus() != EGameStatus.ENDING:
                pass
            else:
                return 
            if not result:
                root.after(1000,fuc,root,coords)
            else:
                return result
        except:
            root.after(1000,fuc,root,coords)
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
    
    def asyncOurPanel(self,root,coords):
        if not self.isExistCheck(root,coords,self.asyncOurPanel):
            return False
        self.checkGameEnded(root)
        global_var.get_value("panel_root").ourCbTextVar.set("关 闭")
        self.ourPanel = tk.Toplevel()
        GwentGUI(self.ourPanel,coords,isEnemy=False)
        global_var.set_value("isActive",True)
        self.ourPanel.mainloop()

    def openOurPanel(self,root,coords):
        self.ourPanel = root
        global_var.get_value("panel_root").ourCbTextVar.set("关 闭 (检索中...)")
        self.ourPanel.after(100,self.asyncOurPanel,self.ourPanel,coords)

    def closeOurPanel(self):
        if self.ourPanel == None:
            return 0
        if self.ourPanel != self.root :
            global_var.get_value("panel_root").ourCbTextVar.set("开  启")
        self.ourPanel.destroy()
        self.ourPanel.after_cancel(self.asyncOurPanel)
        self.ourPanel.after_cancel(self.isExistCheck)
        PanelGUI.closeOurButton()

    # ----------------------------------------------------------------
    # 敌人的窗口
    def asyncOppPanel(self,root,coords):
        if not self.isExistCheck(root,coords,self.asyncOppPanel):
            return False
        self.checkGameEnded(root)
        global_var.get_value("panel_root").oppCbTextVar.set("关 闭")
        self.opponentPanel = tk.Toplevel()
        GwentGUI(self.opponentPanel,coords,isEnemy=True)
        global_var.set_value("isActive",True)
        self.opponentPanel.mainloop()

    def openOpponentPanel(self,root,coords):
        self.opponentPanel = root
        global_var.get_value("panel_root").oppCbTextVar.set("关 闭 (检索中...)")
        self.opponentPanel.after(100,self.asyncOppPanel,self.opponentPanel,coords)
        
    def closeOpponentPanel(self):
        if self.opponentPanel == None:
            return 0
        if self.opponentPanel != self.root :
            global_var.get_value("panel_root").oppCbTextVar.set("开  启")
            self.opponentPanel.destroy()
        self.opponentPanel.after_cancel(self.asyncOurPanel)
        self.opponentPanel.after_cancel(self.isExistCheck)
    
    # 该函数要在游戏启动、gameInstance可以检测到后运行
    def checkGameEnded(self,root):
        gameStatus = cs.getGameStatus()
        if gameStatus == EGameStatus.ENDED:
            self.closeOurPanel()
            self.closeOpponentPanel()
            self.root.after_cancel(self.checkGameEnded)
            return
        self.root.after(1000,self.checkGameEnded,root)
    
    # def checkGameEndedLoop(self,root):
    #     gameStatus = cs.getGameStatus()
    #     if 


