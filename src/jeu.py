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
        # (tour, (pion_selectioné_x, pion_selectioné_y))
        self.tour_joueur = [0, (None, None)]
        self.root = tk.Tk()
        self.root.title("Mini Echecs: Jeu")
        self.root.geometry("800x800")
        self.canvas_width = 600
        self.canvas_height = 600
        self.label = tk.Label(self.root, text="Mini Echecs")
        self.label.pack(pady=(10, 0))  # Ajouter une marge en haut
        self.label_joueur = tk.Label(
            self.root, text="Joueur 1", font=("Helvetica, 20"))
        self.label_joueur.pack(pady=(0, 10))  # Ajouter une marge en bas
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=(10, 0))  # Ajouter une marge en haut du canvas
        self.draw_jeu()

    def draw_jeu(self):
        self.label.config(text="À vous de jouer !", font=("Helvetica, 15"))
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

    def afficher_mouvements_possibles(self, i, j):
        self.effacer_previsualisation()
        piece, joueur = self.plateau.get_plateau()[i][j]
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10

<<<<<<< Updated upstream
    def click_pion(self, i, j):
        case = self.plateau.get_plateau()[i][j]
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.label.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # bouger le pion du joueur vers cette case vide
                self.move_pion(i, j)
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
                self.label.config(
                    text=f"Vous avez sélectionné le pion {i}, {j}")
                self.tour_joueur[1] = (i, j)
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.update_game()  # mettre à jour le jeu tkinter

=======
        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)):
                    self.canvas.create_rectangle(
                        y * largeur_cellule + margin,
                        x * hauteur_cellule + margin,
                        (y + 1) * largeur_cellule - margin,
                        (x + 1) * hauteur_cellule - margin,
                        outline="green", width=2, tags="previsualisation"
                    )

    def effacer_previsualisation(self):
        self.canvas.delete("previsualisation")

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

    def mouvement_valide(self, start, end):
        start_x, start_y = start
        end_x, end_y = end
        piece, _ = self.plateau.get_plateau()[start_x][start_y]
        destination_piece, _ = self.plateau.get_plateau()[end_x][end_y]

        if destination_piece is not None:
            return False

        if piece == 1:  # reine
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        elif piece == 2:  # tour
            if start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        return False

    def move_pion(self, i, j):
        if self.mouvement_valide(self.tour_joueur[1], (i, j)):
            plateau = self.plateau.get_plateau()
            plateau[i][j] = plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]]
            plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (None, None)
            self.effacer_previsualisation()
            return True
        else:
            self.label.config(text="Mouvement invalide")
            return False

    def click_pion(self, i, j):
        case = self.plateau.get_plateau()[i][j]
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.label.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # bouger le pion du joueur vers cette case vide
                if not self.move_pion(i, j):
                    return
                if self.check_victoire():
                    self.label_joueur.config(text="Victoire pour le joueur " + str(self.joueur_actuel + 1))
                self.effacer_previsualisation()
        else:
            # la case a un pion qui n'appartient pas au joueur
            if self.tour_joueur[0] != case[1]:
                # on ne peut pas sélectionner un pion qui n'est pas le notre
                self.label.config(text="Ce n'est pas votre pion.")
                return
            else:  # la case a un pion qui appartient au joueur
                # on remplace l'ancienne selection par la nouvelle
                self.label.config(
                    text=f"Vous avez sélectionné le pion {i}, {j}")
                self.tour_joueur[1] = (i, j)
                self.afficher_mouvements_possibles(i, j)
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.update_game()  # mettre à jour le jeu tkinter
        

>>>>>>> Stashed changes
    def update_game(self):
        self.canvas.delete("all")
        self.effacer_previsualisation()
        self.draw_jeu()
<<<<<<< Updated upstream
=======
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    def on_canvas_click(self, event):
        x = event.x
        y = event.y
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        i = int(y // hauteur_cellule)
        j = int(x // largeur_cellule)
        self.show_possible_moves(i, j)

    def show_possible_moves(self, i, j):
        """Affiche les mouvements possibles pour une pièce."""
        piece = self.plateau.get_plateau()[i][j][0]
        if piece is not None:
            moves = self.get_possible_moves(i, j)
            self.highlight_moves(moves)
             

    def get_possible_moves(self, i, j):
        """Retourne les mouvements possibles pour une pièce."""
        taille = self.plateau.get_taille()
        possible_moves = []
        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)):
                    possible_moves.append((x, y))
        return possible_moves

    def highlight_moves(self, moves):
        """Met en évidence les mouvements possibles."""
        print(moves)
        for move in moves:
            x, y = move
            x0 = y * (self.canvas_width / self.plateau.get_taille())
            y0 = x * (self.canvas_height / self.plateau.get_taille())
            x1 = (y + 1) * (self.canvas_width / self.plateau.get_taille())
            y1 = (x + 1) * (self.canvas_height / self.plateau.get_taille())
            self.canvas.create_rectangle(x0, y0, x1, y1, tags="previsualisation")

    def effacer_previsualisation(self):
        """Efface les mouvements prévisualisés."""
        self.canvas.delete("previsualisation")
>>>>>>> Stashed changes

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
