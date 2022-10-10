import tkinter as tk
root = tk.Tk()
root.geometry()
cv = tk.Canvas(root, bg = 'gray')
cv.pack()
rt1 = cv.create_rectangle(50,50,110,110,
                          activefill = 'gray75',tag = ('r','r1')) #设置属性
rt2 = cv.create_rectangle(50,50,110,110,width = 3,
                          activefill = 'gray75',tag = ('r','r2')) #设置属性
cv.scale('r1',50,50,2,2) #以矩形左上角的点为缩放中心
print(cv.coords('r1')) 
print(cv.coords('r2'))
