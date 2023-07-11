import datetime
import json
import os
import sys
import tkinter as tk
import webbrowser
from tkinter import messagebox
from tkinter.ttk import *

import bean.global_var as global_var
import PanelManager as PM
import RequestManager as RM
import tools.FileTool as FT
from enums.GamePlatform import EGamePlatform
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import *
from ttkbootstrap.scrolled import ScrolledText


def liulonggood():
    webbrowser.open("http://117.50.175.251:8081/good")
def open_official_website():
    webbrowser.open("https://117.50.175.251/")
def open_download_link():
    webbrowser.open("http://117.50.175.251:8081/download")
def open_deck_website():
    webbrowser.open("https://117.50.175.251/mirrordeck/")

def setSortingRealLibraryState(state):
    root.sortingRealLibrary.set(state)
    global_config = FT.getGlobalConfig()
    global_config['sorting'] = root.sortingRealLibrary.get()
    FT.saveGlobalConfig(global_config)

def toggleComparative():
    global_config = FT.getGlobalConfig()
    global_config['comparative'] = root.comparativeForecastDeck.get()
    FT.saveGlobalConfig(global_config)

def toggleSortingRealLibrary():
    global_config = FT.getGlobalConfig()
    global_config['sorting'] = root.sortingRealLibrary.get()
    FT.saveGlobalConfig(global_config)

def toggleAutomaticSubmit():
    global_config = FT.getGlobalConfig()
    global_config['automaticSubmit'] = root.automaticSubmitBattleData.get()
    FT.saveGlobalConfig(global_config)

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
    try:
        root.version_orig.set(data['name'])
    except KeyError:
        print("name不存在!")

def updateVersionSteam():
    updateVersionJson(EGamePlatform.STEAM)
    # 版本切换时会有
    changeOrderCBState()

def updateVersionGOG():
    updateVersionJson(EGamePlatform.GOG)
    # 版本切换时会有
    changeOrderCBState()

def updateVersionGY():
    updateVersionJson(EGamePlatform.GY)
    # 版本切换时会有
    changeOrderCBState()

def changeOrderCBState():
    version = FT.getVersion()
    if 'orderMode' not in version:
        setSortingRealLibraryState(True)
        root.orderCB.config(state = NORMAL)
        return True
    if version['orderMode'] == 1:
        setSortingRealLibraryState(True)
        root.orderCB.config(state = NORMAL)
    else:
        setSortingRealLibraryState(False)
        root.orderCB.config(state = DISABLED)
    
