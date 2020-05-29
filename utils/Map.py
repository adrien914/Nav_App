from tkinter import Tk, Button, Entry, Label, Canvas
from PIL import Image, ImageTk
import json
import math


class Map:
    directory = None
    settings = {}
    image = None
    canvas = None
    line_base = None
    line_end = None
    last_line_id = None
    longitude_text = None
    latitude_text = None
    image_id = None
    vitesse = None
    distance = None
    travel_time = None
    coefficient_maree = None
    history_buttons = []
    etape = "tracé"
    sous_etape = "longitude_top_left_corner"
    path_delimitation = []
    courants = []
    segments_done = 0
    somme_des_courants = None
    boutons_heures = []
    current_button = None
    maps_paths = []
    current_button_index = None
    foreground_items = []
    ligne_cap = None
    cap = None
    waypoints = []
    ligne_decalage_ids = []
    instruction = None
    def load_map(self, directory: str, window: Tk) -> bool:
        """
        This function loads the map's essential variables from the chosen directory
        :param directory: path of the directory
        :return: a bool that signifies success of failure
        """
        try:
            self.directory = directory  # set the map directory to the chosen directory ( full path )
            with open(directory + "/settings.json") as settings_file:
                self.settings = json.load(settings_file)
            image = Image.open(directory + "/" + self.settings["pm_file"])
            ratio = 2147/3087
            #width = 2750
            width = int(window.winfo_screenwidth() * 150/100)
            image = image.resize((width, int(width*ratio)), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image=image)
            self.image = self.image._PhotoImage__photo.subsample(2)
            return True
        except Exception as e:
            print(e)
            return False

    def change_map(self, path, window):
        image = Image.open(path)
        old_width = 3087
        old_height = 2147
        ratio = 2147 / 3087
        width = int(window.winfo_screenwidth() * 150/100)
        #width = 2750
        image = image.resize((width, int(width * ratio)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image=image)
        self.image = self.image._PhotoImage__photo.subsample(2)
        return True

    def show_history(self, canvas, window):
        from utils.Popup import Popup
        from utils.DirectoryManager import DirectoryManager
        for button in self.history_buttons:
            canvas.delete(button)
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
            i = 0
            for entry in history:
                i += 1
                button = Button(window, command=lambda entry=entry: DirectoryManager.get_directory(self, canvas, window,
                                                                                                   entry["path"]),
                                text=entry["name"])
                button.focus_set()
                edit_history_name_button = Button(window,
                                                  command=lambda entry=entry: Popup.change_name_popup(entry["path"], self, canvas, window),
                                                  text="editer")
                history_window = canvas.create_window(900, 250 + 30 * i, anchor="center", window=button)
                button_bounds = canvas.bbox(history_window)
                edit_window = canvas.create_window(button_bounds[2], button_bounds[3], anchor="sw",
                                                   window=edit_history_name_button)
                self.history_buttons.append(history_window)
                self.history_buttons.append(edit_window)

    def is_within_bounds(self, x: int, y: int) -> bool:
        """
        This function gets a x and y coordinates and checks if they are within boundaries of the map
        :param x: the x coordinate
        :param y: the y coordinate
        :return: True if it is within boundaries, False if not
        """
        upper_left_x, upper_left_y = self.settings["upper_left_corner"]
        bottom_right_x, bottom_right_y = self.settings["bottom_right_corner"]
        if upper_left_x < x < bottom_right_x and upper_left_y < y < bottom_right_y:
            return True
        else:
            return False

    def get_longitude(self, x):
        x = x - self.settings["upper_left_corner"][0]
        ratio_pixel, ratio_minutes = self.settings["ratio_pixel_minutes"]
        # Calcul de la longitude par rapport aux pixels:
        #  longitude_top_left_corner = longitude en haut a gauche de la carte en minutes
        # ratio_pixel / ratio_minutes -> nombre de pixels par minutes exprimés en radian
        # x -> position en pixels sur la carte
        # on divise par 60 pour avoir le tout en minutes
        longitude = (self.settings["longitude_top_left_corner"] - (ratio_pixel / ratio_minutes) * x) / 60
        degres_longitude = int(longitude)  # les degrès de longitude sont la partie entière de la longitude
        minutes_longitude = int((longitude - int(longitude)) * 60)  # les minutes de la longitude sont sa partie décimale fois 60
        longitude = str(degres_longitude) + "." + str(minutes_longitude)  # formatage du texte
        return longitude

    def get_latitude(self, y):
        y = abs(y - self.settings["upper_left_corner"][1])
        position_y = self.settings["nombre_pixels_equateur_latitude_de_reference"] - y + self.settings[
            "decalage_pixels_latitude"]
        # multiplier = nombre de pixels / nombre de minutes de latitude
        latitude = math.degrees(2 * math.atan(math.exp(position_y / self.settings["multiplier"])) - math.pi / 2)
        minutes_latitude = int((latitude - int(latitude)) * 60)
        latitude = str(int(latitude)) + "." + str(minutes_latitude)
        return latitude



    def write_coordinates(self, canvas, event, longitude, latitude):
        self.latitude_text = canvas.create_text(event.x + 10, event.y + 25,
                                               text="{}".format(latitude),
                                               fill="green",
                                               font=("Helvetica", "16")
                                               )  # latitude text
        self.longitude_text = canvas.create_text(event.x + 63, event.y + 25,
                                                text=", {}".format(longitude),
                                                fill="red",
                                                font=("Helvetica", "16")
                                                )  # longitude text

    def show_speed_distance(self, canvas):
        x, y = self.line_base
        x1, y1 = self.line_end  # coordonnées des extrémités du vecteur
        canvas.create_rectangle(x, y, x1, y1)
        distance_pixels = math.sqrt(math.pow((x1 - x), 2) + math.pow((y1 - y), 2))  # pythagore pour avoir la distance en pixels
        distance = distance_pixels * self.settings["ratio_pixel_nautical_miles"]  # Conversion de la longeur en pixels en miles nautiques
        self.distance = round(distance, 2)
        text = canvas.create_text(self.settings["bottom_right_corner"][0] + 120,
                           self.settings["upper_left_corner"][1] + 30,
                           text="distance: {} miles".format(self.distance),
                           fill="red",
                           font=("Helvetica", "15")
                           )
        self.foreground_items.append(text)
        self.travel_time = round(self.distance / self.vitesse, 2)
        cote_x = x1 - x
        cote_y = y1 - y
        cote_x_split = cote_x / self.travel_time
        cote_y_split = cote_y / self.travel_time
        for i in range(1, int(self.travel_time) + 1):
            self.path_delimitation.append(canvas.create_oval(x + i * cote_x_split - 5,
                               y + i * cote_y_split - 5,
                               x + i * cote_x_split + 5,
                               y + i * cote_y_split + 5,
                               fill="red"))
        self.path_delimitation.append(canvas.create_oval(x + self.travel_time * cote_x_split - 5,
                           y + self.travel_time * cote_y_split - 5,
                           x + self.travel_time * cote_x_split + 5,
                           y + self.travel_time * cote_y_split + 5,
                           fill="red"))
        print(cote_x_split, cote_y_split)
        text = canvas.create_text(self.settings["bottom_right_corner"][0] + 120,
                           self.settings["upper_left_corner"][1] + 60,
                           text="temps trajet = {} heures".format(self.travel_time),
                           fill="red",
                           font=("Helvetica", "15")
                           )
        self.foreground_items.append(text)

    def calculer_courant_final(self, canvas: Canvas):
        self.somme_des_courants = {"projection_x": 0, "projection_y": 0}
        for courant in self.courants:
            x, y = courant["line_base"]
            x1, y1 = courant["line_end"]
            distance_pixels = math.sqrt(
                math.pow((x1 - x), 2) + math.pow((y1 - y), 2))  # pythagore pour avoir la distance en pixels
            distance = distance_pixels * self.settings[
                "ratio_pixel_nautical_miles"]  # Conversion de la longeur en pixels en miles nautiques
            ratio = distance / courant["vitesse_reelle"]
            projection_x = (x1 - x) / ratio
            courant["projection_x"] = projection_x
            projection_y = (y1 - y) / ratio
            courant["projection_y"] = projection_y
            self.somme_des_courants["projection_x"] += projection_x
            self.somme_des_courants["projection_y"] += projection_y
        x, y = self.line_base
        x1, y1 = self.line_end
        new_x = x + self.somme_des_courants["projection_x"]
        new_y = y + self.somme_des_courants["projection_y"]
        canvas.create_line(new_x, new_y, x1, y1, dash=(3, 5), width=2, fill="green")  # route cap
        projection_x = x1 - new_x
        projection_y = y1 - new_y
        self.ligne_cap = [projection_x, projection_y]
        angle = math.degrees(math.atan(projection_y / projection_x))
        if projection_x < 0:
            self.cap = int(270 + angle)
        else:
            self.cap = int(90 + angle)
        text = canvas.create_text(self.settings["bottom_right_corner"][0] + 110, self.settings["upper_left_corner"][1] + 180,
                                  text="cap a suivre: {}".format(self.cap),
                                  fill="red",
                                  font=("Helvetica", "15")
                                  )  # on l'écrit à l'écran
        self.foreground_items.append(text)
        self.calculer_route_fond(canvas)

    def calculer_route_fond(self, canvas: Canvas):
        x_base = self.line_base[0]
        y_base = self.line_base[1]
        projection_x = self.ligne_cap[0] / len(self.path_delimitation)
        projection_y = self.ligne_cap[1] / len(self.path_delimitation)
        for i in range(0, len(self.path_delimitation)):
            projection_x_courant = self.courants[i]["projection_x"]
            projection_y_courant = self.courants[i]["projection_y"]
            self.ligne_cap[0] = self.ligne_cap[0] - self.ligne_cap[0] / len(self.path_delimitation)
            self.ligne_cap[1] = self.ligne_cap[1] - self.ligne_cap[1] / len(self.path_delimitation)
            new_x = x_base + projection_x + projection_x_courant
            new_y = y_base + projection_y + projection_y_courant
            canvas.create_line(x_base, y_base, new_x, new_y, width=2, fill="blue", arrow="last", arrowshape=(8, 10, 7))
            x_base = new_x
            y_base = new_y
            self.waypoints.append((self.get_latitude(y_base), self.get_longitude(x_base)))
        self.write_waypoints(canvas)

    def write_waypoints(self, canvas):
        i = 0
        for waypoint in self.waypoints:
            text = canvas.create_text(self.settings["bottom_right_corner"][0] + 110,
                                      self.settings["upper_left_corner"][1] + 240 + i * 55,
                                      text="Waypoint {}: \n{}".format(i + 1, waypoint),
                                      fill="red",
                                      font=("Helvetica", "15")
                                      )  # on l'écrit à l'écran
            self.foreground_items.append(text)
            i += 1

    def calibrer(self):
        from utils.Popup import Popup
        self.etape = "calibrage"
        Popup.ask_longitude_top_left_corner(self)

    def show_instruction(self, text):
        if self.instruction:
            self.canvas.delete(self.instruction)
        self.instruction = self.canvas.create_text(self.settings["upper_left_corner"][0] - 150,
                                                 self.settings["upper_left_corner"][1] + 30,
                                                 text=text,
                                                 fill="red",
                                                 font=("Helvetica", "13")
                                                 )

    def reset(self):
        self.directory = None
        self.settings = {}
        self.image = None
        self.line_base = None
        self.line_end = None
        self.last_line_id = None
        self.longitude_text = None
        self.latitude_text = None
        self.image_id = None
        self.vitesse = None
        self.distance = None
        self.travel_time = None
        self.coefficient_maree = None
        self.history_buttons = []
        self.etape = "tracé"
        self.path_delimitation = []
        self.courants = []
        self.segments_done = 0
        self.somme_des_courants = None
        self.boutons_heures = []
        self.current_button = None
        self.maps_paths = []
        self.current_button_index = None
        self.foreground_items = []
        self.ligne_cap = None
        self.cap = None
        self.waypoints = []