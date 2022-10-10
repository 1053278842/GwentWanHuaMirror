import tkinter as tk
from tkinter import ttk, ALL, EventType
import tools.FileTool as ft
from tools.decorators import *
from enums.GwentEnum import *
from PIL import Image, ImageTk, ImageFont
import tkinter.font as tkFont
import copy

class module_board(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root =root

        # 图片源大小
        self.FILTER_BUTTON_ICO = (38,37)

        # 宽高
        self.can_size = [self.root.WIN_WIDTH,self.root.TOP_HEIGHT * 0.55]
        self.to_frame_pad  = [self.can_size[0] * 0.04 , self.can_size[1] * 0.11]
        # 背景宽高
        self.bg_size  = [self.can_size[0]*0.86,self.can_size[1]*0.95]
        self.bg_pad   = [self.can_size[0]*0.07,self.can_size[1]*0.07]
        # 颜色
        self.c_default  = "#2c1f17"
        self.c_hover    = "#6a4f2c"
        self.c_open     = "#f0c860"
        self.borderImageList = None
        # 布局
        self.columMax = 3
        self.sec_page_xPad = self.can_size[0]
        # 数据
        self.bg_page_data = {}
        self.create_page()
    
    def getHeight(self):
        return self.can_size[1]

    def create_page(self):
        self.can_bg = tk.Canvas(self,bg='#000000',width = self.can_size[0],height = self.can_size[1],highlightthickness=0,highlightcolor="green")
        # 两个页面
        self.create_module_page()
        self.create_filter_page()
        # 绑定事件
        self.can_bg.tag_bind("bt_bg",'<Enter>',self.hover_button)
        self.can_bg.tag_bind("bt_bg",'<Leave>',self.Leave_button)
        self.can_bg.tag_bind("bt_bg",'<Button-1>',self.Click_button)
        # 绑定背景
        self.can_bg.tag_bind("bg_page",'<Enter>',self.hover_bg)
        self.can_bg.tag_bind("bg_page",'<Leave>',self.leave_bg)
        # 绑定滚动
        self.can_bg.tag_bind("bg_page","<ButtonPress-1>",self.scroll_start)
        self.can_bg.tag_bind("bg_page","<B1-Motion>",self.scroll_move)
        self.can_bg.tag_bind("bg_page","<ButtonRelease-1>",self.scroll_release)
        # 限制拖动范围
        self.can_bg.configure(scrollregion=(0, 0, self.can_size[0]*2,0))
        self.init_button()
        self.can_bg.pack()
    
    def create_module_page(self):
        # data
        self.icon_pad = [self.root.WIN_WIDTH *0.04 ,self.can_size[1] * 0.05]
        img_size = Image.open(r"main/resources/images/deck_preview/button-border-ext.png").size
        self.scale_factor = (self.root.WIN_WIDTH/img_size[0]) * 0.21
        self.curr_img_size = []
        self.curr_img_size.append( img_size[0] * self.scale_factor )
        self.curr_img_size.append( img_size[1] * self.scale_factor )
        # 背景
        self.panel1 = ft.get_imgTk_xy(r"main/resources/images/deck_preview/wide-column-bg.png",x=self.bg_size[0],y=self.bg_size[1])
        bg_page_id = self.can_bg.create_image(self.bg_pad[0],self.bg_pad[1], anchor='nw' , image = self.panel1 ,tags="bg_page")
        self.bg_page_data[bg_page_id] = 0

        # 图片预存
        tempList = []
        for i in range(0,len(self.root.responseManager.CARD_DECK_INFO)):
            tempList.append(ft.get_img_resized(r"main/resources/images/deck_preview/button-border-ext.png",self.scale_factor))
        self.borderImageList=tempList

        # 存放模式按钮的id,便于时间处理中和filter按钮区分
        self.module_ids = []
        # 对应关系
        self.can_bg.comp_relation_d = {}
        # 地址预存
        tempList = []
        colum = 0
        row = 0
        for i in range(0,len(self.root.responseManager.CARD_DECK_INFO)):
            if colum >= self.columMax:
                colum = 0 
                row += 1
            tempList.append((self.to_frame_pad[0] + self.bg_pad[0] + self.icon_pad[0] * colum + self.curr_img_size[0] * colum, 
            self.to_frame_pad[1] + self.bg_pad[1] + (  self.icon_pad[1] + self.curr_img_size[1] ) * row))
            colum += 1
            self.can_bg.comp_relation_d[str(i)] ={"text":0,"button":0,"button_bg":0}
        self.iCoordDict = tempList

        #   多出来的补偿
        bg_color = self.c_default
        # 绘制按钮底色
        y_offset = -self.curr_img_size[1]*0.05
        for i in range(0,len(self.root.responseManager.CARD_DECK_INFO)):
            id = self.can_bg.create_rectangle(self.iCoordDict[i][0],self.iCoordDict[i][1],
            self.iCoordDict[i][0]+self.curr_img_size[0]+ y_offset , self.curr_img_size[1]+self.iCoordDict[i][1]-3,fill=bg_color)
            self.can_bg.comp_relation_d[str(i)]["button_bg"] = id
        # 绘制字符
        font = tkFont.Font(family='微软雅黑', size=8, weight=tkFont.BOLD)
        for i in range(0,len(self.root.responseManager.CARD_DECK_INFO)):
            buttonName = self.root.responseManager.CARD_DECK_INFO[i].buttonName
            id = self.can_bg.create_text(self.iCoordDict[i][0]+self.curr_img_size[0]/2,self.iCoordDict[i][1]+self.curr_img_size[1]/2,text=buttonName,font=font,fill=self.c_open)
            self.can_bg.comp_relation_d[str(i)]["text"] = id
   
        # 绘制按钮
        for i in range(0,len(self.root.responseManager.CARD_DECK_INFO)):
            id =self.can_bg.create_image(self.iCoordDict[i][0],self.iCoordDict[i][1], anchor='nw' , image = self.borderImageList[i] ,tags="bt_bg")
            self.can_bg.comp_relation_d[str(i)]["button"] = id
            self.module_ids.append(id)
        
        temp_dict = {}
        for key,value in self.can_bg.comp_relation_d.items():
            value["type"] = key
            temp_dict[value["button"]] = value
        self.can_bg.comp_relation_d = temp_dict


    def create_filter_page(self):
        ## 默认位置
        self.ico_scale = (self.root.WIN_WIDTH/self.FILTER_BUTTON_ICO[0]) * 0.12
 
        self.ico_size = ImageTk.getimage(ft.get_img_resized(r"main/resources/images/deck_preview/filter-ico/filter-rarity-rare.png",self.ico_scale)).size
        self.filter_ico_pad = [self.ico_size[0]*0.1,self.ico_size[1]*0.01]
        # 背景
        self.panel = ft.get_imgTk_xy(r"main/resources/images/deck_preview/wide-column-bg.png",x=self.bg_size[0],y=self.bg_size[1])
        bg_page_id = self.can_bg.create_image(self.bg_pad[0]+self.sec_page_xPad,self.bg_pad[1], anchor='nw' , image = self.panel ,tags="bg_page")
        self.bg_page_data[bg_page_id] = 1

        self.struct_data = [
            {"type":Rarity,"index":0,"path":"filter-rarity-all","default":True,"typeEnum":Rarity.ALL},
            {"type":Rarity,"index":1,"path":"filter-rarity-legendary","default":False,"typeEnum":Rarity.LEGENDARY},
            {"type":Rarity,"index":2,"path":"filter-rarity-epic","default":False,"typeEnum":Rarity.EPIC},
            {"type":Rarity,"index":3,"path":"filter-rarity-rare","default":False,"typeEnum":Rarity.RARE},
            {"type":Rarity,"index":4,"path":"filter-rarity-normal","default":False,"typeEnum":Rarity.COMMON},
            {"type":CardType,"index":0,"path":"filter-type-all","default":True,"typeEnum":CardType.ALL},
            {"type":CardType,"index":1,"path":"filter-type-special","default":False,"typeEnum":CardType.SPECIAL},
            {"type":CardType,"index":2,"path":"filter-type-unit","default":False,"typeEnum":CardType.UNIT},
            {"type":CardType,"index":3,"path":"filter-type-artifact","default":False,"typeEnum":CardType.ARTIFACT},
        ]

        
        for dict in self.struct_data:
            count = dict["index"]
            filePath = r"main/resources/images/deck_preview/filter-ico/"+dict["path"]+".png"
            self.temp_img_def = ft.get_img_resized(filePath,self.ico_scale)
            filePath = r"main/resources/images/deck_preview/filter-ico/"+dict["path"]+"-active"+".png"
            self.temp_img_act = ft.get_img_resized(filePath,self.ico_scale)
            row = 0
            if dict["type"] == CardType:
                row = 1
            dict["def_imgTk"] = self.temp_img_def
            dict["act_imgTk"] = self.temp_img_act
            dict["x"] = self.bg_pad[0] + self.to_frame_pad[0] + self.sec_page_xPad + (self.filter_ico_pad[0]+self.ico_size[0])*count
            dict["y"] = self.bg_pad[1] + self.to_frame_pad[1] + (self.filter_ico_pad[1]+self.ico_size[1])*row
            dict["isActive"] = dict["default"]
            img = dict["def_imgTk"]
            if dict["default"]:
                img = dict["act_imgTk"]
            id =self.can_bg.create_image(dict["x"],dict["y"], anchor='nw' , image = img ,tags="bt_bg")
            
            dict["button_id"] = id
            count += 1


    def hover_bg(self,event):
        self.can_bg.config(cursor="sb_h_double_arrow")

    def leave_bg(self,event):
        pass
        # self.can_bg.config(cursor="")

    def scroll_start(self,event):
        id = event.widget.find_withtag('current')[0]
        self.can_bg.config(cursor="sb_left_arrow")
        if self.bg_page_data[id] == 1:
            self.can_bg.config(cursor="sb_right_arrow")
            
        self.can_bg.scan_mark(event.x,event.y)
        self.scroll_start_y = event.y

    def scroll_move(self,event):
        id = event.widget.find_withtag('current')[0]
        self.can_bg.config(cursor="sb_left_arrow")
        if self.bg_page_data[id] == 1:
            self.can_bg.config(cursor="sb_right_arrow")
        self.can_bg.scan_dragto(event.x,self.scroll_start_y,gain=10)

    def scroll_release(self,event):
        self.can_bg.config(cursor="sb_h_double_arrow")
        self.can_bg.scan_dragto(event.x,self.scroll_start_y,gain=1000)

    def init_button(self):
        index = self.root.responseManager.CARD_DECK_INFO.index(self.root.responseManager.DEFAULT_CARD_DECK_INFO)
        self.reset_to_default()
        for key,value in self.can_bg.comp_relation_d.items():
            button_id = int(value["button"])
            bg_id = int(value["button_bg"])
            type_id = int(value["type"])
            text_id = int(value["text"])
            if index == type_id:
                self.can_bg.itemconfig(bg_id,fill=self.c_open)
                self.can_bg.itemconfig(text_id,fill=self.c_default)
                self.root.responseManager.CARD_DECK_INFO[type_id].isActive = True
                break
        

    def hover_button(self,event):
        self.can_bg.config(cursor="hand2")
        button_id = event.widget.find_withtag('current')[0]
        if button_id in self.module_ids:
            bg_id = int(self.can_bg.comp_relation_d[button_id]["button_bg"])
            type_id = int(self.can_bg.comp_relation_d[button_id]["type"])
            bt_status = self.root.responseManager.CARD_DECK_INFO[type_id].isActive 
            if not bt_status:
                self.can_bg.itemconfig(bg_id,fill=self.c_hover)
        
    def Leave_button(self,event):
        self.can_bg.config(cursor="")
        button_id = event.widget.find_withtag('current')[0]
        if button_id in self.module_ids:
            bg_id = int(self.can_bg.comp_relation_d[button_id]["button_bg"])
            type_id = int(self.can_bg.comp_relation_d[button_id]["type"])
            bt_status = self.root.responseManager.CARD_DECK_INFO[type_id].isActive
            if not bt_status:
                self.can_bg.itemconfig(bg_id,fill=self.c_default)

    def Click_button(self,event):
        button_id = event.widget.find_withtag('current')[0]
        if button_id in self.module_ids:
            bg_id = int(self.can_bg.comp_relation_d[button_id]["button_bg"])
            type_id = int(self.can_bg.comp_relation_d[button_id]["type"])
            text_id = int(self.can_bg.comp_relation_d[button_id]["text"])

            bt_status = self.root.responseManager.CARD_DECK_INFO[type_id].isActive 
            if not bt_status:
                self.reset_to_default()
                self.can_bg.itemconfig(bg_id,fill=self.c_open)
                self.can_bg.itemconfig(text_id,fill=self.c_default)
                self.root.responseManager.CARD_DECK_INFO[type_id].isActive = True
                # 更新数据
                self.root.responseManager.resetShowListCondition(self.root.responseManager.CARD_DECK_INFO[type_id])

                # 更新 filter 
                for dict in self.struct_data:
                    dict["isActive"] = False
                    id = dict["button_id"]
                    self.can_bg.itemconfig(id,image = dict["def_imgTk"])
                    if dict["default"]:
                        dict["isActive"] = True
                        self.can_bg.itemconfig(id,image = dict["act_imgTk"])
                    self.root.responseManager.CARD_DECK_INFO[type_id].rarity = Rarity.ALL
                    self.root.responseManager.CARD_DECK_INFO[type_id].cardType = CardType.ALL
            else:
                pass 
        else:
            for dict in self.struct_data:
                if int(dict["button_id"]) == button_id:
                    if not dict["isActive"]:
                        self.reset_to_default_filter(dict["type"])
                        self.can_bg.itemconfig(button_id,image=dict["act_imgTk"])
                        dict["isActive"] = True
                        # 定位当前的module
                        for cardTypeInfo in self.root.responseManager.CARD_DECK_INFO:
                            if cardTypeInfo.isActive:
                                if dict["type"] == Rarity:
                                    cardTypeInfo.rarity = dict["typeEnum"]
                                elif dict["type"] == CardType:
                                    cardTypeInfo.cardType = dict["typeEnum"]
                                # 更新数据
                                conditionObj = copy.copy(cardTypeInfo)
                                conditionObj.titleName = cardTypeInfo.titleName + " *"
                                self.root.responseManager.resetShowListCondition(conditionObj)
                                break
                    else:
                        has_active_num = self.get_active_num_filter(dict["type"])
                        if has_active_num > 1:
                            self.can_bg.itemconfig(button_id,image=dict["def_imgTk"])
                            dict["isActive"] = False


    def reset_to_default_filter(self,type):
        for dict in self.struct_data:
            if dict["type"] == type:
                self.can_bg.itemconfig(dict["button_id"],image=dict["def_imgTk"])
                dict["isActive"] = False
    
    def get_active_num_filter(self,type):
        num = 0
        for dict in self.struct_data:
            if dict["isActive"] and dict["type"] == type:
                num += 1
        return num

    def reset_to_default(self):
        for key,value in self.can_bg.comp_relation_d.items():
            button_id = int(value["button"])
            bg_id = int(value["button_bg"])
            type_id = int(value["type"])
            text_id = int(value["text"])
            
            self.can_bg.itemconfig(bg_id,fill=self.c_default)
            self.can_bg.itemconfig(text_id,fill=self.c_open)
            self.root.responseManager.CARD_DECK_INFO[type_id].isActive = False
