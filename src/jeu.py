import tkinter as tk
from src.joueur import Joueur
from src.plateau import Plateau


class Jeu:
    ref_couleurs = {
        "reine_joueur_1": "purple",
        "tours_joueur_1": "blue",
        "reine_joueur_2": "orange",
        "tours_joueur_2": "red"
    }

    def __init__(self, taille_plateau):
        """
        procédure: initialise les composants du jeu et l'interface graphique.
        """
        self.joueurs = [Joueur(), Joueur()]  # 0 = joueur 1 / 1 = joueur 2
        # plateau de jeu (board) avec tableau de tuples (piece, joueur)
        self.plateau = Plateau(taille_plateau, self.joueurs)
        # [joueur_actuel, pion_selectionne(x, y)]
        self.tour_joueur = [0, (None, None)]
        self.root = tk.Tk()  # fenêtre principale tkinter
        self.root.title("Mini Echecs: Jeu")  # titre de la fenêtre
        self.root.geometry("800x800")  # taille de la fenêtre
        self.canvas_width = 600  # hauteur du board
        self.canvas_height = 600  # largeur du board
        self.label_instruction = tk.Label(self.root, text="À vous de jouer :", font=(
            "Roboto, 15"))  # label tkinter instruction de jeu
        self.label_instruction.pack(pady=(10, 0))  # margin top 10
        self.label_tour_joueur = tk.Label(self.root, text="Joueur 1", font=(
            "Roboto, 20"))  # label tkinter tour du joueur
        self.label_tour_joueur.pack(pady=(0, 10))  # margin bottom 10
        self.canvas = tk.Canvas(
            # canvas tkinter pour dessiner le board
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=(10, 0))  # margin top 10
        self.dessiner_jeu()  # dessine le board

    def dessiner_jeu(self):
        """
        procédure: dessine le plateau de jeu et les pièces sur le canvas.
        """

        self.label_instruction.config(
            text="À vous de jouer !", font=("Helvetica, 15"))
        self.label_tour_joueur.config(text=f"Joueur {self.tour_joueur[0] + 1}")

        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10
        largeur_bordure = 2.5

        for i in range(taille + 1):
            # lignes horizontales
            self.canvas.create_line(largeur_bordure, i * hauteur_cellule, self.canvas_width,
                                    i * hauteur_cellule)
            # lignes verticales
            self.canvas.create_line(
                i * largeur_cellule, largeur_bordure, i * largeur_cellule, self.canvas_height + 0.25)

        # ligne gauche verticale
        self.canvas.create_line(
            largeur_bordure, largeur_bordure, largeur_bordure, self.canvas_height)
        # ligne haute horizontale
        self.canvas.create_line(
            largeur_bordure, largeur_bordure, self.canvas_width, largeur_bordure)

        # boucles qui dessinent les cellules du board
        for i in range(taille):
            for j in range(taille):
                piece, joueur = self.plateau.get_plateau()[i][j]
                x = j * largeur_cellule + margin  # position x sur le plateau
                y = i * hauteur_cellule + margin  # position y sur le plateau
                # largeur de la cellule (width)
                w = (j + 1) * largeur_cellule - margin
                # hauteur de la cellule (height)
                h = (i + 1) * hauteur_cellule - margin
                # dessiner la cellule dans le rectangle x, y, w, h
                rect = self.canvas.create_rectangle(x, y, w, h, outline="")
                self.canvas.tag_bind(
                    # event click sur la cellule
                    rect, '<Button-1>', lambda event, i=i, j=j: self.event_click_pion(i, j))
                if piece is not None:  # si la case contient un pion
                    if piece == 1:  # reine
                        # couleur de la reine en fonction du joueur
                        color = self.ref_couleurs[f"reine_joueur_{joueur + 1}"]
                    elif piece == 2:  # tour
                        # couleur de la tour en fonction du joueur
                        color = self.ref_couleurs[f"tours_joueur_{joueur + 1}"]
                    # dessiner le pion sur le canvas
                    pion = self.canvas.create_oval(x, y, w, h, fill=color)
                    # event click sur un pion
                    self.canvas.tag_bind(
                        pion, '<Button-1>', lambda event, i=i, j=j: self.event_click_pion(i, j))
                    # dessiner un cercle vert autour du pion sélectionné

    def afficher_selection_joueur(self, i, j):
        """
        procédure: Affiche la sélection du joueur et les mouvements possibles sur le plateau.
        """

        # effacer les mouvements prévisualisés auparavant
        self.canvas.delete("previsualisation")
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10

        self.canvas.create_oval(j * largeur_cellule + margin - 5,
                                i * hauteur_cellule + margin - 5,
                                (j + 1) * largeur_cellule - margin + 5,
                                (i + 1) * hauteur_cellule - margin + 5, outline="green", width=2)

        for x in range(taille):
            for y in range(taille):

                # si le mouvement est valide
                if self.mouvement_valide((i, j), (x, y)):
                    self.canvas.create_rectangle(  # dessiner le mouvement possible
                        y * largeur_cellule + margin,
                        x * hauteur_cellule + margin,
                        (y + 1) * largeur_cellule - margin,
                        (x + 1) * hauteur_cellule - margin,
                        outline="green", width=2, tags="previsualisation"
                    )

    def effacer_previsualisation(self):
        """
        procédure: efface les mouvements prévisualisés sur le canvas.
        """

        # effacer les mouvements prévisualisés
        self.canvas.delete("previsualisation")

    def chemin_libre(self, start, end):
        """
        fonction: vérifie si le chemin entre deux cases est libre pour un mouvement. (start(x,y) -> end(x,y))
        return True ou False si le chemin est libre ou non
        """

        # vérifie si le chemin entre deux cases est libre pour un mouvement
        start_x, start_y = start
        end_x, end_y = end

        step_x = (end_x - start_x) // max(1, abs(end_x - start_x))  # pas x
        step_y = (end_y - start_y) // max(1, abs(end_y - start_y))  # pas y

        actuel_x, actuel_y = start_x + step_x, start_y + step_y  # position actuelle
        # tant que la position actuelle n'est pas la destination
        while (actuel_x, actuel_y) != (end_x, end_y):
            # si la case n'est pas vide
            if self.plateau.get_plateau()[actuel_x][actuel_y][0] is not None:
                return False  # le chemin n'est pas libre
            # avancer d'un pas
            actuel_x += step_x
            actuel_y += step_y
        return True  # le chemin est libre

    def mouvement_valide(self, start, end):
        """
        fonction: vérifie si un mouvement est valide pour une pièce donnée sur un plateau d'échecs
        return True ou False si le mouvement est valide ou non
        """

        start_x, start_y = start  # position de départ
        end_x, end_y = end  # position d'arrivée
        piece, _ = self.plateau.get_plateau(
        )[start_x][start_y]  # pièce à déplacer
        destination_piece, _ = self.plateau.get_plateau(
        )[end_x][end_y]  # pièce à la destination

        if destination_piece is not None:
            return False  # la case d'arrivée n'est pas vide

        if piece == 1:  # reine
            # déplacement diagonale ou orthogonal
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        elif piece == 2:  # tour
            if start_x == end_x or start_y == end_y:  # déplacement orthogonal
                return self.chemin_libre(start, end)
        return False

    def deplacer_pion(self, i, j):
        """
        procédure: déplace un pion sur le plateau de jeu si le mouvement est valide
        return True ou False si le mouvement est valide ou non
        """

        # si le mouvement est valide
        if self.mouvement_valide(self.tour_joueur[1], (i, j)):
            plateau = self.plateau.get_plateau()
            plateau[i][j] = plateau[self.tour_joueur[1][0]
                                    # déplacer le pion
                                    ][self.tour_joueur[1][1]]
            plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (
                None, None)  # vider la case de départ
            # effacer les mouvements prévisualisés
            self.canvas.delete("previsualisation")
            return True
        else:
            # le mouvement n'est pas valide
            self.label_instruction.config(text="Mouvement invalide")
            return False

    def event_click_pion(self, i, j):
        """
        procédure: gère les événements de clic sur un pion dans le jeu d'échecs
        permet la selection du pion et le déplacement des pions
        """

        plateau = self.plateau.get_plateau()
        case = plateau[i][j]
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.label_instruction.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # bouger le pion du joueur vers cette case vide
                if not self.deplacer_pion(i, j):
                    return

                reine_coords = self.joueurs[self.tour_joueur[0]
                                            ].get_coordonnees_reine()
                if i != reine_coords[0] and j != reine_coords[1]:
                    rectangle_sommets = [
                        (i, j),
                        (i, reine_coords[1]),
                        reine_coords,
                        (reine_coords[0], j)
                    ]  # rectangle formé par les 4 sommets
                    # condition de sortie
                    for x, y in [rectangle_sommets[1], rectangle_sommets[3]]:
                        if plateau[x][y][1] != self.tour_joueur[0] and plateau[x][y][1] is not None:
                            self.joueurs[plateau[x][y][1]].perdre_tour()
                            plateau[x][y] = (None, None)

                if self.check_victoire():  # vérifier si un joueur a gagné
                    # afficher le joueur gagnant
                    self.label_tour_joueur.config(
                        text="Victoire pour le joueur " + str(self.joueur_actuel + 1))
                # effacer les mouvements prévisualisés
                self.canvas.delete("previsualisation")
        else:
            # la case a un pion qui n'appartient pas au joueur
            if self.tour_joueur[0] != case[1]:
                # on ne peut pas sélectionner un pion qui n'est pas le notre
                self.label_instruction.config(text="Ce n'est pas votre pion.")
                return
            else:  # la case a un pion qui appartient au joueur
                # on remplace l'ancienne selection par la nouvelle
                match case[0]:
                    case 1:  # reine
                        pion_type_msg = "votre reine"
                        self.joueurs[self.tour_joueur[0]
                                     ].set_coordonnees_reine((i, j))
                    case 2:  # tour
                        pion_type_msg = "une tour"

                self.label_instruction.config(text=f"Vous avez sélectionné {
                                              pion_type_msg} ({i}, {j})")
                self.tour_joueur[1] = (i, j)
                largeur_cellule = self.canvas_width / self.plateau.get_taille()
                hauteur_cellule = self.canvas_height / self.plateau.get_taille()
                margin = 10

                self.afficher_selection_joueur(i, j)
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.update_tkinter()  # mettre à jour le jeu tkinter

    def update_tkinter(self):
        """
        procédure: met à jour l'interface Tkinter en effaçant et redessinant le canvas, 
        et en liant l'événement de clic sur le canvas à une fonction de gestion des événements
        """

        self.canvas.delete("all")  # effacer le canvas
        # effacer les mouvements prévisualisés
        self.canvas.delete("previsualisation")
        self.dessiner_jeu()  # redessiner le jeu
        # event click sur le canvas
        self.canvas.bind("<Button-1>", self.event_click_canvas)

    def event_click_canvas(self, event):
        """
        procédure: gère l'événement de clic sur le canvas et affiche les déplacements possibles pour la position cliquée
        """

        x = event.x  # position x du click relative au board (canvas tkinter)
        y = event.y  # position y du click relative au board (canvas tkinter)
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        i = int(y // hauteur_cellule)
        j = int(x // largeur_cellule)
        self.afficher_deplacements_possibles(i, j)

    def afficher_deplacements_possibles(self, i, j):
        """
        procédure: affiche les déplacements possibles pour la pièce située à la position (i, j) sur le plateau
        """
        # récupérer la pièce sur la case
        piece = self.plateau.get_plateau()[i][j][0]
        if piece is not None:
            moves = self.get_deplacements_possibles(
                i, j)  # récupérer les mouvements possibles
            # dessiner les mouvements possibles
            self.dessiner_deplacements_possibles(moves)

    def get_deplacements_possibles(self, i, j):
        """
        fonction: retourne une liste de tuples représentant les mouvements possibles pour une pièce donnée
        """
        taille = self.plateau.get_taille()
        possible_moves = []
        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)):
                    possible_moves.append((x, y))
        return possible_moves

    def dessiner_deplacements_possibles(self, moves):
        """
        procédure: dessine les déplacements possibles sur le plateau de jeu
        """
        for move in moves:  # pour chaque mouvement possible (x, y)
            x, y = move
            x0 = y * (self.canvas_width / self.plateau.get_taille())
            y0 = x * (self.canvas_height / self.plateau.get_taille())
            x1 = (y + 1) * (self.canvas_width / self.plateau.get_taille())
            y1 = (x + 1) * (self.canvas_height / self.plateau.get_taille())
            # dessiner le mouvement possible
            self.canvas.create_rectangle(
                x0, y0, x1, y1, tags="previsualisation")

    def check_victoire(self):
        """
        fonction : vérifie si un joueur a gagné la partie 
        return True/False si un joueur a gagné ou non
        """
        plateau = self.plateau.get_plateau()
        taille = self.plateau.get_taille()
        pions_joueur_1 = 0
        pions_joueur_2 = 0

        # permet de compter le nombre de pions restants pour chaque joueur
        for i in range(taille):
            for j in range(taille):
                piece, joueur = plateau[i][j]
                if piece is not None:
                    if joueur == 0:
                        pions_joueur_1 += 1
                    else:
                        pions_joueur_2 += 1

        # règles de victoire
        if pions_joueur_1 < 3:
            print("Joueur 2 a gagné")
            return True
        elif pions_joueur_2 < 3:
            print("Joueur 1 a gagné")
            return True
        return False

    def run(self):
        """
        procédure : lance le jeu et met à jour le jeu tkinter
        """
        self.update_tkinter()  # mettre à jour le jeu tkinter
        self.root.mainloop()  # lancer le jeu
