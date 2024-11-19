from loguru import logger
import tkinter as tk
from src.joueur import Joueur
from src.plateau import Plateau

ref_couleurs = {
    "reine_joueur_1": "purple",
    "tours_joueur_1": "blue",
    "reine_joueur_2": "orange",
    "tours_joueur_2": "red"
}


class Jeu:
    def __init__(self, taille_plateau):
        self.plateau = Plateau(taille_plateau)
        self.joueurs = [Joueur(), Joueur()]  # joueur 1 et joueur 2
        self.root = tk.Tk()
        self.root.title = ("mini_echecs")
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.canvas.grid(row=0, column=0, columnspan=2, rowspan=2)
        self.canvas.grid(row=1, column=0)
        self.label = tk.Label(self.root, text="Joueur 1")  # Define self.label
        self.label.pack()
        self.draw_plateau()

    def draw_plateau(self):
        taille = self.plateau.get_taille()
        cell_width = self.canvas_width / taille
        cell_height = self.canvas_height / taille

        for i in range(taille):
            for j in range(taille):
                piece, joueur = self.plateau.get_plateau()[i][j]
                if piece is not None:
                    if piece == 1:  # reine
                        color = ref_couleurs[f"reine_joueur_{joueur + 1}"]
                    elif piece == 2:  # tour
                        color = ref_couleurs[f"tours_joueur_{joueur + 1}"]
                    x0 = j * cell_width
                    y0 = i * cell_height
                    x1 = x0 + cell_width
                    y1 = y0 + cell_height
                    self.canvas.create_oval(x0, y0, x1, y1, fill=color)

    def run(self):
        self.root.mainloop()
