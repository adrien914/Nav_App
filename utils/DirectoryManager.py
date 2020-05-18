import json
from utils.Map import Map
import glob
from tkinter import Button, Canvas, filedialog

class DirectoryManager():


    @staticmethod
    def write_history(directory):
        with open("map_history.json", 'w+') as file:
            try:
                history = json.load(file)
            except Exception:
                history = []
                pass
            if history:
                if directory not in [entry["path"] for entry in history]:
                    history.append({"path": directory, "name": directory.split("/")[-1]})
                    file.write(json.dumps(history))
            else:
                history = [{"path": directory, "name": directory.split("/")[-1]}]
                file.write(json.dumps(history))

    @staticmethod
    def get_directory(map: Map, canvas: Canvas, window, directory=None):
        if not directory:
            directory = filedialog.askdirectory()
        if directory:
            DirectoryManager.write_history(directory)
            map.load_map(directory)
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if map.image_id:
                canvas.delete(map.image_id)
            map.image_id = canvas.create_image(width/2, height/2, anchor="center", image=map.image)
            files = glob.glob(directory + "/*.jpg")
            for avant_pm in range(1, 7):
                button = Button(window, text=str(7 - avant_pm) + "h avant pleine mer",
                                command=lambda avant_pm=avant_pm: DirectoryManager.change_map(map, canvas, files[len(files) - 2 - (2 * (avant_pm - 1))]), anchor="w")
                canvas.create_window(40, 250 + 30 * avant_pm, anchor="nw", window=button)
            button = Button(window, text="pleine mer", command=lambda: DirectoryManager.change_map(map, canvas, files[-1]), anchor="w")
            canvas.create_window(60, 250 + 30 * 7, anchor="nw", window=button)
            for apres_pm in range(1, 7):
                button = Button(window, text=str(apres_pm) + "h après pleine mer", command=lambda apres_pm=apres_pm: DirectoryManager.change_map(map, canvas, files[2 * (apres_pm - 1)]), anchor="w")
                canvas.create_window(40, 250 + 30 * (apres_pm + 7), anchor="nw", window=button)
            for history_window in map.history_buttons:
                canvas.delete(history_window)

    @staticmethod
    def change_map(map: Map, canvas: Canvas, path: str):
        if path:
            map.change_map(path)
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if map.image_id:
                canvas.delete(map.image_id)
            map.image_id = canvas.create_image(width / 2, height / 2, anchor="center", image=map.image)
            canvas.tag_raise(map.last_line_id)
            for oval in map.path_delimitation:
                canvas.tag_raise(oval)