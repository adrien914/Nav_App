import json
from PIL import Image, ImageTk

class Map:
    directory = None
    settings = {}
    image = None
    line_base = None
    line_end = None
    last_line_id = None
    text = None

    def load_map(self, directory: str) -> bool:
        """
        This function loads the map's essential variables from the chosen directory
        :param directory: path of the directory
        :return: a bool that signifies success of failure

        :type directory: str
        :rtype: bool
        """
        self.directory = directory  # set the map directory to the chosen directory ( full path )
        with open(directory + "/settings.json") as settings_file:
            self.settings = json.load(settings_file)
        image = Image.open(directory + "/" + self.settings["pm_file"])
        old_width = 3087
        old_height = 2147
        ratio = 2147/3087
        width = 2750
        print(int(width/ratio))
        image = image.resize((width, int(width*ratio)), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image=image)
        self.image = self.image._PhotoImage__photo.subsample(2)
        return True
        # except Exception as e:
        #     print(e)
        #     return False