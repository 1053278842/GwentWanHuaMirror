import tkinter as tk
import tkinter.font as tkFont
from tkinter import ALL, EventType, PhotoImage, ttk

import services.GwentService as service
import tools.FileTool as ft
from enums.GwentEnum import *
from tools.decorators import *


### 卡组标题 ########
class title_board(tk.Frame):
    def __init__(self, root):

        super().__init__(root,bg='#436280')
        self.root =root

        # 宽高
        self.can_size = [self.root.WIN_WIDTH,self.root.TOP_HEIGHT * 0.40]
        # 颜色
        self.c_default  = "#ffffff"
        # 字体大小
        self.fontSize = round(int(self.root.WIN_WIDTH) * 0.06213)
        # 箭头缩放比
        self.scale_factor = self.root.WIN_WIDTH * 0.07988  / 123
        self.pad_x = self.can_size[0]*0.09
        self.pad_x2 = self.can_size[0]*0.83
        # end
        self.create_page()
    
    def getHeight(self):
        return self.can_size[1]

    def create_page(self):
        self.can_bg = tk.Canvas(self,bg='#436280',width = self.can_size[0],height = self.can_size[1],highlightthickness=0,highlightcolor="green")
        # 绘制字符
        # TODO RESIZE 了解字体大小和像素的关系后再定夺
        font = tkFont.Font(family='微软雅黑', size=self.fontSize, weight=tkFont.BOLD)
        self.t_all_deck_bg = self.can_bg.create_text(self.can_size[0]/2,self.can_size[1]/2,
        text=self.root.responseManager.DEFAULT_CARD_DECK_INFO.titleName,font=font,fill=self.c_default,anchor="center")
        self.can_bg.pack()
        # 绘制箭头
        self.left_arrow  = ft.get_img_resized(r"main/resources/images/deck_preview/arrow1.png",    self.scale_factor)
        self.right_arrow  = ft.get_img_resized(r"main/resources/images/deck_preview/arrow_right.png",    self.scale_factor)
        self.can_bg.create_image( self.pad_x , self.can_size[1]/2 + 3, anchor='w' , image = self.left_arrow,tags=("arrow","arrow-l"))
        self.can_bg.create_image( self.pad_x2 , self.can_size[1]/2 + 3, anchor='w' , image = self.right_arrow,tags=("arrow","arrow-r"))
        self.can_bg.tag_bind("arrow","<ButtonRelease-1>",self.click_arrow)

    
    def updateText(self,card_deck_info):
        text = card_deck_info.titleName
        self.can_bg.itemconfig(self.t_all_deck_bg,text=text)

    def click_arrow(self,event):
        if event.x < self.root.WIN_WIDTH / 2:
            #left
            self.root.responseManager.setCardListShowRelatedDeck()
        else:
            pass