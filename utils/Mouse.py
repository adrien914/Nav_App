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
                print("line length: {}x, {}y".format(map.line_end[0] - map.line_base[0],
                                                     map.line_end[1] - map.line_base[1]))

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
            if map.text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.text)
            if map.line_base and not map.line_end:  # if the user started drawing a line
                x1, y1 = map.line_base  # assign the position of the beggining of the line to x1 and y1
                if map.last_line_id:  # if there's already a line delete it so we can redraw it
                    canvas.delete(map.last_line_id)
                map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red")  # draw the line
            latitude = (event.x - map.settings["upper_left_corner"][0]) * map.settings["latitude_multiplier"]
            longitude = (event.y - map.settings["upper_left_corner"][1]) * map.settings["longitude_multiplier"]
            map.text = canvas.create_text(event.x + 30, event.y - 10,
                                          text="{}, {}".format(latitude, longitude),
                                          fill="green")  # latitude - longitude text
        elif map.image and not map.is_within_bounds(event.x, event.y):
            if map.text:
                canvas.delete(map.text)