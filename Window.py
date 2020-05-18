import json
from tkinter import Tk, Button, Canvas, Label, Frame, Entry
from utils.Mouse import Mouse
from utils.Map import Map
from utils.DirectoryManager import DirectoryManager

def change_name_popup(path):
    popup = Tk()
    text = Label(popup, text="Entrez le nouveau nom", font=("Helvetica", 20), foreground="red").pack(
        side="top")
    entry = Entry(popup, width=20)
    entry.pack(side="top")
    Button(popup, command=lambda: change_name(entry, popup, path), text="Confirmer").pack(side="top")
    popup.mainloop()
    Mouse.get_coeff_maree(map, canvas)

def change_name(input, popup, path):
    value = input.get()
    found = False
    i = 0
    history = []
    with open("map_history.json", 'w+') as file:
        history = json.load(file)
        for entry in history:
            if entry["path"] == path:
                found = True
                break
            i += 1
        if found:
            history[i]["name"] = value
            file.write(json.dumps(history))

    popup.quit()
    popup.destroy()

################## Main #####################
window = Tk()

map = Map()

############ Buttons frame ##############
button_frame = Frame(window)
button_frame.pack(side="top")
directory_button = Button(button_frame, command=lambda: DirectoryManager.get_directory(map, canvas, window), text="Choisir zone de navigation").pack(side="left")
exit_button = Button(button_frame, command=lambda: exit(), text="Exit").pack(side="left")

#########################################

############ Canvas creation ############
canvas = Canvas(window, width=1800, height=1000)
canvas.pack(side="bottom")
canvas.bind("<Button-1>", lambda event: Mouse.click(event, map, canvas))
canvas.bind("<Motion>",  lambda event: Mouse.mouse_moved(event, map, canvas))
#########################################

with open("map_history.json", 'r') as file:
    try:
        history = json.load(file)
    except Exception:
        history = []
        pass
    i = 0
    for entry in history:
        i += 1
        button = Button(window, command=lambda entry=entry: DirectoryManager.get_directory(map, canvas, window, entry["path"]), text=entry["name"])
        edit_history_name_button = Button(window, command=lambda entry=entry: change_name_popup(entry["path"]), text="editer")
        history_window = canvas.create_window(900, 250 + 30 * i, anchor="center", window=button)
        edit_window = canvas.create_window(1050, 250 + 30 * i, anchor="center", window=edit_history_name_button)
        map.history_buttons.append(history_window)
        map.history_buttons.append(edit_window)

window.mainloop()


