import json
from utils.Map import Map
import glob
from tkinter import Button, Canvas, filedialog

class DirectoryManager():


    @staticmethod
    def write_history(directory):
        try:
            open("map_history.json", 'r+')
        except FileNotFoundError:
            open("map_history.json", "w+")
        with open("map_history.json", 'r+') as file:
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
            if map.image_id:
                map.reset()
            DirectoryManager.write_history(directory)
            map.load_map(directory, window)
            map.canvas = canvas
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if map.image_id:
                canvas.delete(map.image_id)
            map.image_id = canvas.create_image(width/2, height/2, anchor="center", image=map.image)
            bbox = canvas.bbox(map.image_id)
            map.settings["upper_left_corner"] = [bbox[0] + map.settings["decalage_x"], bbox[1] + map.settings["decalage_y"]]
            map.settings["bottom_right_corner"] = [bbox[2] - map.settings["decalage_x_bottom"], bbox[3] - map.settings["decalage_y_bottom"]]
            map.show_instruction("Tracez la route voulue")
            files = glob.glob(directory + "/*.jpg")
            for avant_pm in range(1, 7):
                button = Button(window, text=str(7 - avant_pm) + "h avant pleine mer",
                                command=lambda avant_pm=avant_pm: DirectoryManager.change_map(map, canvas, files[len(files) - 2 - (2 * (avant_pm - 1))], avant_pm - 1, window), anchor="w")
                map.maps_paths.append(files[len(files) - 2 - (2 * (avant_pm - 1))])
                map.boutons_heures.append(button)
                canvas.create_window(40, 250 + 30 * avant_pm, anchor="nw", window=button)
            button = Button(window, text="pleine mer", command=lambda: DirectoryManager.change_map(map, canvas, files[-1], 6, window), anchor="w")
            map.maps_paths.append(files[-1])
            map.boutons_heures.append(button)
            canvas.create_window(60, 250 + 30 * 7, anchor="nw", window=button)
            for apres_pm in range(1, 7):
                button = Button(window, text=str(apres_pm) + "h après pleine mer",
                                command=lambda apres_pm=apres_pm: DirectoryManager.change_map(map, canvas, files[2 * (apres_pm - 1)], 6 + apres_pm, window),
                                anchor="w")
                map.maps_paths.append(files[2 * (apres_pm - 1)])
                map.boutons_heures.append(button)
                canvas.create_window(40, 250 + 30 * (apres_pm + 7), anchor="nw", window=button)
            print(map.maps_paths)
            for history_window in map.history_buttons:
                canvas.delete(history_window)

    @staticmethod
    def change_map(map: Map, canvas: Canvas, path: str, button_index: int, window):
        if path:
            map.change_map(path, window)
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            if map.image_id:
                canvas.delete(map.image_id)
            map.image_id = canvas.create_image(width / 2, height / 2, anchor="center", image=map.image)
            print(canvas.bbox(map.image_id))
            if map.last_line_id:
                canvas.tag_raise(map.last_line_id)
            for oval in map.path_delimitation:
                canvas.tag_raise(oval)
            if map.current_button:
                map.current_button.configure(bg="white")
            map.boutons_heures[button_index].configure(bg="gray")
            print(map.boutons_heures[button_index])
            map.current_button = map.boutons_heures[button_index]
            map.current_button_index = button_index
            if map.etape == "tracé":
                map.show_instruction("Tracez la route voulue")
            elif map.etape == "courant":
                map.show_instruction("Choisissez une heure de départ\nTracez les courants du trajet")
            for foreground_item in map.foreground_items:
                canvas.tag_raise(foreground_item)