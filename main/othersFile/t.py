import tkinter as tk

root = tk.Tk()

img = tk.Canvas(root, bg = "green", width = 1100, height = 600)
img.grid()
# img.configure(scrollregion=(0, 0, 1000, 800))

#Some canvas objects
#...

img.bind('<ButtonPress-1>', lambda event: img.scan_mark(event.x, event.y))
img.bind("<B1-Motion>", lambda event: img.scan_dragto(event.x, event.y, gain=1))

root.mainloop()