def updateVersionJson(EGP):
    # 根据版本数据指定是否限制卡组顺序检视
    # 1:Steam
    # 2:GOG
    orig_data = FT.getVersion()
    orig_id = orig_data["id"]
    
    global_config = FT.getGlobalConfig()
    try:
        RM.RequestManager().updateVersion()
    except Exception:
        FT.saveVersion(orig_data)
        messagebox.showerror("错误","服务器请求失败!烦请重试或者手动前往官网进行更新:{0}".format(global_config["url"]))
        return
    data = FT.getVersion()
    new_id = data["id"]
    if data["canAutoUpdate"] == 0 and orig_id != new_id:
        FT.saveVersion(orig_data)
        messagebox.showwarning("警告","最新版本不支持自动更新!烦请手动前往官网进行更新:{0}".format(global_config["url"]))
        return
    root.version_orig.set(data['name'])
    root.version_new.set(data['name'])
    # 根据按钮，重设不同平台版本的基址
    FT.resetVersionPlatformAddress(EGP)
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
    # ----高级设置
    root.comparativeForecastDeck = tk.BooleanVar()
    root.sortingRealLibrary = tk.BooleanVar()
    root.automaticSubmitBattleData = tk.BooleanVar()
    global_config = FT.getGlobalConfig()
    root.comparativeForecastDeck.set(global_config['comparative'])
    root.sortingRealLibrary.set(global_config['sorting'])
    root.automaticSubmitBattleData.set(global_config['automaticSubmit'])
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
    main_frame5 = Frame(root)
    main_frame5.pack()

    frame_5 = Frame(main_frame5)
    frame_5.pack(side="top")
    playerWindowFrame = LabelFrame(frame_5,text="记牌窗口")
    # p1
    frame = Frame(frame_5)
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Label(frame,text="官网主页:",font=("黑体",9)).pack(side="left")
    Button(frame,command=open_official_website,text="Gwent Mirror",bootstyle=("warning")).pack(side="left",fill="x",expand=1)
    # p1
    frame = Frame(frame_5)
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Label(frame,text="下载地址:",font=("黑体",9)).pack(side="left")
    Button(frame,command=open_download_link,text="Download",bootstyle=("light")).pack(side="left",fill="x",expand=1)
    # p1
    frame = Frame(frame_5)
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Label(frame,text="卡组全书:",font=("黑体",9)).pack(side="left")
    Button(frame,command=open_deck_website,text="Mirror Deck",bootstyle=("info")).pack(side="left",fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_5)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Button(frame,command=liulonggood,text="点赞开发者！",bootstyle=("info")).pack(side="left",fill="x",expand=1)
    ########################################################################
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
    frame.pack(side="top",pady=6,padx=5,fill="x",expand=1)
    frame = Frame(frame_2)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Button(frame,command=updateVersionSteam,text="更新&设置平台版本!(Steam)",bootstyle=("warning")).pack(side="left",fill="x",expand=1)
    frame = Frame(frame_2)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Button(frame,command=updateVersionGOG,text="更新&设置平台版本!(GOG)",bootstyle=("light")).pack(side="left",fill="x",expand=1)
    frame = Frame(frame_2)
    frame.pack(side="top",pady=2,padx=5,fill="x",expand=1)
    Button(frame,command=updateVersionGY,text="更新&设置平台版本!(盖娅国服)",bootstyle=("info")).pack(side="left",fill="x",expand=1)

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
    st.insert(END, 
'<更新日志>\n\
 - <Version 0.5.1-bate>\n\
 · 【潮生】版本Steam&GOG自适应更新;\n\
 · 新增"其他"选项卡以及相关网页跳转;\n\
 · 新增"卡组全书"Web站点;\n\
 · 新增"点赞"按钮，为开发者灌注"活力"\n\
 · 其他功能陆续上线中...\n\
 · (心里话）说实在刚刚出入社会，花费了不少时间在找工作上，对于游戏和开发很难挤出精力，更多还是回到家躺床上；很抱歉中间断更了一两个版本。但还是希望我能够调整好心态，规划时间好好为我们喜爱的游戏发电~;\n\
\n\
 - <Version 0.3.95-bate>\n\
 · 服务器迁移,新官网IP为:http://117.50.175.251;\n\
\n\
 - <Version 0.3.9-bate>\n\
 · 兼容游戏版本10.12;\n\
 · 现在可以对盖娅国服兼容了;\n\
\n\
 - <Version 0.3.4-bate>\n\
 · 修复了读取不到"回响"卡牌的问题;\n\
 · 新增了预测卡牌不能自动刷新的问题;\n\
 · 新增了更新自检&提示;\n\
 · 新增了预测卡组的对比效果;\n\
 · 新增了高级选项卡;\n\
 · 新增了卡组状态栏的hover效果;\n\
 · 限制了监测剩余卡组顺序的功能;\n\
\n\
 - <Version 0.3.2-bate>\n\
 · 兼容了GOG;\n\
 · 修改了该窗口的初始化位置;\n\
\n\
 - <Version 0.3.1-bate>\n\
 · 编写了更新系统;\n\
 · 修复了推荐卡组时导致的意外崩溃问题;\n\
\n\
-------------------------------------\n\
-------------------------------------\n\
\n<写在前面>\n\
 · BUG提交烦请惠书邮箱:\n\
 · 1053278842@qq.com\n\
 · 内测交流群:129120844(QQ)\n\
\n ')
   ######################################################################
    main_frame4 = Frame(root)
    main_frame4.pack()
    frame_2 = Frame(main_frame4)
    frame_2.pack(side="top",fill="both",expand=1)
    # p1
    playerWindowFrame = LabelFrame(frame_2,text="预测模块")
    frame = Frame(playerWindowFrame)
    frame.pack(side="top",padx=5,pady=8,fill="x",expand=1)
    Label(frame,text="差 异 对 比:",font=("黑体",9)).pack(side="left")
    Checkbutton(frame,variable=root.comparativeForecastDeck,
        command=toggleComparative,bootstyle=("info")).pack(side="left",fill="both",expand=1)
    playerWindowFrame.pack(pady=5,fill="both",expand=1)
    # p2
    playerWindowFrame = LabelFrame(frame_2,text="记牌模块")
    frame = Frame(playerWindowFrame)
    frame.pack(side="top",padx=5,pady=8,fill="x",expand=1)
    Label(frame,text="真实牌组顺序:",font=("黑体",9)).pack(side="left")
    root.orderCB = Checkbutton(frame,variable=root.sortingRealLibrary,
        command=toggleSortingRealLibrary,bootstyle=("info"))
    root.orderCB.pack(side="left",fill="both",expand=1)
    playerWindowFrame.pack(pady=5,fill="both",expand=1)
    # p3
    playerWindowFrame = LabelFrame(frame_2,text="其他")
    frame = Frame(playerWindowFrame)
    frame.pack(side="top",padx=5,pady=8,fill="x",expand=1)
    Label(frame,text="共享对局卡组:",font=("黑体",9)).pack(side="left")
    Checkbutton(frame,variable=root.automaticSubmitBattleData,
        command=toggleAutomaticSubmit,bootstyle=("info")).pack(side="left",fill="both",expand=1)
    playerWindowFrame.pack(pady=5,fill="both",expand=1)

   ######################################################################

    frame = Frame(frame_2)
    frame.pack(side="top",pady=60,padx=5,fill="x",expand=1)  

    noteBook.add(main_frame,text="启动")
    noteBook.add(main_frame2,text="更新")
    noteBook.add(main_frame4,text="高级")
    noteBook.add(main_frame3,text="日志")
    noteBook.add(main_frame5,text="其他")
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
    panel_width = 250
    panel_height = 280
    panel_x = int((root.winfo_screenwidth() - panel_width) / 2)
    panel_y = int((root.winfo_screenheight() - panel_height) / 2)
    root.geometry('{0}x{1}+{2}+{3}'.format(panel_width,panel_height,panel_x,panel_y))
    root.resizable(0, 0)
    global_var.set_value("panel_root",root)
    # 隐藏界面，启动正常后显示，in PanelManager
    hidden()
    create_page(root)

    if checkCanUpdateDecks():
        root.after(10,RM.RequestManager().updateDecks())
    
    root.mainloop()



