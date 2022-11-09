import datetime
import json
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import *

import bean.global_var as global_var
import PanelManager as PM
import RequestManager as RM
import tools.FileTool as FT
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
        global_var.get_value("panel_root").ourCbTextVar.set("开 启")

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
        global_var.get_value("panel_root").oppCbTextVar.set("开 启")

def tips_no_gwent():
    root = global_var.get_value('panel_root')
    root.opponentPlayerCBVar.set(0)
    root.panelManager.closeOpponentPanel()
    root.ourPlayerCBVar.set(0)
    root.panelManager.closeOurPanel()
    root.ourCbTextVar.set("开  启")
    root.oppCbTextVar.set("开  启")
    messagebox.showinfo("提示","未检测到'Gwent.exe',请检查游戏否与启动!")

def tips_show(header,context):
    messagebox.showinfo(header,context)


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

def init_versionText():
    data = json.loads(open(r'main/resources/config/version.json', 'r',encoding="utf-16").read())
    root.version_orig.set(data['name'])

def updateVersionJson():
    orig_data = FT.getVersion()
    orig_id = orig_data["id"]

    global_config = FT.getGlobalConfig()
    try:
        RM.RequestManager().updateVersion()
    except Exception:
        FT.saveVersion(orig_data)
        messagebox.showerror("错误","服务器请求失败!烦请手动前往官网进行更新:{0}/download".format(global_config["url"]))
        return
    data = FT.getVersion()
    new_id = data["id"]
    if data["canAutoUpdate"] == 0 and orig_id != new_id:
        FT.saveVersion(orig_data)
        messagebox.showwarning("警告","最新版本不支持自动更新!烦请手动前往官网进行更新:{0}/download".format(global_config["url"]))
        return
    root.version_orig.set(data['name'])
    root.version_new.set(data['name'])
    if orig_id != new_id:
        messagebox.showinfo("提示","更新完毕!")
    else:
        messagebox.showinfo("提示","已经是最新版本!")



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

    root.version_orig = tk.StringVar()
    root.version_new = tk.StringVar()

    # 初始化组件值
    init_versionText()
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
    Entry(frame,font=("Verdana",8),state="readonly",textvariable=root.version_orig).pack(side="left",fill="x",expand=1)
    # p2
    frame = Frame(frame_2)
    frame.pack(side="top",pady=0,padx=5,fill="x",expand=1)
    Label(frame,text="最新版本:",font=("黑体",9)).pack(side="left")
    Entry(frame,font=("Verdana",8),state="readonly",textvariable=root.version_new).pack(side="left",fill="x",expand=1)

    frame = Frame(frame_2)
    frame.pack(side="top",pady=8,padx=5,fill="x",expand=1)
    Button(frame,command=updateVersionJson,text="点击检查并更新最新版本!",bootstyle=("warning")).pack(side="left",fill="x",expand=1)

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
    # context = FT.getVersion()["context"]
    st.insert(END, '<更新日志>\nVersion 0.3.1-bate:\n  编写了更新系统;\n  修复了推荐卡组时导致的意外崩溃问题;\n \
        \n<写在前面>\n \
    BUG提交烦请惠书邮箱:\n \
    1053278842@qq.com\n \
    技术交流:1053278842(QQ)\n \
    \n \
    本想做一个demo,集成暂时掌握的技术栈。但是不小心越走越远做的似乎臃肿了些。当然笔者也是广大昆友的一员,面对Gwent玩家数量的惨淡也希望贡献自己的一点力量。\
    \n\n \
    暂时不考虑盈利，代码很烂暂不考虑开源，维护好了便会开源。')
   

    noteBook.add(main_frame,text="启动")
    noteBook.add(main_frame2,text="更新")
    noteBook.add(main_frame3,text="关于")
    noteBook.pack(padx=10,pady=5,fill="both",expand=1)


def checkCanUpdateDecks():
    data = FT.getGlobalConfig()
    MaxDifHour = int(data["max_dif_hours"])
    nowTime = datetime.now()

    differenceTime = (nowTime - datetime.strptime(data["last_update_decks_time"], "%Y-%m-%d %H:%M:%S.%f")).seconds
    difHours = differenceTime/3600
    if difHours < MaxDifHour:
        print("距离下次更新卡组小时数:",MaxDifHour-difHours)
        pass
    else:
        print("本次启动将会更新本地卡组库!")
        data["last_update_decks_time"] = nowTime.strftime("%Y-%m-%d %H:%M:%S.%f")
        fp=open("main/resources/config/global_config.json","w",encoding="utf-8")
        json.dump(data,fp=fp,ensure_ascii=False)
        return True
    return False

def hidden():
    global_var.get_value("panel_root").withdraw()

def show():
    global_var.get_value("panel_root").deiconify()
    
def destroy():
    sys.exit(0)
    # global_var.get_value("panel_root").destroy()


if __name__ == '__main__':
    # 初始化全局变量文件
    global_var._init()

    root = tk.Tk()
    style = Style(theme="darkly")
    # 338*1000 最好比率
    
    root.title("Gwent Mirror")
    # root.iconbitmap('main/resources/images/favicon/Beer.ico')
    root.iconphoto(True,tk.PhotoImage(file='main/resources/images/favicon/Beer.png'))
    root.geometry('{0}x{1}+0+0'.format(230,280))
    root.resizable(0, 0)
    global_var.set_value("panel_root",root)
    # 隐藏界面，启动正常后显示，in PanelManager
    hidden()
    create_page(root)

    if checkCanUpdateDecks():
        root.after(10,RM.RequestManager().updateDecks())

    root.mainloop()



