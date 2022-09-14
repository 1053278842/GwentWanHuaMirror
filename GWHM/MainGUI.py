import tkinter as tk
from tkinter import ttk
import GwentService as service
from GwentEnum import *
from view import *
from threading import Thread
from tkinter import PhotoImage


class GwentGUI:

    def __init__(self,root):
        self.root = root
        self.root.title = "Gwent Card View"
        self.root.geometry('338x800+50+50')
        self.root.wm_attributes('-topmost',1)
        # root.overrideredirect(True)
        self.root.resizable(width=False,height=True)
        self.root.WINDOW_H = 0
        self.root.DECK_IMG_SCALE_FACTOR = 0.6
        self.root.DECK_IMG_SCALE_COMPENSATE_FACTOR = 1.214

        self.table_view = tk.Frame()
        self.table_view.pack()
        
        self.create_menu()
        self.create_page()


    def create_page(self):
        self.deck_preview_bg_page = deck_preview_bg_page(self.root)
        self.my_deck_img_page = deck_preview_card_img_area(self.root)

        self.show_deck_img()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        menubar.add_command(label='卡组-data',command=self.show_deck_data)
        menubar.add_command(label='卡组-Img ',command=self.show_deck_img)
        self.root['menu'] = menubar
    
    def show_deck_img(self):
        self.my_deck_img_page["bg"] = "#000000"
        # 透明化Frame
        hwnd = self.my_deck_img_page.winfo_id()
        colorkey = win32api.RGB(0,0,0) #full black in COLORREF structure
        wnd_exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        new_exstyle = wnd_exstyle | win32con.WS_EX_LAYERED
        win32gui.SetWindowLong(hwnd,win32con.GWL_EXSTYLE,new_exstyle)
        win32gui.SetLayeredWindowAttributes(hwnd,colorkey,255,win32con.LWA_COLORKEY)

        self.my_deck_img_page.place(x=0, y=50, anchor='nw')
        

    def show_deck_data(self):
        pass
    #     self.my_deck_data_page.pack(fill=tk.BOTH,expand=True)
    #     self.my_deck_data_page.tree_view.pack(fill=tk.BOTH,expand=True)
    #     self.my_deck_img_page.pack_forget()
    #     self.my_deck_img_page.tree_view.pack_forget()

if __name__ == '__main__':
    root = tk.Tk()
    
    memory_thread = Thread(target=service.start)
    memory_thread.start()
    memory_thread.join()
    # 扫描到GameInstance,进入deck功能
    mainPage = GwentGUI(root)
    
    root.mainloop()