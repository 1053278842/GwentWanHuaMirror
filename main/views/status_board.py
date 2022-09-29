import tkinter as tk
from tkinter import ttk, ALL, EventType
import tools.FileTool as ft
from tools.decorators import *
import services.GwentService as service
from enums.GwentEnum import *
from tkinter import PhotoImage
import tkinter.font as tkFont
from PIL import Image, ImageTk, ImageFont
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

        self.canvas_padding = [ self.can_size[0]*0.07,20]
        self.icon_x_padding = ( self.root.WIN_WIDTH - self.canvas_padding[0] * 2 ) / 2 - 40
        self.scale_factor = 1.214
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

        leftPad = self.canvas_padding[0] + 7
        self.topPad  = self.canvas_padding[1]+Image.open(r"main/resources/images/deck_preview/cards-icon.png").size[1]
        xOffset = self.icon_x_padding

        aver_x_offset = 10
        self.iCoordDict = {"total":leftPad + xOffset * 0,"unit":leftPad + xOffset * 1 + aver_x_offset,"provision":leftPad + xOffset * 2 -aver_x_offset}
        self.can_bg.create_image(self.iCoordDict["total"]     , self.topPad , anchor='sw' , image = self.i_total)
        self.can_bg.create_image(self.iCoordDict["unit"]      , self.topPad , anchor='sw' , image = self.i_unit)
        self.can_bg.create_image(self.iCoordDict["provision"] , self.topPad , anchor='sw' , image = self.i_provision)

        self.offset = (Image.open(r"main/resources/images/deck_preview/cards-icon.png").size[0]+10
        ,Image.open(r"main/resources/images/deck_preview/cards-icon.png").size[1])
        # 数字
        self.t_total =      self.get_text_img(size=(25,30),color=(213,215,213),name="25")
        self.t_unit =       self.get_text_img(size=(25,30),color=(213,215,213),name="13")
        self.t_provision =  self.get_text_img(size=(45,30),color=(213,215,213),name="166")
        self.t_total_id = self.can_bg.create_image(self.iCoordDict["total"]    +self.offset[0], self.topPad-3,anchor='sw',image=self.t_total)
        self.t_unit_id = self.can_bg.create_image(self.iCoordDict["unit"]     +self.offset[0] - 10, self.topPad-3,anchor='sw',image=self.t_unit)
        self.t_provision_id = self.can_bg.create_image(self.iCoordDict["provision"]+self.offset[0] - 5, self.topPad-3,anchor='sw',image=self.t_provision)
        # 线
        
        # self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.05,
        # self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.05,fill = "#261a13",width=2)
        # self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.08,
        # self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.08,fill = "#5e4637",width=1)

        self.can_bg.create_line(self.iCoordDict["total"]    +self.offset[0] * 2.1, self.canvas_padding[0],
        self.iCoordDict["total"]    +self.offset[0] * 2.1, self.canvas_padding[0]*2,fill = "#d9d8cb",width=2)
        self.can_bg.create_line(self.iCoordDict["unit"]    +self.offset[0] * 1.7, self.canvas_padding[0],
        self.iCoordDict["unit"]    +self.offset[0] * 1.7, self.canvas_padding[0]*2,fill = "#d9d8cb",width=2)

        self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.95,
        self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.95,fill = "#5e4637",width=1)
        self.can_bg.create_line(self.canvas_padding[0], self.can_size[1]*0.98,
        self.can_size[0]-self.canvas_padding[0], self.can_size[1]*0.98,fill = "#261a13",width=2)

        self.can_bg.pack()
    
    def get_text_img(self,size,color,name):
        img = ft.get_num_img(size,color,name)
        imgTk = ImageTk.PhotoImage(img)
        return imgTk

    def update_data(self,total,unit,provision):
        # 数字
        self.can_bg.delete(self.t_total_id)
        self.t_total =      self.get_text_img(size=(25,30),color=(213,215,213),name=str(total))
        self.t_total_id = self.can_bg.create_image(self.iCoordDict["total"]    +self.offset[0], self.topPad-8,anchor='sw',image=self.t_total)

        self.can_bg.delete(self.t_unit_id)
        self.t_unit =       self.get_text_img(size=(25,30),color=(213,215,213),name=str(unit))
        self.t_unit_id = self.can_bg.create_image(self.iCoordDict["unit"]     +self.offset[0] - 10, self.topPad-8,anchor='sw',image=self.t_unit)

        self.can_bg.delete(self.t_provision_id)
        self.t_provision =  self.get_text_img(size=(35,30),color=(213,215,213),name=str(provision))
        self.t_provision_id = self.can_bg.create_image(self.iCoordDict["provision"]+self.offset[0] - 5, self.topPad-8,anchor='sw',image=self.t_provision)

####################################################################################################################