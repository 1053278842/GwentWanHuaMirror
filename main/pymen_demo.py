import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CardCounterPanel(tk.Toplevel):
    def __init__(self, master, deck_name):
        '''初始化记牌器面板'''
        super().__init__(master)
        self.title(f'卡组 {deck_name} 记牌器')
        self.geometry('800x600')
        # 在窗口中心创建一个画布
        self.canvas = tk.Canvas(self, bg='#ECECEC', width=750, height=500, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.place(x=25, y=50)
        # 设置卡组名称和数量信息的字体样式
        self.heading_font = ('Arial', 20, 'bold')
        self.subheading_font = ('Arial', 12, 'bold')
        # 在画布上添加卡组名称和数量信息
        self.canvas.create_text(40, 10, text='卡组', font=self.heading_font, anchor='nw')
        self.canvas.create_text(40, 45, text=deck_name, font=self.subheading_font, anchor='nw')
        self.canvas.create_text(650, 10, text='数量', font=self.heading_font, anchor='ne')
        self.canvas.create_text(650, 45, text='（张）', font=self.subheading_font, anchor='ne')
        # 添加卡牌和数量信息
        card_names = ['战斗号角', '小精灵', '吸血蝙蝠', '大荒星陨', '烈焰陨星']
        card_counts = [3, 2, 1, 4, 0]
        x, y, width, height = 25, 80, 140, 200
        for card_name, card_count in zip(card_names, card_counts):
            # 加载卡牌图像，并调整大小以适应画布
            image_file = f'main/{card_name}.jpg'
            image = Image.open(image_file)
            image = image.resize((int(width * 0.8), int(height * 0.8)))
            image = ImageTk.PhotoImage(image)
            panel = tk.Label(master = root)
            panel.temp_img = image
            self.canvas.create_image(x+width/2, y+height/2, image=panel.temp_img)
            self.canvas.create_text(x+width/2, y+height-35, text=card_count, font=self.heading_font)
            self.canvas.create_text(x+width/2, y+height+40, text=card_name, font=self.subheading_font)
            x += width + 25

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    # 使用ttk风格美化应用程序
    style = ttk.Style()
    style.theme_use('clam')
    # 显示卡组1的记牌器面板
    CardCounterPanel(root, '卡组1')
    root.mainloop()
