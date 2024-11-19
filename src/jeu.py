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
        self.joueurs = [Joueur(), Joueur()]
        self.plateau = Plateau(taille_plateau, self.joueurs)
        # (tour, (pion_selectioné_x, pion_selectioné_y))
        self.tour_joueur = [0, (None, None)]
        self.root = tk.Tk()
        self.root.title("Mini Echecs: Jeu")
        self.root.geometry("800x800")
        self.canvas_width = 600
        self.canvas_height = 600
        self.label = tk.Label(self.root, text="À vous de jouer :", font=("Roboto, 15"))
        self.label.pack(pady=(10, 0))  # Ajouter une marge en haut
        self.label_joueur = tk.Label(self.root, text="Joueur 1", font=("Roboto, 20"))
        self.label_joueur.pack(pady=(0, 10))  # Ajouter une marge en bas
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=(10, 0))  # Ajouter une marge en haut du canvas
        self.draw_jeu()

    def draw_jeu(self):
        self.label_joueur.config(text=f"Joueur {self.tour_joueur[0] + 1}")

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
                x = j * largeur_cellule + margin
                y = i * hauteur_cellule + margin
                w = (j + 1) * largeur_cellule - margin
                h = (i + 1) * hauteur_cellule - margin
                rect = self.canvas.create_rectangle(x, y, w, h, outline="")
                self.canvas.tag_bind(
                    rect, '<Button-1>', lambda event, i=i, j=j: self.click_pion(i, j))
                if piece is not None:
                    if piece == 1:  # reine
                        color = ref_couleurs[f"reine_joueur_{joueur + 1}"]
                    elif piece == 2:  # tour
                        color = ref_couleurs[f"tours_joueur_{joueur + 1}"]
                    # dessiner le pion sur le canvas
                    oval = self.canvas.create_oval(x, y, w, h, fill=color)
                    # event click sur un pion
                    self.canvas.tag_bind(
                        oval, '<Button-1>', lambda event, i=i, j=j: self.click_pion(i, j))
                    # dessiner un cercle vert autour du pion sélectionné
                    if (i, j) == self.tour_joueur[1]:
                        self.canvas.create_oval(x - 5, y - 5, w + 5, h + 5, outline="green", width=2)
                    
    
    def move_pion(self, i, j):
        plateau = self.plateau.get_plateau()
        plateau[i][j] = plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]]
        plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (None, None)

    def click_pion(self, i, j):
        plateau = self.plateau.get_plateau()
        case = plateau[i][j]
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.label.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # check ici si c'est possible de le bouger
                
                # bouger le pion du joueur vers cette case vide
                if not self.move_pion(i, j):
                    return
                reine_coords = self.joueurs[self.tour_joueur[0]].get_coordonnees_reine()
                if i != reine_coords[0] and j != reine_coords[1]:
                    rectangle_sommets = [
                        (i, j),
                        (i, reine_coords[1]),
                        reine_coords,
                        (reine_coords[0], j)
                    ]
                    for x, y in [rectangle_sommets[1], rectangle_sommets[3]]:
                        if plateau[x][y][1] != self.tour_joueur[0] and plateau[x][y][1] is not None:
                            plateau[x][y] = (None, None)
                 
                if self.check_victoire():
                    self.update_game()
                    self.label.config(text="Partie terminée")
                    self.label_joueur.config(text="Victoire pour le joueur " + str(self.joueur_actuel + 1))
        else:
            # la case a un pion qui n'appartient pas au joueur
            if self.tour_joueur[0] != case[1]:
                # on ne peut pas sélectionner un pion qui n'est pas le notre
                self.label.config(text="Ce n'est pas votre pion.")
                return
            else:  # la case a un pion qui appartient au joueur
                # on remplace l'ancienne selection par la nouvelle
                match case[0]:
                    case 1: # reine 
                        pion_type_msg = "votre reine"
                        self.joueurs[self.tour_joueur[0]].set_coordonnees_reine((i, j))
                    case 2: # tour
                        pion_type_msg = "une tour"
                
                self.label.config(text=f"Vous avez sélectionné {pion_type_msg} ({i}, {j})")
                self.tour_joueur[1] = (i, j)
                self.update_game()
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.label.config(text="À vous de jouer :")
        self.update_game()  # mettre à jour le jeu tkinter
        
    def mouvement_valide(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        piece, _ = self.plateau.get_plateau()[start_x][start_y]

        if piece == 1:  # reine
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        elif piece == 2:  # tour
            if start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        return False

    def chemin_libre(self, start, end):
        start_x, start_y = start
        end_x, end_y = end

        step_x = (end_x - start_x) // max(1, abs(end_x - start_x))
        step_y = (end_y - start_y) // max(1, abs(end_y - start_y))

        current_x, current_y = start_x + step_x, start_y + step_y
        while (current_x, current_y) != (end_x, end_y):
            if self.plateau.get_plateau()[current_x][current_y][0] is not None:
                return False
            current_x += step_x
            current_y += step_y
        return True

    def move_pion(self, i, j):
        if self.mouvement_valide(self.tour_joueur[1], (i, j)):
            plateau = self.plateau.get_plateau()
            plateau[i][j] = plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]]
            plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (None, None)
            return True
        else:
            self.label.config(text="Mouvement invalide")
            return False
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
