from tkinter import Canvas,mainloop,Tk
import numpy as np
import random
import traceback
import threading
import time
from queue import Queue

class Point:
    def __init__(self,the_canvas,uID):
        self.uID = uID
        self.location = np.ones((2)) * 200
        self.color = "#"+"".join([random.choice('0123456789ABCDEF') for j in range(6)])
        self.the_canvas = the_canvas
        self.the_canvas.create_oval(200,200,200,200,
                     fill=self.color,outline=self.color,width=6,
                     tags=('runner'+str(self.uID),'runner'))
    def move(self):
        delta = (np.random.random((2))-.5)*20
        self.the_canvas.move('runner'+str(self.uID),delta[0],delta[1])

def queue_func():
    while True:
        time.sleep(.25)
        try:
            next_action = the_queue.get(False)
            next_action()
        except Exception as e: 
            if str(e) != "": 
                print(traceback.format_exc())

the_queue = Queue()
the_thread = threading.Thread(target=queue_func)
the_thread.daemon = True
the_thread.start()

window = Tk()
window.geometry('400x400')
the_canvas = Canvas(window,width=400,height=400,background='black')
the_canvas.grid(row=0,column=0)

points = {}
for i in range(100):
    points[i] = Point(the_canvas,i)

def random_movement():
    while True:
        for point in points.values():
            point.move()

the_queue.put(random_movement)

mainloop()