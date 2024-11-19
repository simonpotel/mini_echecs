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
        self.joueurs = [Joueur(), Joueur()]
        self.joueur_actuel = 0
        self.root = tk.Tk()
        self.root.title("Mini Echecs: Jeu")
        self.root.geometry("800x800")
        self.canvas_width = 600
        self.canvas_height = 600
        self.label = tk.Label(self.root, text="Mini Echecs")
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.label.pack()
        self.canvas.pack()
        self.label_joueur = tk.Label(self.root, text="Joueur 1", font=("Helvetica, 20"))
        self.label_joueur.pack()
        self.draw_jeu()

    def draw_jeu(self):
        self.label.config(text="À vous de jouer !")
        self.label_joueur.config(text=f"Joueur {self.joueur_actuel + 1}")

        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10

        largeur_bordure = 2.5

        for i in range(taille + 1):
            self.canvas.create_line(largeur_bordure, i * hauteur_cellule, self.canvas_width,
                                    i * hauteur_cellule)  # lignes horizontales
            self.canvas.create_line(
                i * largeur_cellule, largeur_bordure, i * largeur_cellule, self.canvas_height + 0.25)  # lignes verticales

        # ligne gauche verticale
        self.canvas.create_line(
            largeur_bordure, largeur_bordure, largeur_bordure, self.canvas_height)
        # ligne haute horizontale
        self.canvas.create_line(
            largeur_bordure, largeur_bordure, self.canvas_width, largeur_bordure)

        for i in range(taille):
            for j in range(taille):
                piece, joueur = self.plateau.get_plateau()[i][j]
                if piece is not None:
                    if piece == 1:  # reine
                        color = ref_couleurs[f"reine_joueur_{joueur + 1}"]
                    elif piece == 2:  # tour
                        color = ref_couleurs[f"tours_joueur_{joueur + 1}"]
                    x = j * largeur_cellule + margin
                    y = i * hauteur_cellule + margin
                    w = (j + 1) * largeur_cellule - margin
                    h = (i + 1) * hauteur_cellule - margin
                    # dessiner le pion sur le canvas
                    oval = self.canvas.create_oval(x, y, w, h, fill=color)
                    # event click sur un pion
                    self.canvas.tag_bind(
                        oval, '<Button-1>', lambda event, i=i, j=j: self.click_pion(i, j))

    def click_pion(self, i, j):
        if self.joueur_actuel != self.plateau.get_plateau()[i][j][1]:
            self.label.config(text="Ce n'est pas votre pion.")
            return
        else:
            self.label.config(text="Votre pion a disparu !.!")
        self.plateau.get_plateau()[i][j] = (None, None)
        self.joueur_actuel = 0 if self.joueur_actuel == 1 else 1
        self.update_game()
        if self.check_victoire():
            self.update_game()
            self.label.config(text="Partie terminée")
            self.label_joueur.config(text="Victoire pour le joueur " + str(self.joueur_actuel + 1))
        else:
            self.joueur_actuel = 0 if self.joueur_actuel == 1 else 1
            self.update_game()

    def update_game(self):
        self.canvas.delete("all")
        self.draw_jeu()

    
    
    def check_victoire(self):
        plateau = self.plateau.get_plateau()
        taille = self.plateau.get_taille()
        pions_joueur_1 = 0
        pions_joueur_2 = 0

        for i in range(taille):
            for j in range(taille):
                piece, joueur = plateau[i][j]
                if piece is not None:
                    if joueur == 0:
                        pions_joueur_1 += 1
                    else:
                        pions_joueur_2 += 1

        if pions_joueur_1 < 3:
            print("Joueur 2 a gagné")
            return True
        elif pions_joueur_2 < 3:
            print("Joueur 1 a gagné")
            return True
        return False
            

    def run(self):
        self.update_game()
        self.root.mainloop()