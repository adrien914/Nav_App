from tkinter import Tk, Button, Canvas, filedialog, Frame
from PIL import ImageTk as itk
from utils.Mouse import Mouse
from tkinter.font import Font
from utils.Map import Map
import os

def get_directory(map: Map, canvas: Canvas):
    directory = filedialog.askdirectory()
    map.load_map(directory)
    # arr = os.listdir(directory)
    # print(arr)
    print(vars(map))
    print(canvas)
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    canvas.create_image(width/2, height/2, anchor="center", image=map.image)



################## Main
window = Tk()

map = Map()

############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: get_directory(map, canvas), text="chose map").pack(side="left")
show_directory_button = Button(button_frame, command=lambda: print(map.directory), text="show directory").pack(side="left")
exit_button = Button(button_frame, command=lambda: exit(), text="Exit").pack(side="left")
#########################################

############ Canvas creation ############
canvas = Canvas(window, width=1800, height=1000)
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

window.mainloop()