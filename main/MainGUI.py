import tkinter as tk
import services.GwentService as service
import sys
import os
from GwentGUI import GwentGUI

def start(temp_root):
    service.start()
    g2 = tk.Toplevel(temp_root)
    GwentGUI(temp_root)
    GwentGUI(g2,isEnemy=True)
    temp_root.mainloop()
    g2.mainloop()
    
def restart_program():
  python = sys.executable
  os.execl(python, python, * sys.argv)


if __name__ == '__main__':
    root_main = tk.Tk()
    service.start()
    sec_root = tk.Toplevel(root_main)
    GwentGUI(root_main,isEnemy=False)
    GwentGUI(sec_root,isEnemy=True)
    root_main.mainloop()
    sec_root.mainloop()

