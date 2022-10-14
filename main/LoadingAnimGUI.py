from itertools import cycle
from pathlib import Path

import ttkbootstrap as ttk
from PIL import Image, ImageSequence, ImageTk
from ttkbootstrap.constants import *


class AnimatedGif(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=300)

        # open the GIF and create a cycle iterator
        file_path = Path(__file__).parent / "resources/images/deck_preview/loadding.gif"
        with Image.open(file_path) as im:
            # create a sequence
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # length of each frame
            self.framerate = im.info["duration"]

        self.img_container = ttk.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """Update the image for each frame"""
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)