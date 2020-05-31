from tkinter import Tk, Button, Entry, Label, Canvas
from utils.Map import Map
from utils.Popup import Popup
from utils.DirectoryManager import DirectoryManager

class Mouse():
    """
        this class contains the different methods related to mouse actions
    """
    @staticmethod
    def click(event, map, canvas, window) -> None:
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
                Mouse.trace_ligne(map, event, canvas)
        elif map.etape == "calibrage":
            if map.sous_etape == "ratio_pixel_minutes":
                Mouse.trace_ligne(map, event, canvas)
            elif map.sous_etape == "ratio_pixel_nautical_miles":
                Mouse.trace_ligne(map, event, canvas)
            elif map.sous_etape == "decalage_x_y":
                Mouse.calculer_decalage(event, map, canvas)
            elif map.sous_etape == "decalage_pixels_latitude":
                Mouse.calculer_decalage_latitude(event, map, canvas)
        else:
            Mouse.get_courant(event, map, canvas, window)

    @staticmethod
    def trace_ligne(map: Map, event, canvas: Canvas):
        if not map.line_base or map.line_end:  # if it's our first click or a line has already been drawn
            map.line_base = (event.x, event.y)  # Set the line base to the clicked coordinates
            map.line_end = None  # set the line end to None because there could already be a drawn line
        elif map.line_base and not map.line_end:  # else if the line base is already selected
            map.line_end = (event.x, event.y)  # set the line end to the clicked cooordinates
            if map.etape == "tracé":
                Popup.get_boat_speed(map, canvas)
                map.show_speed_distance(canvas)
            elif map.etape == "calibrage":
                if map.sous_etape == "ratio_pixel_minutes":
                    Popup.ask_number_of_minutes_popup(map)
                    if map.last_line_id:
                        canvas.delete(map.last_line_id)
                elif map.sous_etape == "ratio_pixel_nautical_miles":
                    print("line_id", map.last_line_id)
                    if map.last_line_id:
                        canvas.delete(map.last_line_id)
                    Popup.ask_number_of_minutes_popup(map)

    @staticmethod
    def calculer_decalage(event, map: Map, canvas: Canvas):
        x, y, _, _ = canvas.bbox(map.image_id)
        map.settings["decalage_x"] = event.x - x
        map.settings["decalage_y"] = event.y - y
        map.settings["decalage_x_bottom"] = event.x - x
        map.settings["decalage_y_bottom"] = event.y - y
        map.sous_etape = "decalage_pixels_latitude"
        map.show_instruction("Veuillez tracer le décalage de latitude (coin supérieur droit)")
        for line in map.ligne_decalage_ids:
            canvas.delete(line)

    @staticmethod
    def calculer_decalage_latitude(event, map: Map, canvas: Canvas):
        x, y, _, _ = canvas.bbox(map.image_id)
        map.settings["decalage_pixels_latitude"] = event.y - y
        if map.last_line_id:
            canvas.delete(map.last_line_id)
        map.save_settings()
        map.etape = "tracé"
        map.show_instruction("Tracez la route voulue")

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
            Mouse.show_trace(map, event, canvas)
        elif map.etape == "calibrage":
            if map.sous_etape == "ratio_pixel_minutes" or "ratio_pixel_nautical_miles":
                Mouse.show_trace_ratio_pixel_minutes(map, event, canvas)
            if map.sous_etape == "decalage_x_y":
                Mouse.show_trace_decalage_x_y(map, event, canvas)
            if map.sous_etape == "decalage_pixels_latitude":
                Mouse.show_trace_decalage_pixels_latitude(map, event, canvas)
        else:
            if map.image and map.is_within_bounds(event.x, event.y):
                try:
                    if map.courants[-1]["line_base"] and not map.courants[-1]["line_end"]:  # if the user started drawing a line
                        x1, y1 = map.courants[-1]["line_base"]  # assign the position of the beggining of the line to x1 and y1
                        if map.courants[-1]["line_id"]:  # if there's already a line delete it so we can redraw it
                            canvas.delete(map.courants[-1]["line_id"])
                        map.courants[-1]["line_id"] = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red", arrow="last", arrowshape=(8, 10, 7))  # draw the line
                except:
                    pass

    @staticmethod
    def show_trace(map, event, canvas):
        if map.image and map.is_within_bounds(event.x, event.y):
            if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
            if map.line_base and not map.line_end:  # if the user started drawing a line
                x1, y1 = map.line_base  # assign the position of the beggining of the line to x1 and y1
                if map.last_line_id:  # if there's already a line delete it so we can redraw it
                    canvas.delete(map.last_line_id)
                map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red", arrow="last",
                                                      arrowshape=(8, 10, 7))  # draw the line

            ################ Calcul de la longitude ################
            longitude = map.get_longitude(event.x)
            ########################################################

            ################ Calcul de la latitude #################
            latitude = map.get_latitude(event.y)
            ########################################################
            map.write_coordinates(canvas, event, longitude, latitude)
        elif map.image and not map.is_within_bounds(event.x, event.y):
            if map.longitude_text and map.latitude_text:
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)

    @staticmethod
    def show_trace_ratio_pixel_minutes(map, event, canvas):
        if map.image and map.is_within_bounds(event.x, event.y):
            if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
            if map.line_base and not map.line_end:  # if the user started drawing a line
                x1, y1 = map.line_base  # assign the position of the beggining of the line to x1 and y1
                if map.last_line_id:  # if there's already a line delete it so we can redraw it
                    canvas.delete(map.last_line_id)
                map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red", arrow="last",
                                                      arrowshape=(8, 10, 7))  # draw the line

    @staticmethod
    def show_trace_decalage_x_y(map: Map, event, canvas: Canvas):
        x, y, _, _ = canvas.bbox(map.image_id)
        if map.image:
            if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
            vertical_line = canvas.create_line(event.x, y, event.x, event.y, fill="red")
            horizontal_line = canvas.create_line(x, event.y, event.x, event.y, fill="red")
            for line in map.ligne_decalage_ids:
                canvas.delete(line)
            map.ligne_decalage_ids = [vertical_line, horizontal_line]

    @staticmethod
    def show_trace_decalage_pixels_latitude(map: Map, event, canvas: Canvas):
        _, y, x, _ = canvas.bbox(map.image_id)
        x -= map.settings["decalage_x_bottom"]
        y += map.settings["decalage_y"]
        if map.image:
            if map.longitude_text and map.latitude_text:  # if there was already a text for the position delete it so we can redraw it
                canvas.delete(map.longitude_text)
                canvas.delete(map.latitude_text)
            if map.last_line_id:
                canvas.delete(map.last_line_id)
            map.last_line_id = canvas.create_line(x, y, x, event.y, width=1, fill="red", arrow="last", arrowshape=(8, 10, 7))

    @staticmethod
    def get_courant(event, map: Map, canvas: Canvas, window):
        """
        Cette fonction permet de tracer un courant et fait les calculs nécessaires tout en changeant d'heure de navigation si besoin
        """
        if map.segments_done < len(map.path_delimitation):
            courant = {"line_base": None, "line_end": None, "vives_eaux": None, "mortes_eaux": None, "line_id": None, "vitesse_reelle": None}
            try:
                if map.courants[-1]["line_end"]:  # si le dernier courant ajouté a été entièrement tracé
                    map.courants.append(courant)  # on ajoute le courant suivant
            except Exception:  # ça rentre dans l'exception si il n'y a pas encore de courant
                map.courants.append(courant)  # dans ce cas on ajoute simplement le courant actuel
            if map.is_within_bounds(event.x, event.y):
                if not map.courants[-1]["line_base"] or map.courants[-1]["line_end"]:  # if it's our first click or a line has already been drawn
                    map.courants[-1]["line_base"] = (event.x, event.y)  # Set the line base to the clicked coordinates
                    map.courants[-1]["line_end"] = None  # set the line end to None because there could already be a drawn line
                elif map.courants[-1]["line_base"] and not map.courants[-1]["line_end"]:  # else if the line base is already selected
                    map.courants[-1]["line_end"] = (event.x, event.y)  # set the line end to the clicked cooordinates
                    canvas.itemconfig(map.path_delimitation[map.segments_done], fill="green")
                    map.segments_done += 1  # On incrémente le nombre de segments dont on a donné le courant de 1
                    Popup.get_vitesse_courant(map)  # On récupère la vitesse du couarnt
                    if map.segments_done == len(map.path_delimitation):  # Si le nombre de segments du chemin == nombre de segments dont on a donné le courant
                        canvas.delete(map.courants[-1]["line_id"])
                        map.calculer_courant_final(canvas)  # on calcule le courant final
                    else:
                        ################# Changer d'heure de navigation automatiquement si il reste des courants a tracer
                        map.boutons_heures[map.current_button_index].configure(bg="green")  # Changer la couleur du bouton corespondant a l'heure en vert
                        # Changer le bouton actuel de la carte a l'heure suivante pour éviter que la background ne se rechange en blanc par la fonction change_map
                        map.current_button = map.boutons_heures[map.current_button_index + 1]
                        map.current_button_index += 1  # On incrémente l'index du bouton actuel de 1
                        DirectoryManager.change_map(map, canvas, map.maps_paths[map.current_button_index],
                                                    map.current_button_index, window)  # On met la carte correspondant à l'heure suivante
                        ###############################################################


