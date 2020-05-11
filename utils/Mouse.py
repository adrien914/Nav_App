import math
from tkinter.font import Font

class Mouse():
    """
        this class contains the different methods related to mouse actions
    """
    @staticmethod
    def click(event, map, canvas) -> None:
        """
        This method plays when the user left clicks on the map with his mouse
        it's used to select the lines coordinates
        :param event: the mouse event
        :param map: the map currently shown
        :param canvas: the canvas currently drawn
        :return: None
        """
        if map.is_within_bounds(event.x, event.y):
            if not map.line_base or map.line_end:  # if it's our first click or a line has already been drawn
                map.line_base = (event.x, event.y)  # Set the line base to the clicked coordinates
                map.line_end = None  # set the line end to None because there could already be a drawn line
            elif map.line_base and not map.line_end:  # else if the line base is already selected
                map.line_end = (event.x, event.y)  # set the line end to the clicked cooordinates

    @staticmethod
    def mouse_moved(event, map, canvas) -> None:
        """
        This method plays when the users moves his mouse on the map
        it's used to preview the lines while they are being drawn
        :param event: the mouse event
        :param map: the map currently shown
        :param canvas: the canvas currently drawn
        :return: None
        """
        if map.image and map.is_within_bounds(event.x, event.y):
            if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
            if map.line_base and not map.line_end:  # if the user started drawing a line
                x1, y1 = map.line_base  # assign the position of the beggining of the line to x1 and y1
                if map.last_line_id:  # if there's already a line delete it so we can redraw it
                    canvas.delete(map.last_line_id)
                map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red")  # draw the line
                line_bounds = canvas.bbox(map.last_line_id)
                length = math.sqrt(math.pow((line_bounds[2] - line_bounds[0]), 2) + math.pow((line_bounds[3] - line_bounds[1]), 2)) # Pythagore pour la longeur de la ligne
                length *= map.settings["ratio_pixel_nautical_miles"]  # Conversion de la longeur en pixels en miles nautiques
                print("line length: {}".format(length))
            ################ Calcul de la longitude ################
            x = event.x - map.settings["upper_left_corner"][0]  # We get x value and substract the number of pixels before the map to it to get the position on the map
            longitude = map.get_longitude(x)
            ########################################################

            ################ Calcul de la latitude #################
            y = abs(event.y - map.settings["upper_left_corner"][1])
            latitude = map.get_latitude(y)
            ########################################################
            map.write_coordinates(canvas, event, longitude, latitude)
        elif map.image and not map.is_within_bounds(event.x, event.y):
            if map.longitude_text and map.latitude_text:
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
