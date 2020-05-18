from tkinter import Tk, Button, Entry, Label
from utils.Map import Map

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
        if map.etape == "tracé":
            if map.is_within_bounds(event.x, event.y):
                if not map.line_base or map.line_end:  # if it's our first click or a line has already been drawn
                    map.line_base = (event.x, event.y)  # Set the line base to the clicked coordinates
                    map.line_end = None  # set the line end to None because there could already be a drawn line
                elif map.line_base and not map.line_end:  # else if the line base is already selected
                    map.line_end = (event.x, event.y)  # set the line end to the clicked cooordinates
                    Mouse.get_boat_speed(map, canvas)
                    map.show_speed_distance(canvas)
        else:
            Mouse.get_courant(event, map, canvas)

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
        if map.etape == "tracé":
            if map.image and map.is_within_bounds(event.x, event.y):
                if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                    canvas.delete(map.longitude_text)
                    canvas.delete(map.latitude_text)
                if map.line_base and not map.line_end:  # if the user started drawing a line
                    x1, y1 = map.line_base  # assign the position of the beggining of the line to x1 and y1
                    if map.last_line_id:  # if there's already a line delete it so we can redraw it
                        canvas.delete(map.last_line_id)
                    map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red")  # draw the line

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
        else:
            if map.image and map.is_within_bounds(event.x, event.y):
                try:
                    if map.courants[-1]["line_base"] and not map.courants[-1]["line_end"]:  # if the user started drawing a line
                        x1, y1 = map.courants[-1]["line_base"]  # assign the position of the beggining of the line to x1 and y1
                        if map.courants[-1]["line_id"]:  # if there's already a line delete it so we can redraw it
                            canvas.delete(map.courants[-1]["line_id"])
                        map.courants[-1]["line_id"] = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red")  # draw the line
                except:
                    pass

    @staticmethod
    def get_boat_speed(map, canvas):
        popup = Tk()
        text = Label(popup, text="Veuillez entrer la vitesse du bateau", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        Button(popup, command=lambda: Mouse.get_speed_value(entry, popup, map, canvas), text="Confirmer").pack(side="top")
        popup.mainloop()
        Mouse.get_coeff_maree(map, canvas)

    @staticmethod
    def get_coeff_maree(map, canvas):
        popup = Tk()
        text = Label(popup, text="Veuillez entrer le coefficient de marée", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        Button(popup, command=lambda: Mouse.get_coeff_maree_value(entry, popup, map, canvas), text="Confirmer").pack(
            side="top")
        popup.mainloop()

    @staticmethod
    def get_speed_value(input, popup, map, canvas):
        value = input.get()
        map.vitesse = int(value)
        canvas.create_text( map.settings["bottom_right_corner"][0] + 110, map.settings["upper_left_corner"][1],
                            text="speed = {} knots".format(map.vitesse),
                            fill="red",
                            font=("Helvetica", "15")
                            )
        popup.quit()
        popup.destroy()

    @staticmethod
    def get_coeff_maree_value(input, popup, map, canvas):
        value = input.get()
        map.coefficient_maree = int(value)
        canvas.create_text(map.settings["bottom_right_corner"][0] + 120, map.settings["upper_left_corner"][1] + 90,
                           text="coefficient de marée = {}".format(map.coefficient_maree),
                           fill="red",
                           font=("Helvetica", "15")
                           )
        map.etape = "courant"
        popup.quit()
        popup.destroy()


    @staticmethod
    def get_courant(event, map, canvas):
        courant = {"line_base": None, "line_end": None, "vives_eaux": None, "mortes_eaux": None, "line_id": None, "vitesse_reelle": None}
        try:
            if map.courants[-1]["line_end"]:
                map.courants.append(courant)
        except Exception:
            map.courants.append(courant)
        if map.is_within_bounds(event.x, event.y):
            if not map.courants[-1]["line_base"] or map.courants[-1]["line_end"]:  # if it's our first click or a line has already been drawn
                print(map.courants)
                map.courants[-1]["line_base"] = (event.x, event.y)  # Set the line base to the clicked coordinates
                map.courants[-1]["line_end"] = None  # set the line end to None because there could already be a drawn line
            elif map.courants[-1]["line_base"] and not map.courants[-1]["line_end"]:  # else if the line base is already selected
                map.courants[-1]["line_end"] = (event.x, event.y)  # set the line end to the clicked cooordinates
                canvas.itemconfig(map.path_delimitation[map.segments_done], fill="green")
                map.segments_done += 1
                Mouse.get_vitesse_courant(map, canvas)


    @staticmethod
    def get_vitesse_courant(map, canvas):
        popup = Tk()
        entries = []
        text = Label(popup, text="Veuillez entrer les vitesses du courant", font=("Helvetica", 20),
                     foreground="red").pack(
            side="top")
        Label(popup, text="En vives eaux", font=("Helvetica", 10),
              foreground="black").pack(
            side="top")
        entries.append(Entry(popup, width=20))
        entries[0].pack(side="top")
        Label(popup, text="En mortes eaux", font=("Helvetica", 10),
              foreground="black").pack(
            side="top")
        entries.append(Entry(popup, width=20))
        entries[1].pack(side="top")
        Button(popup, command=lambda: Mouse.set_vitesse_courant(entries, popup, map, canvas), text="Confirmer").pack(
            side="top")
        popup.mainloop()

    @staticmethod
    def set_vitesse_courant(entries, popup, map: Map, canvas):
        vives_eaux = map.courants[-1]["vives_eaux"] = int(entries[0].get())
        mortes_eaux = map.courants[-1]["mortes_eaux"] = int(entries[1].get())
        map.courants[-1]["vitesse_reelle"] = mortes_eaux + (((vives_eaux - mortes_eaux) * (map.coefficient_maree - 45)) / 50)
        popup.quit()
        popup.destroy()