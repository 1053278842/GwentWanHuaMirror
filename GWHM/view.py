from email.mime import image
import tkinter as tk
from tkinter import ttk, ALL, EventType
import FileTool as ft
import GwentService as service
from GwentEnum import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
import win32gui
import win32con
import win32api

class deck_preview_bg_page(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.window =root
        self.create_page()

    
    def create_page(self):
        self.can_bg = tk.Canvas(self.window,bg="blue")
        self.window_width = self.window.winfo_width()
        self.window_height = self.window.winfo_height()
        
        self.p_top = ft.get_img_resized("Images/deck_preview/deck_bg_top_j.png",self.window.DECK_IMG_SCALE_FACTOR)
        self.can_bg.create_image(0,0,anchor='nw',image=self.p_top)
        self.p_mid = ft.get_img_resized("Images/deck_preview/deck_bg_mid_j.png",self.window.DECK_IMG_SCALE_FACTOR)
        self.can_bg.create_image(0,190,anchor='nw',image=self.p_mid)
        self.p_end = ft.get_img_resized("Images/deck_preview/deck_bg_end_j.png",self.window.DECK_IMG_SCALE_FACTOR)
        self.c_end = self.can_bg.create_image(0,700-118,anchor='nw',image=self.p_end)
        # 注册（绑定）窗口变动事件
        self.window.bind('<Configure>', self.window_resize)
        self.can_bg.pack(expand=True,fill=tk.BOTH)

    def window_resize(self,event=None):
        if event != None:
            if self.window_width != self.window.winfo_width() or self.window_height != self.window.winfo_height():
                if self.window_width != self.window.winfo_width():
                    self.window_width = self.window.winfo_width()
                if self.window_height != self.window.winfo_height():
                    self.window_height = self.window.winfo_height()
                    self.window.WINDOW_H = self.window_height
                self.load_image()

    def load_image(self):
        # return 0
        self.can_bg.coords(self.c_end,0,self.window_height-118)
        img = Image.open("Images/deck_preview/deck_bg_mid_j.png")
        scale = self.window.DECK_IMG_SCALE_FACTOR
        y_scale = (self.window_height-198-110)/(img.size[1]*scale)
        out = img.resize((int(img.size[0]*1*scale),int(img.size[1]*y_scale*scale)),Image.Resampling.LANCZOS)
        panel = tk.Label(master = self.window)
        panel.photo = ImageTk.PhotoImage(out)
        self.can_bg.itemconfig(2, image = panel.photo)
########################################################################################
# 图片卡组
class deck_preview_card_img_area(tk.Frame):

    def __init__(self, root):
        super().__init__(master = root)
        self.root = root

        # label list padding
        self.canvas_padding = [23,10]
        # row_padding
        # BUG: 修改为卡片高度的比例
        self.canvas_row_padding = 38

        self.deck_component_card_id_list = []
        self.all_rows = []
        self.create_page()
        
      

    def create_page(self):

        self.can_bg = tk.Canvas(self,bg='#000000',width = 338,height = 700,highlightthickness=0,highlightcolor="green")
        hwnd = self.can_bg.winfo_id()
        color_key = win32api.RGB(0,0,0) #full black in COLORREF structure
        wnd_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_ex_style = wnd_ex_style | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_ex_style)
        win32gui.SetLayeredWindowAttributes(hwnd,color_key,255,win32con.LWA_COLORKEY)

        # self.can_bg.bind('<ButtonPress-1>', lambda event: self.can_bg.scan_mark(event.x, event.y))
        # self.can_bg.bind("<B1-Motion>", lambda event: self.can_bg.scan_dragto(event.x, event.y, gain=1))
        self.can_bg.pack()
       
        self.show_data_frame()

    def get_component_card_id_list(self):
        return self.deck_component_card_id_list 

    def remove_component(self,remove_card_id_list):

        curr_memo_cards  = service.get_my_all_cards(1)

        component_all_rows = self.all_rows
        for row_dict in component_all_rows:
            # id 列表
            row        = row_dict["row"]
            instanceId = row_dict["instanceId"]
            templateId = row_dict["templateId"]
            if instanceId in remove_card_id_list:
                remove_card_id_list.remove(instanceId)

                self.delete_tips_item(row,templateId,5,row_dict)
                print("即将删除:",curr_memo_cards[instanceId]["Name"],row_dict)

    def add_component(self,add_card_id_list):
        curr_memo_cards  = service.get_my_all_cards(1)
        for card_id in add_card_id_list:
            # 防止图片实例化完丢失
            scale_factor = self.root.DECK_IMG_SCALE_FACTOR * self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR
            self.panel = tk.Label(master = self.root)
            template_id = curr_memo_cards[card_id]["Id"]
            template_provision = curr_memo_cards[card_id]["Provision"]
            template_name = curr_memo_cards[card_id]["Name"]
            card_index = curr_memo_cards[card_id]["Index"]
            # TODO 增加判断是否目录存在，存在则直接使用，反之在目录内重新实例化图片
            img = ft.get_deck_preview_img(template_id,template_provision,template_name,scale_factor)
            self.panel.temp_img = img
            self.insert_deck(self.panel.temp_img,card_id,template_id,card_index)
            
           
    def insert_deck(self,img,instanceId,templateId,index):
        index = int(index,16)
        curr_memo_cards  = service.get_my_all_cards(1)

        row = self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*index,anchor='nw',image=img)
        temp_row_dict = {"row":row,"instanceId":instanceId,"templateId":templateId,"isFlashing":False}
        self.all_rows.insert(index,temp_row_dict)
        self.deck_component_card_id_list.append(instanceId) 
        print("添加行:",index,curr_memo_cards[instanceId]["Name"],temp_row_dict)
        self.anim_move(index,1)
        self.add_tips_item(row,templateId,5,temp_row_dict)


    def show_data_frame(self):
        scale_factor = self.root.DECK_IMG_SCALE_FACTOR * self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR
        deck_component_card_id_list = self.get_component_card_id_list()
        self.curr_memo_cards = service.get_my_all_cards(1)
        remove_card_id_list  = service.get_deck_remove_cards(self.curr_memo_cards,deck_component_card_id_list,scale_factor)
        add_card_id_list     = service.get_deck_add_cards(self.curr_memo_cards,deck_component_card_id_list,scale_factor)        
        # 删除多余的图片
        self.remove_component(remove_card_id_list)
        # 增加新加入的图片
        self.add_component(add_card_id_list)
        # 循环收集curr_memo_cards并00
        # 处理add和remove
        self.after(1000,self.show_data_frame)

    def add_tips_item(self,row,id,times,row_dict):
        if not row_dict["isFlashing"]:
            row_dict["isFlashing"] = True
            print(row_dict)
            self.img_flash_show_tip(row,id,times,1.5,row_dict)

    def delete_tips_item(self,row,id,times,row_dict):
        if not row_dict["isFlashing"]:
            row_dict["isFlashing"] = True
            self.img_flash_show_tip(row,id,times,0.7,row_dict)

    # 依次替换img图标
    def img_flash_hidden_tip(self,row,id,times,hidden_effect_factor,row_dict):
        can_doing = False
        for row_dict_temp in self.all_rows:
            if row == row_dict_temp["row"]:
                can_doing = True
        if not can_doing:
            return 0

        path = "deck_preview_temp/"+str(id)+".png"
        img = ft.get_img_hidden_effect(path,hidden_effect_factor)
        self.panel = tk.Label(master = self.root)
        self.panel.photo = ImageTk.PhotoImage(img)
        self.can_bg.itemconfig(row,image=self.panel.photo)

        self.root.after(200,self.img_flash_show_tip,row,id,times,hidden_effect_factor,row_dict)

   # 依次替换img图标
    def img_flash_show_tip(self,row,id,times,hidden_effect_factor,row_dict):
        can_doing = False
        for row_dict_temp in self.all_rows:
            if row == row_dict_temp["row"]:
                can_doing = True
        if not can_doing:
            return 0

        path = "deck_preview_temp/"+str(id)+".png"
        img = ft.get_img(path)
        self.panel = tk.Label(master = self.root)
        self.panel.pic = ImageTk.PhotoImage(img)
        self.can_bg.itemconfig(row,image=self.panel.pic)
        times -= 1
        if times > 0:
            self.root.after(200,self.img_flash_hidden_tip,row,id,times,hidden_effect_factor,row_dict)
        else:
            # 删除情况下
            if hidden_effect_factor < 1:
                next_row_index = 0
                self.can_bg.delete(row)
                for row_dict in self.all_rows:
                    # print(row)
                    if row_dict["row"] == row and row_dict["templateId"] == id:
                        print("删除行:",row)
                        
                        next_row_index = self.all_rows.index(row_dict)
                        self.all_rows.remove(row_dict)
                        self.deck_component_card_id_list.remove(row_dict["instanceId"])
                # 移动
                self.anim_move(next_row_index)
                row_dict["isFlashing"] = False
            else:
                row_dict["isFlashing"] = False
                print(row_dict,"ADD")

    def anim_move(self,start_index,dir = -1):
        print("执行动画:",start_index,dir)
        all_rows = self.all_rows
        index = 0
        start_move = False
        for row_dict in all_rows:
            row_id = row_dict["row"]
            if all_rows[start_index] == row_dict:
                start_move = True
            if start_move:
                self.can_bg.move(row_id,0,self.canvas_row_padding * dir)
            index += 1
        # self.root.after(100,self.anim_move_all_to_top)
