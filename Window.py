from tkinter import Tk, Button, Canvas, filedialog, Frame
from utils.Mouse import Mouse
from utils.Map import Map
import glob

def get_directory(map: Map, canvas: Canvas, window):
    directory = filedialog.askdirectory()
    if directory:
        map.load_map(directory)
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if map.image_id:
            canvas.delete(map.image_id)
        map.image_id = canvas.create_image(width/2, height/2, anchor="center", image=map.image)
        files = glob.glob(directory + "/*.jpg")
        for avant_pm in range(1, 7):
            button = Button(window, text=str(7 - avant_pm) + "h avant pleine mer", command=lambda avant_pm=avant_pm: change_map(map, canvas, files[len(files) - 2 - (2 * (avant_pm - 1))]), anchor="w")
            canvas.create_window(40, 250 + 30 * avant_pm, anchor="nw", window=button)
        button = Button(window, text="pleine mer",command=lambda: change_map(map, canvas, files[-1]), anchor="w")
        canvas.create_window(60, 250 + 30 * 7, anchor="nw", window=button)
        for apres_pm in range(1, 7):
            button = Button(window, text=str(apres_pm) + "h après pleine mer", command=lambda apres_pm=apres_pm: change_map(map, canvas, files[2 * (apres_pm - 1)]), anchor="w")
            canvas.create_window(40, 250 + 30 * (apres_pm + 7), anchor="nw", window=button)

def change_map(map: Map, canvas: Canvas, path: str):
    if path:
        map.change_map(path)
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if map.image_id:
            canvas.delete(map.image_id)
        map.image_id = canvas.create_image(width / 2, height / 2, anchor="center", image=map.image)

################## Main #####################
window = Tk()

map = Map()

############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: get_directory(map, canvas, window), text="Choisir zone de navigation").pack(side="left")
exit_button = Button(button_frame, command=lambda: exit(), text="Exit").pack(side="left")

#########################################

############ Canvas creation ############
canvas = Canvas(window, width=1800, height=1000)
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

window.mainloop()


