from tkinter import Tk, Button, Entry, Label, Canvas
from utils.Map import Map
from utils.Popup import Popup
from utils.DirectoryManager import DirectoryManager

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
                    Popup.get_boat_speed(map, canvas)
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
                    map.last_line_id = canvas.create_line(x1, y1, event.x, event.y, width=2, fill="red", arrow="last", arrowshape=(8, 10, 7))  # draw the line

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
    def get_courant(event, map: Map, canvas: Canvas):
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
                                                    map.current_button_index)  # On met la carte correspondant à l'heure suivante
                        ###############################################################