########################################################################################
# 图片卡组
class my_deck_img_page(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.root =root
        self.create_page()
        

    def create_page(self):
        self.tree_view = ttk.Treeview(self.root,show='tree',select="none",padding="(0,0,0,0)",height=30)
        ttk.Style().configure("Treeview", background="black",foreground="white")
        self.tree_view.pack(fill=tk.BOTH,expand=True,padx=0,pady=0)

        self.show_data_frame()
        s = ttk.Style()
        s.configure('Treeview', rowheight=35)

    def get_component_card_id_list(self):
        component_all_rows = self.tree_view.get_children()
        deck_component_card_id_list = []
        for row in component_all_rows:
            curr_card_id = self.tree_view.item(row,option='values')[0]
            deck_component_card_id_list.append(int(curr_card_id))
        return deck_component_card_id_list 

    def remove_component(self,remove_card_id_list):
        component_all_rows = self.tree_view.get_children()
        for row in component_all_rows:
            # id 列表
            instanceId = int(self.tree_view.item(row)['values'][0])
            templateId = self.curr_memo_cards[instanceId]["Id"]
            if instanceId in remove_card_id_list:
                remove_card_id_list.remove(instanceId)
                self.delete_tips_item(row,templateId,5)

    def add_component(self,add_card_id_list):
        curr_memo_cards  = service.get_my_all_cards(1)
        for card_id in add_card_id_list:
            # 防止图片实例化完丢失
            global SCALE_FACTOR
            SCALE_FACTOR = 0.6
            self.paned = tk.PanedWindow(self.root)
            template_id = curr_memo_cards[card_id]["Id"]
            template_provision = curr_memo_cards[card_id]["Provision"]
            template_name = curr_memo_cards[card_id]["Name"]
            img = ft.get_deck_preview_img(template_id,template_provision,template_name,SCALE_FACTOR)
            self.paned.temp_img = img
            curr_row = self.tree_view.insert('', tk.END, image = self.paned.temp_img,
                value=(card_id)
            )
            self.add_tips_item(curr_row,template_id,5)

    def show_data_frame(self):
        scale_factor = self.root.DECK_IMG_SCALE_FACTOR * self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR
        deck_component_card_id_list = self.get_component_card_id_list()
        self.curr_memo_cards = service.get_my_all_cards(1)
        remove_card_id_list  = service.get_deck_remove_cards(self.curr_memo_cards,deck_component_card_id_list,scale_factor)
        add_card_id_list     = service.get_deck_add_cards(self.curr_memo_cards,deck_component_card_id_list,scale_factor)        
        # 删除多余的图片
        self.remove_component(remove_card_id_list)
        # 增加新加入的图片
        self.add_component(add_card_id_list)
        # 循环收集curr_memo_cards并00
        # 处理add和remove
        self.after(2000,self.show_data_frame)

    def add_tips_item(self,row,id,times):
        if self.tree_view.exists(row):
            self.img_flash_show_tip(row,id,times,1.5)

    def delete_tips_item(self,row,id,times):
        if self.tree_view.exists(row):
            self.img_flash_show_tip(row,id,times,0.7)

    # 依次替换img图标
    def img_flash_hidden_tip(self,row,id,times,hidden_effect_factor):
        if self.tree_view.exists(row):
            path = "deck_preview_temp/"+str(id)+".png"
            img = ft.get_img_hidden_effect(path,hidden_effect_factor)
            self.panel = tk.Label(master = self.root)
            self.panel.photo = ImageTk.PhotoImage(img)
            self.tree_view.item(row,option=None,image=self.panel.photo)

            self.root.after(300,self.img_flash_show_tip,row,id,times,hidden_effect_factor)

   # 依次替换img图标
    def img_flash_show_tip(self,row,id,times,hidden_effect_factor):
        if self.tree_view.exists(row):
            path = "deck_preview_temp/"+str(id)+".png"
            img = ft.get_img(path)
            self.panel = tk.Label(master = self.root)
            self.panel.photo = ImageTk.PhotoImage(img)
            self.tree_view.item(row,option=None,image=self.panel.photo)
            times -= 1
            if times > 0:
                self.root.after(300,self.img_flash_hidden_tip,row,id,times,hidden_effect_factor)
            else:
                # 删除情况下
                if hidden_effect_factor < 1:
                    self.tree_view.delete(row)