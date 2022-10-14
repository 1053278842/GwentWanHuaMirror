import json
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *

import bean.global_var as global_var
import PanelManager as PM
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import *
from ttkbootstrap.scrolled import ScrolledText


def toggleOurCardPanel():
    root = global_var.get_value('panel_root')
    status_var = root.ourPlayerCBVar.get()
    if status_var == 1:
        # 显示我方记牌器
        var_w = int(root.cardsPanelWidth.get())
        var_h = int(root.cardsPanelHeight.get())
        coords = (var_w,var_h)
        root.panelManager.openOurPanel(root,coords)
    elif status_var == 0:
        # 关闭我方记牌器
        root.panelManager.closeOurPanel()

def toggleOpponentCardPanel():
    root = global_var.get_value('panel_root')
    status_var = root.opponentPlayerCBVar.get()
    if status_var == 1:
        # 显示我方记牌器
        var_w = int(root.cardsPanelWidth.get())
        var_h = int(root.cardsPanelHeight.get())
        coords = (var_w,var_h)
        root.panelManager.openOpponentPanel(root,coords)
    elif status_var == 0:
        # 关闭我方记牌器
        root.panelManager.closeOpponentPanel()

def tips_no_gwent():
    root = global_var.get_value('panel_root')
    root.opponentPlayerCBVar.set(0)
    root.panelManager.closeOpponentPanel()
    root.ourPlayerCBVar.set(0)
    root.panelManager.closeOurPanel()
    root.ourCbTextVar.set("开  启")
    root.oppCbTextVar.set("开  启")
    messagebox.showinfo("提示","未检测到'Gwent.exe',请检查游戏否与启动!")


def UpdateCoordsJson():
    var_w = root.cardsPanelWidth.get()
    var_h = root.cardsPanelHeight.get()
    data = {"width": var_w, "height": var_h}
    if len(var_w)> 0 and len(var_h)> 0 and var_w.isdigit() and var_h.isdigit():
        if int(var_w) <150 or int(var_h) <400:
            data = {"width": 150, "height": 400}
        # 写入Json文件到config文件夹
        try:
            with open(r'main/resources/config/panelCoords.json', 'w') as write_f:
                write_f.write(json.dumps(data,indent=4,ensure_ascii=False))
                return True
        except Exception :
            print("写入分辨率时出错！")
            return False
    return False

def init_coords_components():
    isExist = os.path.exists(r'main/resources/config/panelCoords.json')
    if isExist:
        try:
            coords_data = json.loads(open(r'main/resources/config/panelCoords.json', 'r').read())
            root.cardsPanelWidth.set(coords_data['width'])
            root.cardsPanelHeight.set(coords_data['height'])
        except Exception:
            pass

