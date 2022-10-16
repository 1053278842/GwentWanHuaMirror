import copy
import tkinter as tk
import tkinter.font as tkFont
from tkinter import ALL, EventType, PhotoImage, ttk

import tools.FileTool as ft
from enums.GwentEnum import *
from PIL import Image, ImageFont, ImageTk
from tools.decorators import *


# 图片背景 #
class bg_img(tk.Canvas):
    def __init__(self, root):
        super().__init__(root)
        self.window =root

        # 图片大小 
        BG_WIDTH = 564

        # 背景缩放比
        self.scale_factor = int(self.window.WIN_WIDTH)/BG_WIDTH

        self.create_page()

    
    def create_page(self):
        self.can_bg = tk.Canvas(self.window,bg="#000000",highlightthickness=0,cursor="fleur")
        self.window.update()
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()
        
        
        self.p_top = ft.get_img_resized(r"main/resources/images/deck_preview/deck_bg_top_j.png",self.scale_factor)
        self.p_mid = ft.get_img_resized(r"main/resources/images/deck_preview/deck_bg_mid_j.png",self.scale_factor)
        self.p_end = ft.get_img_resized(r"main/resources/images/deck_preview/deck_bg_end_j.png",self.scale_factor)

        self.window.TOP_HEIGHT = ImageTk.getimage(self.p_top).size[1]
        self.window.BOTTOM_HEIGHT = ImageTk.getimage(self.p_end).size[1]
        # self.window.WIN_WIDTH = ImageTk.getimage(self.p_end).size[0]
        self.window.MID_HEIGHT = self.window_height-self.window.TOP_HEIGHT-self.window.BOTTOM_HEIGHT

        self.can_bg.create_image(0,0,anchor='nw',image=self.p_top,tag=("bg_top","bg"))
        self.can_bg.create_image(0,self.window.TOP_HEIGHT,anchor='nw',image=self.p_mid,tag=("bg_mid","bg"))
        self.c_end = self.can_bg.create_image(0,self.window_height-self.window.BOTTOM_HEIGHT,anchor='nw',image=self.p_end,tag=("bg_end","bg"))


        self.window_width -= 1
        # 注册（绑定）窗口变动事件
        self.window.bind('<Configure>', self.window_resize)
        self.can_bg.pack(expand=True,fill=tk.BOTH)

    def window_resize(self,event=None):
        if event != None:
            if self.window_width != self.window.winfo_width() or self.window_height != self.window.winfo_height():
                # print(len(self.can_bg.find_withtag("bg")),self.window.winfo_width()/338)
                # self.temp = ImageTk.getimage(self.p_top).resize((50, 50), Image.ANTIALIAS)
                # self.can_bg.itemconfig(1, image= ImageTk.PhotoImage(self.temp))
                

                if self.window_width != self.window.winfo_width():
                    self.window_width = self.window.winfo_width()
                if self.window_height != self.window.winfo_height():
                    self.window_height = self.window.winfo_height()
                # self.window.WIN_WIDTH = self.window.winfo_width()
                self.load_image()

    # TODO BUG 这里实例化图片资源密集型创建，改为提前创建！或者直接缩放
    def load_image(self):
        # return 0
        self.can_bg.coords(self.c_end,0,self.window_height-self.window.BOTTOM_HEIGHT)
        img = Image.open(r"main/resources/images/deck_preview/deck_bg_mid_j.png")
        scale = self.scale_factor
        y_scale = (self.window_height-self.window.TOP_HEIGHT-self.window.BOTTOM_HEIGHT)/(img.size[1]*scale)
        out = img.resize((self.window_width,int(img.size[1]*y_scale*scale)),Image.Resampling.LANCZOS)
        panel = tk.Label(master = self.window)
        panel.photo = ImageTk.PhotoImage(out)
        self.can_bg.itemconfig(2, image = panel.photo)
        # 修改MID高度
        self.window.MID_HEIGHT = out.size[1]