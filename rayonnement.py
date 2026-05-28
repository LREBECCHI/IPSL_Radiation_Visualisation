import xarray as xy
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ds = xy.open_dataset("srb_climatology.nc", decode_times=False)

# Fenêtre
fenetre = ctk.CTk()
fenetre.title("IPSL Radiation Solaire")
fenetre.geometry("1080x800")
fenetre.minsize(800, 500)
fenetre.configure(fg_color="#6EBAF0")

# Barre de Menu
barreMenu = ctk.CTkFrame(fenetre, fg_color='#585E5E', corner_radius=0)
barreMenu.pack(fill="x", side="top")

ongletTemps = ctk.CTkOptionMenu(barreMenu, width=140, height=40, fg_color="#1E2121",
                                 values=["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                                         "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"])
ongletTemps.pack(side="left", padx=8, pady=8)

donnees = ctk.CTkSegmentedButton(barreMenu,
                                  values=["swdwn", "swcs", "swnet", "lwdwn", "lwcs",
                                          "Rayonnements Renvoyés", "Effets Nuages SW", "Effets Nuages LW"],
                                  height=40, corner_radius=8, fg_color="#585E5E",
                                  selected_color="#1E2121", selected_hover_color="#1E2121")
donnees.pack(side="right", padx=8, pady=8)
donnees.set("swdwn")

# Zone graphique
fig, ax = plt.subplots(figsize=(9, 5))
fig.patch.set_facecolor("#6EBAF0")
canvas = FigureCanvasTkAgg(fig, master=fenetre)
canvas.get_tk_widget().pack(fill="both", expand=True, padx=16, pady=16)

# Fonction affichage
def afficherCarte(*args):
    choixMois = ongletTemps.get()
    choixDonnees = donnees.get()

    moisListe = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                 "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
    moisAffichageCarte = moisListe.index(choixMois)

    match choixDonnees:
        case "swdwn":
            carte = ds["swdwn"].isel(time=moisAffichageCarte)
        case "swcs":
            carte = ds["swcs"].isel(time=moisAffichageCarte)
        case "swnet":
            carte = ds["swnet"].isel(time=moisAffichageCarte)
        case "lwdwn":
            carte = ds["lwdwn"].isel(time=moisAffichageCarte)
        case "lwcs":
            carte = ds["lwcs"].isel(time=moisAffichageCarte)
        case "Rayonnements Renvoyés":
            carte = ds["swdwn"].isel(time=moisAffichageCarte) - ds["swnet"].isel(time=moisAffichageCarte)
        case "Effets Nuages SW":
            carte = ds["swcs"].isel(time=moisAffichageCarte) - ds["swdwn"].isel(time=moisAffichageCarte)
        case "Effets Nuages LW":
            carte = ds["lwcs"].isel(time=moisAffichageCarte) - ds["lwdwn"].isel(time=moisAffichageCarte)

    # Rafraîchissement de la carte
    fig.clf()
    ax = fig.add_subplot(111)
    carte.plot(ax=ax)
    fig.tight_layout()
    canvas.draw()

# bind
ongletTemps.configure(command=afficherCarte)
donnees.configure(command=afficherCarte)

afficherCarte()  # affichage initial
fenetre.mainloop()