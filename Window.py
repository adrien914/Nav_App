from tkinter import Tk, Button, Canvas, Frame
from utils.Mouse import Mouse
from utils.Map import Map
import sys
from utils.DirectoryManager import DirectoryManager

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,hscale)

print("Please wait while your application is booting up ...")
################## Main #####################
window = Tk()
window.attributes('-fullscreen', True)

map = Map()
map.window = window

############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: DirectoryManager.get_directory(map, canvas, window), text="Choisir zone de navigation").pack(side="left")
calibrer_button = Button(button_frame, command=lambda: map.calibrer(), text="Calibrer carte").pack(side="left")
exit_button = Button(button_frame, command=lambda: sys.exit(0), text="Exit").pack(side="left")

#########################################

############ Canvas creation ############
width = window.winfo_screenwidth()
height = window.winfo_screenheight()
print(width)
print(height)
canvas = Canvas(window, width=width, height=height, bg="gray")
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas, window))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

map.show_history(canvas, window)

window.mainloop()
