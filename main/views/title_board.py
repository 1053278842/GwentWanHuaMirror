import tkinter as tk
from tkinter import ttk, ALL, EventType
import tools.FileTool as ft
from tools.decorators import *
import services.GwentService as service
from enums.GwentEnum import *
from tkinter import PhotoImage
import tkinter.font as tkFont
### 卡组标题 ########
class title_board(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root =root
        # 宽高
        self.can_size = [self.root.WIN_WIDTH,self.root.TOP_HEIGHT * 0.40]
        # 颜色
        self.c_default  = "#ffffff"
        # 字体大小
        self.fontSize = round(int(self.root.WIN_WIDTH) * 0.06213)
        # end
        self.create_page()
    
    def getHeight(self):
        return self.can_size[1]

    def create_page(self):
        self.can_bg = tk.Canvas(self,bg='#000000',width = self.can_size[0],height = self.can_size[1],highlightthickness=0,highlightcolor="green")
        # 绘制字符
        # TODO RESIZE 了解字体大小和像素的关系后再定夺
        font = tkFont.Font(family='微软雅黑', size=self.fontSize, weight=tkFont.BOLD)
        self.t_all_deck_bg = self.can_bg.create_text(self.can_size[0]/2,self.can_size[1]/2,
        text=self.root.responseManager.DEFAULT_CARD_DECK_INFO.titleName,font=font,fill=self.c_default,anchor="center")
        self.can_bg.pack()
    
    def updateText(self,card_deck_info):
        text = card_deck_info.titleName
        self.can_bg.itemconfig(self.t_all_deck_bg,text=text)
