from tkinter import *
# 以下是callback方法
def selAll():                  # 选取全部字符串
    entry.select_range(0,END)
def deSel():                   # 取消选取
    entry.select_clear()
def clr():                     # 删除文字
    entry.delete(0,END)
def read_only():
    print("调用read_only函数中...",var.get())
    if var.get() == True:
        chkReadOnly.config(state=DISABLED)  # 设为DISABLED 不可使用
    else:
        chkReadOnly.config(state=NORMAL)    # 设为NORMAL

root = Tk()
root.title("apidemos.com")     # 窗口标题

# 以下row=0建立Entry
entry = Entry(root)
entry.grid(row=0,column=0,columnspan=4,
            padx=5,pady=5,sticky=W)
# 以下row=1建立Button
btnSel = Button(root,text="全选",command=selAll)
btnSel.grid(row=1,column=0,padx=5,pady=5,sticky=W)

btnDesel = Button(root,text="取消选取",command=deSel)
btnDesel.grid(row=1,column=1,padx=5,pady=5,sticky=W)

btnClr = Button(root,text="删除",command=clr)
btnClr.grid(row=1,column=2,padx=5,pady=5,sticky=W)

btnQuit = Button(root,text="结束程序",command=root.destroy)
btnQuit.grid(row=1,column=3,padx=5,pady=5,sticky=W)

# 以下row=2建立Checkboxes
var = BooleanVar()
var.set(False)
# var.set(True)
# read_only()
chkReadOnly = Checkbutton(root,text="只读",variable=var,
                            command=read_only)
chkReadOnly.grid(row=2,column=0)

root.mainloop()