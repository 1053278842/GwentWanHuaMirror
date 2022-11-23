import tkinter as tk
import tkinter.font as tkFont
from tkinter import ALL, EventType, PhotoImage, ttk

import tools.FileTool as ft
from enums.GwentEnum import *
from PIL import Image, ImageFont, ImageTk
from tools.decorators import *


### 卡组状态区域 ########
class status_board(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root =root

        # 向 bottom 借的高度
        yOffset = self.root.TOP_HEIGHT * 0.15
        self.can_size= [self.root.WIN_WIDTH,self.root.TOP_HEIGHT * 0.20 + yOffset ]
        # 背景宽高
        self.bg_size  = [self.can_size[0]*0.86,self.can_size[1]*0.85]
        self.bg_pad   = [self.can_size[0]*0.07,self.can_size[1]*0.1]

        # TODO RESIZE 20要和高度关联
        self.canvas_padding = [ self.can_size[0]*0.07,20]
        self.icon_x_padding = ( self.root.WIN_WIDTH - self.canvas_padding[0] * 2 ) /2 - round(self.root.WIN_WIDTH*0.12)

        self.ICO_SIZE = (33,36)
        self.scale_factor = self.root.WIN_WIDTH/8.2/self.ICO_SIZE[0]
        self.create_page()

    def getHeight(self):
        return self.can_size[1]

    def create_page(self):
        self.can_bg = tk.Canvas(self,bg='#000000',width = self.can_size[0],height = self.can_size[1],highlightthickness=0,highlightcolor="green")

        # 背景
        self.panel = ft.get_imgTk_xy(r"main/resources/images/deck_preview/frame-status.png",x=self.bg_size[0],y=self.bg_size[1])
        self.can_bg.create_image(self.bg_pad[0],self.bg_pad[1], anchor='nw' , image = self.panel)

        self.i_total     = ft.get_img_resized(r"main/resources/images/deck_preview/cards-icon.png",    self.scale_factor)
        self.i_unit      = ft.get_img_resized(r"main/resources/images/deck_preview/helmet-icon.png",   self.scale_factor)
        self.i_provision = ft.get_img_resized(r"main/resources/images/deck_preview/provision-icon.png",self.scale_factor)

        leftPad = self.canvas_padding[0] + self.bg_size[0]*0.03
        # top偏移 = + 缩放后图片高
        # self.topPad  = self.canvas_padding[1]+self.ICO_SIZE[1]*self.scale_factor
        self.topPad  = self.bg_size[1]/2+self.bg_pad[1]
        xOffset = self.bg_size[0]*0.34


        self.iCoordDict = {"total":leftPad + xOffset * 0,"unit":leftPad + xOffset * 1 ,"provision":leftPad + xOffset * 2 }
        self.can_bg.create_image(self.iCoordDict["total"]     , self.topPad , anchor='w' , image = self.i_total)
        self.can_bg.create_image(self.iCoordDict["unit"]      , self.topPad , anchor='w' , image = self.i_unit)
        self.can_bg.create_image(self.iCoordDict["provision"] , self.topPad , anchor='w' , image = self.i_provision)
        
        # 图片实际宽度+图片实际宽度的百分比
        self.offset = (self.ICO_SIZE[0]*self.scale_factor+self.ICO_SIZE[0]*self.scale_factor*0.05
        ,Image.open(r"main/resources/images/deck_preview/cards-icon.png").size[1])
        # 数字
        self.t_total =      self.get_text_img(size=(25,30),color=(213,215,213),name="25")
        self.t_unit =       self.get_text_img(size=(25,30),color=(213,215,213),name="13")
        self.t_provision =  self.get_text_img(size=(45,30),color=(213,215,213),name="166")
        self.t_total_id = self.can_bg.create_image(self.iCoordDict["total"]    +self.offset[0], self.topPad,anchor='w',image=self.t_total)
        self.t_unit_id = self.can_bg.create_image(self.iCoordDict["unit"]     +self.offset[0] , self.topPad,anchor='w',image=self.t_unit)
        self.t_provision_id = self.can_bg.create_image(self.iCoordDict["provision"]+self.offset[0], self.topPad,anchor='w',image=self.t_provision)
        # 线
        
        # self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.05,
        # self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.05,fill = "#261a13",width=2)
        # self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.08,
        # self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.08,fill = "#5e4637",width=1)

        self.can_bg.create_line(self.bg_size[0]*0.4, self.bg_size[1]*0.4,
        self.bg_size[0]*0.4, self.bg_size[1]*0.8,fill = "#d9d8cb",width=round(self.root.WIN_WIDTH/150))
        self.can_bg.create_line(self.bg_size[0]*0.74, self.bg_size[1]*0.4,
        self.bg_size[0]*0.74, self.bg_size[1]*0.8,fill = "#d9d8cb",width=round(self.root.WIN_WIDTH/150))


        self.can_bg.pack()

        self.can_bg.bind('<Enter>',self.hover_bg)
        self.can_bg.bind('<Leave>',self.leave_bg)
    
    def hover_bg(self,event):
        self.root.responseManager.showHighlightStatusData()

    def leave_bg(self,event):
        self.root.responseManager.hideHighlightStatusData()
    
    def get_text_img(self,size,color,name):
        img = ft.get_num_img(size,color,name)
        x,y = img.size
        scale_factor = self.bg_size[1]/y*0.50
        out = img.resize((int(x*scale_factor),int(y*scale_factor)),Image.Resampling.LANCZOS) 
        imgTk = ImageTk.PhotoImage(out)
        return imgTk

    def update_data(self,total,unit,provision,highlight = False):
        # 颜色
        color = ()
        if highlight:
            color = (250,208,95)
        else:
            color = (213,215,213)
        # 数字
        self.can_bg.delete(self.t_total_id)
        self.t_total =      self.get_text_img(size=(22,27),color=color,name=str(total))
        self.t_total_id = self.can_bg.create_image(self.iCoordDict["total"]    +self.offset[0], self.topPad,anchor='w',image=self.t_total)

        self.can_bg.delete(self.t_unit_id)
        self.t_unit =       self.get_text_img(size=(22,27),color=color,name=str(unit))
        self.t_unit_id = self.can_bg.create_image(self.iCoordDict["unit"]     +self.offset[0], self.topPad,anchor='w',image=self.t_unit)

        self.can_bg.delete(self.t_provision_id)
        self.t_provision =  self.get_text_img(size=(33,27),color=color,name=str(provision))
        self.t_provision_id = self.can_bg.create_image(self.iCoordDict["provision"]+self.offset[0], self.topPad,anchor='w',image=self.t_provision)

####################################################################################################################