from src.jeu import Jeu
import tkinter as tk
from tkinter import messagebox


class PreConfig:
    """
    class PreConfig représente le menu de configuration du jeu avant de lancer une partie
    """

    def __init__(self):
        self.root = None

        # taille du plateau
        self.label_taille = None
        self.entry_taille = None
        # bouton charger partie
        self.bouton_charger = None

    def charger_menu_configuration(self):
        """
        procédure qui charge le menu de configuration du jeu avant de lancer une partie
        """
        self.root = tk.Tk()
        self.root.title("Mini Echecs: PreConfig")

        self.label_taille = tk.Label(
            self.root, text="Taille du plateau (6-12):")
        self.label_taille.pack(pady=10)

        self.entry_taille = tk.Entry(self.root)
        self.entry_taille.insert(0, "8")
        self.entry_taille.pack(pady=10)

        self.bouton_charger = tk.Button(
            self.root, text="Charger", command=self.charger_partie) # event quand on clique sur le bouton
        self.bouton_charger.pack(pady=10)

        self.root.mainloop()

    def charger_partie(self):
        try:
            taille_plateau = int(self.entry_taille.get())
            if 6 <= taille_plateau <= 12: # taille comprise entre 6 et 12 (énnoncé)
                self.root.destroy() # ferme la fenêtre tkinter de configuration car plus nécessaire
                jeu = Jeu(taille_plateau) # on crée une instance de la classe Jeu
                jeu.run() # on lance la partie
            else:
                messagebox.showerror(
                    "Erreur", "La taille du plateau doit être entre 6 et 12.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
