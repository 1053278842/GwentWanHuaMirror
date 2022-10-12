import tkinter as tk
from bean.CardDeckTypeInfo import CardDeckTypeInfo
from ResponseManager import *
import services.GwentService as service
from enums.GwentEnum import *
from views.bg_img import bg_img
from views.card_preview_list_board import card_preview_list_board
from views.module_board import module_board
from views.status_board import status_board
from views.title_board import title_board
import win32gui
import win32con
import win32api
import sys
import os

class GwentGUI:

    def __init__(self,root,coords,isEnemy=False):
        self.root = root
        # 338*1000 最好比率
        self.root.WIN_WIDTH = coords[0]
        self.root.WIN_HEIGHT = coords[1]
        self.root.title = "Gwent Card View"
        self.root.geometry('{0}x{1}+0+0'.format(self.root.WIN_WIDTH,self.root.WIN_HEIGHT))
        if isEnemy:
            self.root.WIN_WIDTH = coords[0]
            self.root.WIN_HEIGHT = coords[1]
            self.root.geometry('{0}x{1}+400+0'.format(self.root.WIN_WIDTH,self.root.WIN_HEIGHT))
        # self.root.wm_attributes('-topmost',1)
        # root.overrideredirect(True)
        
        self.root.DECK_IMG_SCALE_FACTOR = 0.6
        self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR = 1.214
        print("倍率：",self.root.DECK_IMG_SCALE_FACTOR*self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR)

        self.root.TOP_HEIGHT = 0
        self.root.MID_HEIGHT = 0
        self.root.BOTTOM_HEIGHT = 0


        self.create_page(isEnemy)




    def create_page(self,isEnemy):
        responseManager = ResponseManager(isEnemy)
        self.root.responseManager = responseManager

        # 背景板
        self.root.bg_board = bg_img(self.root)
        # 卡组标题名
        self.root.title_board = title_board(self.root)
        # 显示模式
        self.root.module_board = module_board(self.root)
        # 卡组状态
        self.root.status_board = status_board(self.root)
        # 卡组列表显示
        self.root.card_list_board = card_preview_list_board(self.root)

        self.root.bg_board.can_bg.bind("<Button-1>",self.MouseDown)  # 按下鼠标左键绑定MouseDown函数
        self.root.bg_board.can_bg.bind("<B1-Motion>",self.MouseMove)  # 鼠标左键按住拖曳事件,3个函数都不要忘记函数写参数
        self.root.bg_board.can_bg.bind("<Double-Button-1>",self.exit)  # 双击鼠标左键，关闭窗体

        # 注册响应控制器
        responseManager.register(self.root.bg_board,self.root.title_board,self.root.module_board
                                ,self.root.status_board,self.root.card_list_board)
        self.root.responseManager = responseManager
        self.root.responseManager.startDataLoop()

        self.show_deck_img()
    
    def show_deck_img(self):
        # 透明化Frame
        # TODO 这里的y=100 是top图片的高度
        height = 0
        # deck_h = self.
        self.set_frame_coordinate(self.root.title_board,0,height,"green")

        height+=self.root.title_board.getHeight()
        self.set_frame_coordinate(self.root.module_board,0,height,"blue")

        height+=self.root.module_board.getHeight()
        self.set_frame_coordinate(self.root.status_board,0,height,"pink")

        height+=self.root.status_board.getHeight()
        self.set_frame_coordinate(self.root.card_list_board,0,height,"red")
    
    def set_frame_coordinate(self,frame_page,x,y,color):
        hwnd = frame_page.winfo_id()
        colorkey = win32api.RGB(43,62,80) #full black in COLORREF structure
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd,colorkey,255,win32con.LWA_COLORKEY)
        frame_page.config(highlightthickness=0)
        frame_page.place(x=x, y=y, anchor='nw')
        # frame_page.pack()
    

    def MouseDown(self,event): # 不要忘记写参数event
        global mouseX  # 全局变量，鼠标在窗体内的x坐标
        global mouseY  # 全局变量，鼠标在窗体内的y坐标
        mouseX=event.x  # 获取鼠标相对于窗体左上角的X坐标
        mouseY=event.y  # 获取鼠标相对于窗左上角体的Y坐标
        
    def MouseMove(self,event):
        self.root.geometry(f'+{event.x_root - mouseX}+{event.y_root - mouseY}') # 窗体移动代码
        # event.x_root 为窗体相对于屏幕左上角的X坐标
        # event.y_root 为窗体相对于屏幕左上角的Y坐标
    def exit(self,event):
        self.root.destroy()
        # restart()
    

 

