from email.mime import image
import tkinter as tk
from tkinter import ttk, ALL, EventType
import FileTool as ft
import GwentService as service
from GwentEnum import *
from tkinter import PhotoImage
from PIL import Image, ImageTk
import copy
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
        self.canvas_padding = [23,60]
        # row_padding
        # BUG: 修改为卡片高度的比例
        self.canvas_row_padding = 38

        # 存储当前行信息
        self.orig_rows_infos = []

      
        self.create_page()

    def create_page(self):

        self.can_bg = tk.Canvas(self,bg='#000000',width = 338,height = 700,highlightthickness=0,highlightcolor="green")
        hwnd = self.can_bg.winfo_id()
        color_key = win32api.RGB(0,0,0) #full black in COLORREF structure
        wnd_ex_style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_ex_style = wnd_ex_style | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_ex_style)
        win32gui.SetLayeredWindowAttributes(hwnd,color_key,255,win32con.LWA_COLORKEY)

        # self.can_bg.bind("<B1-Motion>", lambda event: self.can_bg.scan_dragto(event.x, event.y, gain=1))
        self.can_bg.pack()

        self.btn1=tk.Button(self.root,text ='确定')
        self.btn1.bind('<ButtonPress-1>', lambda event: self.printInfo())
        self.btn1.pack()
        
        self.show_data_frame()

    def printInfo(self):

        print("# 输出 orig_rows_infos  #######################################")
        for i in self.orig_rows_infos :
            print(i,self.curr_memo_cards[i["instanceId"]]["Name"])  
        
        for i in self.can_bg.find_all():
            print(f'id:{i} tags:{self.can_bg.itemcget(i, "tags")}')

    
    def delay_delete_data(self,delete_row_info,row_info_dict):
        if len(self.can_bg.find_withtag(str(row_info_dict["row"])+"effect_tips")) == 0:
            if delete_row_info in self.orig_rows_infos:
                self.orig_rows_infos.remove(delete_row_info)
                self.can_bg.itemconfig(row_info_dict["row"],state="hidden")

    def remove_component(self,remove_card_id_list):
        will_delete_row_infos = []
        for row_info in self.orig_rows_infos:
            instanceId = row_info["instanceId"]
            if instanceId in remove_card_id_list:
                will_delete_row_infos.append(row_info)
                
        # 不影响遍历的情况下删除
        for delete_row_info in will_delete_row_infos:
            anim_time = 1000
            if len(self.can_bg.find_withtag(str(delete_row_info["row"])+"effect_tips")) == 0:
                row        = delete_row_info["row"]
                instanceId = delete_row_info["instanceId"]
                self.can_bg.after(anim_time,self.delay_delete_data,delete_row_info,delete_row_info)
                print("删除行:",row,self.curr_memo_cards[instanceId]["Name"],delete_row_info)
                # 隐藏行
                
                self.remove_tips_item(row,anim_time)


    def add_component(self,add_card_id_list):
        for iId in add_card_id_list:
            template_id = self.curr_memo_cards[iId]["Id"]
            card_index = int(self.curr_memo_cards[iId]["Index"],16)

            tagName = str(iId) + "card"
            temp_list = self.can_bg.find_withtag(tagName)
            if len(temp_list) == 0:
                print("【ERROR ERROR ERROR ERROR】 add 失败!")
                return 0
            row = temp_list[0]
            # 激活
            self.can_bg.itemconfig(row, state = "normal")
            self.can_bg.moveto(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*card_index)
            # 数据存储更新..
            temp_row_dict = {"row":row,"instanceId":iId,"templateId":template_id,"isFlashing":False,"rowId":row}
            self.orig_rows_infos.insert(card_index,temp_row_dict)
            print("添加行:",card_index,self.curr_memo_cards[iId]["Name"],temp_row_dict)
            self.add_tips_item(row)

        
    def get_orig_deck_iIds(self):
        temp_list = []
        for row_info in self.orig_rows_infos:
            temp_list.append(row_info["instanceId"])
        return temp_list

    def init_img_pool(self,curr_memo_cards,scale_factor):
        for key in curr_memo_cards:
            if len(self.can_bg.find_withtag(str(key)+"card")) == 0:
                # 不存在池中则实例化一个进入池
                template_id = int(curr_memo_cards[key]["Id"])
                template_provision =curr_memo_cards[key]["Provision"]
                template_name = curr_memo_cards[key]["Name"]

                imgTk = ft.get_deck_preview_img(template_id,template_provision,template_name,scale_factor)
                self.panel = tk.Label(master = self.root)
                self.panel.temp_img = imgTk
                self.can_bg.create_image(0,0,anchor='nw',image=self.panel.temp_img, tags = str(key)+"card",state = "hidden")

    def show_data_frame(self):
        scale_factor = self.root.DECK_IMG_SCALE_FACTOR * self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR
        # 分别获取当前软件中row的instanceId集，以及游戏内存中的instanceId
        curr_deck_iIds = self.get_orig_deck_iIds()
        self.curr_memo_cards = service.get_my_all_cards(1)
        # 从这开始
        self.init_img_pool(self.curr_memo_cards,scale_factor)
        # 过滤出需要增加或删除的数据
        remove_card_id_list  = service.get_deck_remove_cards(self.curr_memo_cards,curr_deck_iIds,scale_factor)
        add_card_id_list     = service.get_deck_add_cards(self.curr_memo_cards,curr_deck_iIds,scale_factor)        

        # print("remove_card_id_list:",self.remove_card_id_list,"add_card_id_list:",self.add_card_id_list)

        if len(remove_card_id_list) == 0 and len(add_card_id_list) == len(remove_card_id_list):
            self.move_component()
            # 源位置instanceId List
        # 删除多余的图片
        self.remove_component(remove_card_id_list)
        # 增加新加入的图片
        self.add_component(add_card_id_list)
        # 获取需要移动位置的图片
        self.update_deck_sort()
        # 循环收集curr_memo_cards并00
        # 处理add和remove
        self.after(200,self.show_data_frame)

    def move_component(self):
        original_iId_list = self.get_orig_deck_iIds()
        new_iId_list = []
        for card_instance_id in self.curr_memo_cards:
            if self.curr_memo_cards[card_instance_id]["Location"] == hex(Location.DECK.value):
                new_iId_list.append(int(card_instance_id))

        is_reload_param = False
        for i in range(0,len(original_iId_list)):
            if original_iId_list[i] != new_iId_list[i]:
                is_reload_param = True
                print("重置触发条件:",i,original_iId_list[i],self.curr_memo_cards[original_iId_list[i]])

        if not is_reload_param:
            return 0
        print("重设！","new:",len(new_iId_list),"orig:",len(self.orig_rows_infos))
        orig_list = copy.copy(self.orig_rows_infos)
        
        temp_list = []
        for new_iId in new_iId_list:
            # 顺带执行动画
            # self.anim_img_tips(new_iId,TipsType.WHITE)
            for orig_row_info in self.orig_rows_infos:
                if orig_row_info["instanceId"] == new_iId:
                    temp_list.append(orig_row_info)
                    self.orig_rows_infos.remove(orig_row_info)
                    break
        self.orig_rows_infos = temp_list

        new_list = copy.copy(self.orig_rows_infos)
        moved_row_id = self.get_moved_row(orig_list,new_list)
        self.anim_img_tips(moved_row_id,TipsType.WHITE)

    def get_moved_row(self,orig_list,new_list):
        moved_row_id = 0
        for i in range(0,len(orig_list)):
            if i+1 < len(orig_list):
                if orig_list[i+1]["row"] == new_list[i]["row"]:
                    moved_row_id = orig_list[i]["row"]
                    break
                else:
                    moved_row_id = new_list[i]["row"]
                    break
        return moved_row_id
    

    def add_tips_item(self,row):
        self.anim_img_tips(row,TipsType.ADD)

    def remove_tips_item(self,row,anim_time):
        self.anim_img_tips(row,TipsType.REMOVE,anim_time)


    def anim_img_tips(self,row,tipsType,anim_time=2500):
        count = 0
        iId = 0
        for row_info in self.orig_rows_infos:
            if row_info["row"] == row:
                iId = row_info["instanceId"]
                break
            count += 1
        if tipsType == TipsType.ADD:
            path = "Images/deck_preview/BLUE_FRAME.png"
        elif tipsType == TipsType.REMOVE:
            path = "Images/deck_preview/PURPLE_FRAME.png"
        elif tipsType == TipsType.MOVE:
            path = "Images/deck_preview/BLUE_FRAME.png"
        elif tipsType == TipsType.WHITE:
            path = "Images/deck_preview/WHITE_FRAME.png"

        img = ft.get_img(path)
        imgTk = ImageTk.PhotoImage(img)
        self.panel = tk.Label(master = self.root)
        self.panel.temp_img = imgTk
        row_id = self.can_bg.create_image(self.canvas_padding[0],self.canvas_padding[1]+self.canvas_row_padding*count,
        anchor='nw',image=self.panel.temp_img,tags = str(iId)+"effect_tips")
        self.root.after(anim_time,self.anim_img_tips_hidden,row_id)
        
    def anim_img_tips_hidden(self,img_id):
        self.can_bg.delete(img_id)

    def update_deck_sort(self):
        count  = 0
        for row_info in self.orig_rows_infos:
            self.can_bg.moveto(row_info["row"],x=self.canvas_padding[0],y=self.canvas_padding[1]+self.canvas_row_padding*count)
            count += 1
                

    # @moved_element: 要移动的row对象中card的instanceId
    # @moved_to_index: 要移动到的新下标位置      
    # @row_dict: 行信息字典，包含row对象id,template_id,instanceId，Name       
    def anim_move_one_row(self,moved_element,moved_to_index):
        orig_index = 0
        orig_row = 0
        for row_dict in self.orig_rows_infos:
            if row_dict["instanceId"] == moved_element:
                orig_index = self.orig_rows_infos.index(row_dict)
                orig_row = row_dict["row"]
                break
        # 目标row移至下标处
        times = moved_to_index-orig_index
        self.can_bg.move(orig_row,0,self.canvas_row_padding * times)
        