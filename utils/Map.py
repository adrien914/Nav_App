from PIL import Image, ImageTk
import json
import math

class Map:
    directory = None
    settings = {}
    image = None
    line_base = None
    line_end = None
    last_line_id = None
    longitude_text = None
    latitude_text = None
    image_id = None

    def load_map(self, directory: str) -> bool:
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
            old_width = 3087
            old_height = 2147
            ratio = 2147/3087
            width = 2750
            image = image.resize((width, int(width*ratio)), Image.ANTIALIAS)
            self.image = ImageTk.PhotoImage(image=image)
            self.image = self.image._PhotoImage__photo.subsample(2)
            return True
        except Exception as e:
            print(e)
            return False

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
        position_y = self.settings["nombre_pixels_equateur_latitude_de_reference"] - y + self.settings[
            "decalage_pixels_latitude"]
        latitude = math.degrees(2 * math.atan(math.exp(position_y / self.settings["multiplier"])) - math.pi / 2)
        minutes_latitude = int((latitude - int(latitude)) * 60)
        latitude = str(int(latitude)) + "." + str(minutes_latitude)
        return latitude

    def change_map(self, path):
        image = Image.open(path)
        old_width = 3087
        old_height = 2147
        ratio = 2147 / 3087
        width = 2750
        image = image.resize((width, int(width * ratio)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image=image)
        self.image = self.image._PhotoImage__photo.subsample(2)
        return True

    def write_coordinates(self, canvas, event, longitude, latitude):
        self.longitude_text = canvas.create_text(event.x + 10, event.y + 25,
                                                text=str(longitude),
                                                fill="red",
                                                font=("Helvetica", "16")
                                                )  # longitude text
        self.latitude_text = canvas.create_text(event.x + 63, event.y + 25,
                                               text=", {}".format(latitude),
                                               fill="green",
                                               font=("Helvetica", "16")
                                               )  # latitude text