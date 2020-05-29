from tkinter import Tk, Button, Entry, Label, Canvas
from utils.Map import Map
import json
import math


class Popup:
    @staticmethod
    def center(win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 3) - (height // 2)
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    @staticmethod
    def get_boat_speed(map: Map, canvas: Canvas):
        popup = Tk()
        Label(popup, text="Veuillez entrer la vitesse du bateau", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        popup.bind('<Return>', lambda event: Popup.get_speed_value(entry, popup, map,
                                                                   canvas))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        Button(popup, command=lambda: Popup.get_speed_value(entry, popup, map, canvas), text="Confirmer").pack(
            side="top")
        Popup.center(popup)
        popup.mainloop()
        Popup.get_coeff_maree(map, canvas)

    @staticmethod
    def get_coeff_maree(map: Map, canvas: Canvas):
        popup = Tk()
        Label(popup, text="Veuillez entrer le coefficient de marée", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        popup.bind('<Return>', lambda event: Popup.get_coeff_maree_value(entry, popup, map,
                                                                         canvas))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        Button(popup, command=lambda: Popup.get_coeff_maree_value(entry, popup, map, canvas), text="Confirmer").pack(
            side="top")
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def get_speed_value(input: Entry, popup: Tk, map: Map, canvas: Canvas):
        value = input.get()  # on récupère la valeur de l'input
        map.vitesse = int(value)  # on l'assigne a la vitesse du bateau
        text = canvas.create_text(map.settings["bottom_right_corner"][0] + 130, map.settings["upper_left_corner"][1],
                                  text="vitesse:\n{} noeuds".format(map.vitesse),
                                  fill="red",
                                  font=("Helvetica", "13"),
                                  anchor="n"
                                  )  # on l'écrit à l'écran
        r = canvas.create_rectangle(canvas.bbox(text), fill="white")
        canvas.tag_lower(r, text)
        map.foreground_items.append(text)
        popup.quit()
        popup.destroy()

    @staticmethod
    def get_coeff_maree_value(input: Entry, popup: Tk, map: Map, canvas: Canvas):
        value = input.get()  # on récupère la valeur de l'input
        map.coefficient_maree = int(value)  # On en tire la coefficient de marée en tant qu'entier
        text = canvas.create_text(map.settings["bottom_right_corner"][0] + 130,
                                  map.settings["upper_left_corner"][1] + 150,
                                  text="coefficient de marée:\n{}".format(map.coefficient_maree),
                                  fill="red",
                                  font=("Helvetica", "13"),
                                  anchor="n",
                                  )  # on écrit le coefficient de marée à l'écran
        r = canvas.create_rectangle(canvas.bbox(text), fill="white")
        canvas.tag_lower(r, text)
        map.foreground_items.append(text)
        map.etape = "courant"  # On change l'étape au tracé des courants
        map.show_instruction("Choisissez une heure de départ\nTracez les courants du trajet")
        canvas.delete(map.longitude_text)
        canvas.delete(map.latitude_text)
        popup.quit()
        popup.destroy()

    @staticmethod
    def get_vitesse_courant(map: Map):
        popup = Tk()
        entries = []
        Label(popup, text="Veuillez entrer les vitesses du courant", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        Label(popup, text="En vives eaux", font=("Helvetica", 10),
              foreground="black").pack(side="top")
        entries.append(Entry(popup, width=20))
        entries[0].pack(side="top")
        entries[0].focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        Label(popup, text="En mortes eaux", font=("Helvetica", 10), foreground="black").pack(side="top")
        entries.append(Entry(popup, width=20))
        entries[1].pack(side="top")
        Button(popup, command=lambda: Popup.set_vitesse_courant(entries, popup, map), text="Confirmer").pack(
            side="top")
        popup.bind('<Return>', lambda event: Popup.set_vitesse_courant(entries, popup, map))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def set_vitesse_courant(entries: list, popup: Tk, map: Map):
        vives_eaux = map.courants[-1]["vives_eaux"] = int(entries[0].get())
        vives_eaux /= 10
        mortes_eaux = map.courants[-1]["mortes_eaux"] = int(entries[1].get())
        mortes_eaux /= 10
        map.courants[-1]["vitesse_reelle"] = mortes_eaux + (
                    ((vives_eaux - mortes_eaux) * (map.coefficient_maree - 45)) / 50)
        popup.quit()
        popup.destroy()

    @staticmethod
    def change_name_popup(path, map: Map, canvas, window):
        popup = Tk()
        text = Label(popup, text="Entrez le nouveau nom", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        Button(popup, command=lambda: Popup.change_name(entry, popup, path, map, canvas, window), text="Confirmer").pack(side="top")
        popup.bind('<Return>', lambda event: Popup.change_name(entry, popup, path, map, canvas, window))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def change_name(input, popup, path, map: Map, canvas, window):
        value = input.get()
        found = False
        i = 0
        history = []
        with open("map_history.json", 'r+') as file:
            history = json.load(file)
            print(history)
            for entry in history:
                if entry["path"] == path:
                    found = True
                    break
                i += 1
        if found:
            history[i]["name"] = value
            with open("map_history.json", 'w+') as file:
                file.write(json.dumps(history))
            Map.show_history(map, canvas, window)
        popup.quit()
        popup.destroy()

    @staticmethod
    def ask_longitude_top_left_corner(map):
        popup = Tk()
        text = Label(popup, text="Entrez la longitude de référence en haut a gauche de la carte", font=("Helvetica", 20),
                     foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        Button(popup, command=lambda: Popup.set_longitude_top_left_corner(entry, popup, map),
               text="Confirmer").pack(side="top")
        popup.bind('<Return>', lambda event: Popup.set_longitude_top_left_corner(entry, popup, map))
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def set_longitude_top_left_corner(entry, popup, map):
        value = str(entry.get())
        try:
            degres = int(value.split(",")[0]) * 60
            minutes = int(value.split(",")[1])
        except:
            degres = int(value.split(".")[0]) * 60
            minutes = int(value.split(".")[1])
        map.settings["longitude_top_left_corner"] = degres + minutes
        map.sous_etape = "ratio_pixel_minutes"
        map.show_instruction("Veuillez tracer une ligne\n correspondant a \nun nombre entier de\n minutes de longitude")
        popup.quit()
        popup.destroy()

    @staticmethod
    def ask_number_of_minutes_popup(map):
        popup = Tk()
        text = Label(popup, text="Entrez le nombre de minutes correspondant a la ligne tracée", font=("Helvetica", 20), foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        if map.sous_etape == "ratio_pixel_minutes":
            print(map.sous_etape)

            Button(popup, command=lambda: Popup.calculate_pixel_minutes_ratio(entry, popup, map),
                   text="Confirmer").pack(side="top")
            popup.bind('<Return>', lambda event: Popup.calculate_pixel_minutes_ratio(entry, popup, map))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        elif map.sous_etape == "ratio_pixel_nautical_miles":
            print(map.sous_etape)
            Button(popup, command=lambda: Popup.calculate_ratio_pixel_nautical_miles(entry, popup, map),
                   text="Confirmer").pack(side="top")
            popup.bind('<Return>', lambda event: Popup.calculate_ratio_pixel_nautical_miles(entry, popup,
                                                                                     map))  # Assigner la touché Entrée a la meme fonction que le bouton confirmer
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def calculate_pixel_minutes_ratio(entry, popup, map: Map):
        # Nombre de pixels correspondant a une minute en longitude
        value = int(entry.get())
        longueur_ligne = map.line_end[0] - map.line_base[0]
        map.settings["ratio_pixel_minutes"] = [value, longueur_ligne]
        radian = math.radians(value / 60)  # On calcule ne nombre de degrés en radian
        map.settings["multiplier"] = longueur_ligne / radian  # = nombre de pixels par nombre de minutes de longitude
        map.show_instruction("Veuillez tracer une ligne\n correspondant a \nun nombre entier de\n minutes de latitude")
        map.sous_etape = "ratio_pixel_nautical_miles"
        popup.quit()
        popup.destroy()

    @staticmethod
    def calculate_ratio_pixel_nautical_miles(entry, popup, map):
        # nombre de pixels correspondant a 1 mile en latitude
        value = int(entry.get())
        longueur_ligne = map.line_end[1] - map.line_base[1]
        map.settings["ratio_pixel_nautical_miles"] = value / longueur_ligne
        popup.quit()
        popup.destroy()
        Popup.ask_latitude_de_reference(map)

    @staticmethod
    def ask_latitude_de_reference(map):
        popup = Tk()
        text = Label(popup, text="Entrez la latitude de référence", font=("Helvetica", 20),
                     foreground="red").pack(
            side="top")
        entry = Entry(popup, width=20)
        entry.pack(side="top")
        Button(popup, command=lambda: Popup.calculate_latitude_de_reference(entry, popup, map),
               text="Confirmer").pack(side="top")
        popup.bind('<Return>', lambda event: Popup.calculate_latitude_de_reference(entry, popup, map))
        entry.focus_force()  # Forcer le focus sur l'input pour ne pas avoir a cliquer dessus
        Popup.center(popup)  # Center the popup
        popup.mainloop()

    @staticmethod
    def calculate_latitude_de_reference(entry, popup, map: Map):
        value = str(entry.get())
        degres = int(value.split(",")[0])
        degres = math.radians(degres)
        minutes = int(value.split(",")[1])
        minutes = math.radians(minutes / 60)
        val_latitude_ref_radian = degres + minutes
        latitude_ref_pixels = math.log(math.tan((math.pi / 4) + val_latitude_ref_radian / 2) ) * map.settings["multiplier"]
        map.settings["nombre_pixels_equateur_latitude_de_reference"] = latitude_ref_pixels
        map.show_instruction("Veuillez tracer le décalage\n par rapport au \ncoin supérieur haut-gauche")
        map.sous_etape = "decalage_x_y"
        popup.quit()
        popup.destroy()


