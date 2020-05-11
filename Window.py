from tkinter import Tk, Button, Canvas, filedialog, Frame
from utils.Mouse import Mouse
from utils.Map import Map

def get_directory(map: Map, canvas: Canvas):
    directory = filedialog.askdirectory()
    if directory:
        map.load_map(directory)
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if map.image_id:
            canvas.delete(map.image_id)
        map.image_id = canvas.create_image(width/2, height/2, anchor="center", image=map.image)

def get_file(map: Map, canvas: Canvas):
    path = filedialog.askopenfile()
    if path:
        map.change_map(path.name)
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if map.image_id:
            canvas.delete(map.image_id)
        map.image_id = canvas.create_image(width/2, height/2, anchor="center", image=map.image)

################## Main
window = Tk()

map = Map()

############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: get_directory(map, canvas), text="Choisir zone de navigation").pack(side="left")
file_button = Button(button_frame, command=lambda: get_file(map, canvas), text="Changer de carte").pack(side="left")
exit_button = Button(button_frame, command=lambda: exit(), text="Exit").pack(side="left")
#########################################

############ Canvas creation ############
canvas = Canvas(window, width=1800, height=1000)
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

window.mainloop()