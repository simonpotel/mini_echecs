from loguru import logger
import tkinter as tk
from src.joueur import Joueur

ref_couleurs = {
    "reine_joueur_1": "purple",
    "tours_joueur_1": "blue",
    "reine_joueur_2": "orange",
    "tours_joueur_2": "red"
}


class Plateau:
    def __init__(self, taille):
        self.taille = taille
        self.plateau = [[(None, None) for _ in range(taille)]
                        for _ in range(taille)]  # i = ligne, j = colonne
        self.initialise_plateau()

    def get_plateau(self):
        return self.plateau

    def get_taille(self):
        return self.taille
    
    def initialise_plateau(self):
        """
        Procédure qui permet de placer les reines et les tours sur le plateau
        pour chaque joueur en début de partie.
        """
        nombre_pions = (self.taille**2)//4-1  # nombre forcément impair
        # placement initial des tours
        nombre_lignes_pions = self.taille//2 # nombre de pions par ligne et nombre de lignes
        for i in range(nombre_lignes_pions):
            for j in range(nombre_lignes_pions):
                self.plateau[self.taille-1-i][j] = (2, 0) # tour joueur 1
                self.plateau[i][self.taille-1-j] = (2, 1) # tour joueur 2

        # 1 = reine / 2 = tour // 0 = joueur 1 / 1 = joueur 2
        self.plateau[self.taille-1][0] = (1, 0) # reine joueur 1
        self.plateau[0][self.taille-1] = (1, 1) # reine joueur 2


class Jeu:
    def __init__(self, taille_plateau):
        self.plateau = Plateau(taille_plateau)
        self.joueurs = [Joueur(), Joueur()]  # joueur 1 et joueur 2
        self.root = tk.Tk()
        self.root.title = ("mini_echecs")
        self.canvas_width = 800
        self.canvas_height = 800
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def run(self):
        self.root.mainloop()
