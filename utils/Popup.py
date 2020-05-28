from tkinter import Tk, Button, Entry, Label, Canvas
from utils.Map import Map
import json

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
        text = canvas.create_text(map.settings["bottom_right_corner"][0] + 110, map.settings["upper_left_corner"][1],
                                  text="speed = {} knots".format(map.vitesse),
                                  fill="red",
                                  font=("Helvetica", "15")
                                  )  # on l'écrit à l'écran
        map.foreground_items.append(text)
        popup.quit()
        popup.destroy()

    @staticmethod
    def get_coeff_maree_value(input: Entry, popup: Tk, map: Map, canvas: Canvas):
        value = input.get()  # on récupère la valeur de l'input
        map.coefficient_maree = int(value)  # On en tire la coefficient de marée en tant qu'entier
        text = canvas.create_text(map.settings["bottom_right_corner"][0] + 120,
                                  map.settings["upper_left_corner"][1] + 90,
                                  text="coefficient de marée = {}".format(map.coefficient_maree),
                                  fill="red",
                                  font=("Helvetica", "15")
                                  )  # on écrit le coefficient de marée à l'écran
        map.foreground_items.append(text)
        map.etape = "courant"  # On change l'étape au tracé des courants
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
        print(map)
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