def create_page(root):
    # Data
    # ----复选框(显示记牌器)
    root.ourPlayerCBVar = tk.IntVar()
    root.opponentPlayerCBVar = tk.IntVar()
    root.ourPlayerCBVar.set(0)
    root.opponentPlayerCBVar.set(0)
    root.ourCbTextVar = tk.StringVar()
    root.oppCbTextVar = tk.StringVar()
    root.ourCbTextVar.set("开  启")
    root.oppCbTextVar.set("开  启")
    # ----输入框(记牌器大小)
    root.cardsPanelWidth = tk.StringVar()
    root.cardsPanelHeight = tk.StringVar()

    # 初始化组件值
    init_coords_components()
    root.panelManager = PM.PanelManager(root)
    
    noteBook = Notebook(root,bootstyle="secondary")

    main_frame = Frame(root)
    main_frame.pack()

    frame_1 = Frame(main_frame)
    frame_1.pack(side="top")
    playerWindowFrame = LabelFrame(frame_1,text="记牌窗口")
    # p1
    frame = Frame(playerWindowFrame)
    frame.pack(side="top",padx=5,pady=3,fill="both",expand=1)
    Label(frame,text="我方:",font=("黑体",9)).pack(side="left")
    Checkbutton(frame,text="开  启",textvariable=root.ourCbTextVar,variable=root.ourPlayerCBVar,command=toggleOurCardPanel,bootstyle=("toolbutton","success")).pack(side="left",fill="both",expand=1)
    # p2
    frame = Frame(playerWindowFrame)
    frame.pack(side="top",pady=5,padx=5,fill="both",expand=1)
    Label(frame,text="对方:",font=("黑体",9)).pack(side="left")
    Checkbutton(frame,text="开  启",textvariable=root.oppCbTextVar,variable=root.opponentPlayerCBVar,command=toggleOpponentCardPanel,bootstyle=("toolbutton","success")).pack(side="left",fill="both",expand=1)
    playerWindowFrame.pack(pady=5,fill="both",expand=1)

    playerWindowFrame = LabelFrame(frame_1,text="Config",padding=(0,5))
    # label
    size_config_frame = LabelFrame(playerWindowFrame,text="分辨率")
    size_config_frame.pack(side="top",padx=5)
    # width
    frame = Frame(size_config_frame)
    frame.pack(side="top",padx=5,pady=4)
    Label(frame,text="宽:",font=("黑体",9)).pack(side="left")
    Entry(frame,font=("Verdana",7),textvariable=root.cardsPanelWidth,validate="focusout",validatecommand=UpdateCoordsJson).pack()
    # height
    frame = Frame(size_config_frame)
    frame.pack(side="top",padx=5,pady=4)
    Label(frame,text="高:",font=("黑体",9)).pack(side="left")
    Entry(frame,font=("Verdana",7),textvariable=root.cardsPanelHeight,validate="focusout",validatecommand=UpdateCoordsJson).pack(side="left")
    playerWindowFrame.pack(pady=8,fill="both",expand=1)

    ######################################################################
    main_frame2 = Frame(root)
    main_frame2.pack()
    frame_2 = Frame(main_frame2)
    frame_2.pack(side="top",fill="both",expand=1)
    # p1
    frame = Frame(frame_2)
    frame.pack(side="top",padx=5,pady=8,fill="x",expand=1)
    Label(frame,text="当前版本:",font=("黑体",9)).pack(side="left")
    Entry(frame,font=("Verdana",8)).pack(side="left",fill="x",expand=1)
    # p2
    frame = Frame(frame_2)
    frame.pack(side="top",pady=0,padx=5,fill="x",expand=1)
    Label(frame,text="最新版本:",font=("黑体",9)).pack(side="left")
    Entry(frame,font=("Verdana",8)).pack(side="left",fill="x",expand=1)

    frame = Frame(frame_2)
    frame.pack(side="top",pady=8,padx=5,fill="x",expand=1)
    Button(frame,text="点击检查最新版本更新!",bootstyle=("warning")).pack(side="left",fill="x",expand=1)

    frame = Frame(frame_2)
    frame.pack(side="top",pady=60,padx=5,fill="x",expand=1)  

    ######################################################################
    main_frame3 = Frame(root)
    main_frame3.pack()
    frame_2 = Frame(main_frame3)
    frame_2.pack(side="top",fill="both",expand=1)
    # p1
    # scrolled text with autohide vertical scrollbar
    st = ScrolledText(frame_2, padding=5, height=10, autohide=True)
    st.pack(fill=BOTH, expand=YES)

    # add text
    st.insert(END, 'BUG提交烦请惠书邮箱:\n1053278842@qq.com')
    st.insert(END, '\n技术交流:1053278842(QQ)')
    st.insert(END, '\n')
    st.insert(END, '\n开发这个的原因:\n')
    st.insert(END, '本想做一个demo,集成暂时掌握的技术栈。但是不小心越走越远做的似乎臃肿了些。')
    st.insert(END, '当然笔者也是广大昆友的一员,面对Gwent玩家数量的惨淡也希望贡献自己的一点力量。')
    st.insert(END, '于是着力于游戏内、外信息获取的方式,从便利性上寻求突破(这里不得不提一嘴LOR,光找卡组就把我劝退了...)。')
    st.insert(END, '暂时不考虑盈利，开源的话因为代码很烂，等维护好了自然会开源的。')

    noteBook.add(main_frame,text="启动")
    noteBook.add(main_frame2,text="更新")
    noteBook.add(main_frame3,text="关于")
    noteBook.pack(padx=10,pady=5,fill="both",expand=1)



if __name__ == '__main__':
    # 初始化全局变量文件
    global_var._init()

    root = tk.Tk()
    style = Style(theme="darkly")
    # 338*1000 最好比率
    
    root.title("Gwent Mirror")
    root.geometry('{0}x{1}+0+0'.format(230,280))
    root.resizable(0, 0)
    global_var.set_value("panel_root",root)
    create_page(root)

    root.mainloop()

def restartCardListPanel():
    isActive = global_var.get_value("isActive")
    if isActive:
        gl_panel_root = global_var.get_value("panel_root")
        ourCBVar = int(gl_panel_root.ourPlayerCBVar.get())
        oppCBVar = int(gl_panel_root.opponentPlayerCBVar.get())
        if ourCBVar == 1:
            global_var.set_value("isActive",False)
            gl_panel_root.ourPlayerCBVar.set(0)
            toggleOurCardPanel()
            gl_panel_root.ourPlayerCBVar.set(1)
            toggleOurCardPanel()
        
        if oppCBVar == 1:
            global_var.set_value("isActive",False)
            gl_panel_root.opponentPlayerCBVar.set(0)
            toggleOpponentCardPanel()
            gl_panel_root.opponentPlayerCBVar.set(1)
            toggleOpponentCardPanel()


