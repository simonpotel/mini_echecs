from loguru import logger 
import tkinter as tk
from src.joueur import Joueur

class Plateau:
    def __init__(self, taille):
        self.taille = taille
        self.plateau = [[(None, None) for _ in range(taille)] for _ in range(taille)] # i = ligne, j = colonne
        nombre_pions = taille**2//4-1
        self.plateau[taille-1][0] = (1, 0) # 1 = reine / 2 = tour // 0 = joueur 1 / 1 = joueur 2
        self.plateau[0][taille-1] = (1, 1)

    def get_plateau(self):
        return self.plateau
    
    def get_taille(self):
        return self.taille
    

class Jeu:
    def __init__(self, taille_plateau):
        self.plateau = Plateau(taille_plateau)
        self.joueurs = [Joueur(), Joueur()] # joueur 1 et joueur 2
        self.root = tk.Tk()
        self.root.title = ("mini_echecs")
        self.canvas_width = 800
        self.canvas_height = 800
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

    def run(self):
        self.root.mainloop()