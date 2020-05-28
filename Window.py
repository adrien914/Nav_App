from tkinter import Tk, Button, Canvas, Frame
from utils.Mouse import Mouse
from utils.Map import Map
import sys
from utils.DirectoryManager import DirectoryManager

print("Please wait while your application is booting up ...")
################## Main #####################
window = Tk()

map = Map()
############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: DirectoryManager.get_directory(map, canvas, window), text="Choisir zone de navigation").pack(side="left")
exit_button = Button(button_frame, command=lambda: sys.exit(0), text="Exit").pack(side="left")

#########################################

############ Canvas creation ############
canvas = Canvas(window, width=1800, height=1000)
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

map.show_history(canvas, window)

window.mainloop()
