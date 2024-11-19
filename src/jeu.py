from loguru import logger
import tkinter as tk
from src.joueur import Joueur
from src.plateau import Plateau
from src.render import Render
from tkinter import messagebox

class Jeu:
    def __init__(self):
        self.root_config = None
        self.label_taille = None
        self.entry_taille = None
        self.bouton_charger = None
        
        self.plateau = None
        self.joueurs = None
        self.render = None 
        
        self.charger_menu_configuration()
        
    def charger_menu_configuration(self):
        self.root_config = tk.Tk()
        self.root_config.title("Mini Echecs: Chargement")

        self.label_taille = tk.Label(self.root_config, text="Taille du plateau (6-12):")
        self.label_taille.pack(pady=10)

        self.entry_taille = tk.Entry(self.root_config)
        self.entry_taille.insert(0, "8")
        self.entry_taille.pack(pady=10)

        self.bouton_charger = tk.Button(self.root_config, text="Charger", command=self.charger_partie)
        self.bouton_charger.pack(pady=10)

        self.root_config.mainloop()

    def charger_partie(self):
        try:
            taille_plateau = int(self.entry_taille.get())
            if 6 <= taille_plateau <= 12:
                self.root_config.destroy()
                self.plateau = Plateau(taille_plateau)
                self.joueurs = [Joueur(), Joueur()]  # joueur 1 et joueur 2
                self.render = Render(self.plateau)
                self.run()
            else:
                messagebox.showerror(
                    "Erreur", "La taille du plateau doit être entre 6 et 12.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")

    def run(self):
        self.render.run()
        print('run')