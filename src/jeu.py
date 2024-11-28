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
        self.joueurs = [Joueur(), Joueur()] # 0 = joueur 1 / 1 = joueur 2
        self.plateau = Plateau(taille_plateau) # plateau de jeu (board) avec tableau de tuples (piece, joueur)
        self.tour_joueur = [0, (None, None)] # [joueur_actuel, pion_selectionne(x, y)]
        self.root = tk.Tk() # fenêtre principale tkinter
        self.root.title("Mini Echecs: Jeu") # titre de la fenêtre
        self.root.geometry("800x800") # taille de la fenêtre
        self.canvas_width = 600 # hauteur du board
        self.canvas_height = 600 # largeur du board
        self.label_instruction = tk.Label(self.root, text="À vous de jouer :", font=("Roboto, 15")) # label tkinter instruction de jeu
        self.label_instruction.pack(pady=(10, 0))  # margin top 10
        self.label_tour_joueur = tk.Label(self.root, text="Joueur 1", font=("Roboto, 20")) # label tkinter tour du joueur
        self.label_tour_joueur.pack(pady=(0, 10))  # margin bottom 10
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height) # canvas tkinter pour dessiner le board
        self.canvas.pack(pady=(10, 0))  # margin top 10
        self.dessiner_jeu() # dessine le board 

    def dessiner_jeu(self):
        self.label_instruction.config(text="À vous de jouer !", font=("Helvetica, 15"))
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
                x = j * largeur_cellule + margin # position x sur le plateau
                y = i * hauteur_cellule + margin # position y sur le plateau
                w = (j + 1) * largeur_cellule - margin # largeur de la cellule (width)
                h = (i + 1) * hauteur_cellule - margin # hauteur de la cellule (height)
                rect = self.canvas.create_rectangle(x, y, w, h, outline="") # dessiner la cellule dans le rectangle x, y, w, h
                self.canvas.tag_bind(
                    rect, '<Button-1>', lambda event, i=i, j=j: self.event_click_pion(i, j)) # event click sur la cellule 
                if piece is not None: # si la case contient un pion
                    if piece == 1:  # reine
                        color = ref_couleurs[f"reine_joueur_{joueur + 1}"] # couleur de la reine en fonction du joueur
                    elif piece == 2:  # tour
                        color = ref_couleurs[f"tours_joueur_{joueur + 1}"] # couleur de la tour en fonction du joueur
                    # dessiner le pion sur le canvas
                    pion = self.canvas.create_oval(x, y, w, h, fill=color)
                    # event click sur un pion
                    self.canvas.tag_bind(
                        pion, '<Button-1>', lambda event, i=i, j=j: self.event_click_pion(i, j))

    def afficher_mouvements_possibles(self, i, j):
        self.effacer_previsualisation() # effacer les mouvements prévisualisés auparavant
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10

        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)): # si le mouvement est valide
                    self.canvas.create_rectangle( # dessiner le mouvement possible
                        y * largeur_cellule + margin,
                        x * hauteur_cellule + margin,
                        (y + 1) * largeur_cellule - margin,
                        (x + 1) * hauteur_cellule - margin,
                        outline="green", width=2, tags="previsualisation"
                    )

    def effacer_previsualisation(self):
        self.canvas.delete("previsualisation") # effacer les mouvements prévisualisés

    def chemin_libre(self, start, end):
        # vérifie si le chemin entre deux cases est libre pour un mouvement
        start_x, start_y = start
        end_x, end_y = end

        step_x = (end_x - start_x) // max(1, abs(end_x - start_x)) # pas x
        step_y = (end_y - start_y) // max(1, abs(end_y - start_y)) # pas y

        actuel_x, actuel_y = start_x + step_x, start_y + step_y # position actuelle
        while (actuel_x, actuel_y) != (end_x, end_y): # tant que la position actuelle n'est pas la destination
            if self.plateau.get_plateau()[actuel_x][actuel_y][0] is not None: # si la case n'est pas vide
                return False # le chemin n'est pas libre
            # avancer d'un pas
            actuel_x += step_x 
            actuel_y += step_y 
        return True # le chemin est libre

    def mouvement_valide(self, start, end):
        start_x, start_y = start # position de départ
        end_x, end_y = end # position d'arrivée
        piece, _ = self.plateau.get_plateau()[start_x][start_y] # pièce à déplacer
        destination_piece, _ = self.plateau.get_plateau()[end_x][end_y] # pièce à la destination

        if destination_piece is not None:
            return False # la case d'arrivée n'est pas vide

        if piece == 1:  # reine
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y: # déplacement diagonale ou orthogonal
                return self.chemin_libre(start, end) 
        elif piece == 2:  # tour
            if start_x == end_x or start_y == end_y: # déplacement orthogonal
                return self.chemin_libre(start, end) 
        return False

    def deplacer_pion(self, i, j):
        if self.mouvement_valide(self.tour_joueur[1], (i, j)): # si le mouvement est valide
            plateau = self.plateau.get_plateau()
            plateau[i][j] = plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] # déplacer le pion
            plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (None, None) # vider la case de départ
            self.effacer_previsualisation() # effacer les mouvements prévisualisés
            return True
        else:
            self.label_instruction.config(text="Mouvement invalide") # le mouvement n'est pas valide
            return False

    def event_click_pion(self, i, j):
        case = self.plateau.get_plateau()[i][j] # récupérer la case cliquée
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.label_instruction.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # bouger le pion du joueur vers cette case vide
                if not self.deplacer_pion(i, j):
                    return
                if self.check_victoire(): # vérifier si un joueur a gagné
                    self.label_tour_joueur.config(text="Victoire pour le joueur " + str(self.joueur_actuel + 1))  # afficher le joueur gagnant
                self.effacer_previsualisation() # effacer les mouvements prévisualisés
        else:
            # la case a un pion qui n'appartient pas au joueur
            if self.tour_joueur[0] != case[1]:
                # on ne peut pas sélectionner un pion qui n'est pas le notre
                self.label_instruction.config(text="Ce n'est pas votre pion.")
                return
            else:  # la case a un pion qui appartient au joueur
                # on remplace l'ancienne selection par la nouvelle
                self.label_instruction.config(
                    text=f"Vous avez sélectionné le pion {i}, {j}")
                self.tour_joueur[1] = (i, j)
                self.afficher_mouvements_possibles(i, j)
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.update_tkinter()  # mettre à jour le jeu tkinter
        
    def update_tkinter(self): 
        self.canvas.delete("all") # effacer le canvas
        self.effacer_previsualisation() # effacer les mouvements prévisualisés
        self.dessiner_jeu() # redessiner le jeu
        self.canvas.bind("<Button-1>", self.event_click_canvas) # event click sur le canvas

    def event_click_canvas(self, event):
        x = event.x # position x du click relative au board (canvas tkinter)
        y = event.y # position y du click relative au board (canvas tkinter)
        taille = self.plateau.get_taille() 
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        i = int(y // hauteur_cellule) 
        j = int(x // largeur_cellule)
        self.afficher_deplacements_possibles(i, j)

    def afficher_deplacements_possibles(self, i, j):
        piece = self.plateau.get_plateau()[i][j][0] # récupérer la pièce sur la case
        if piece is not None:
            moves = self.get_deplacements_possibles(i, j) # récupérer les mouvements possibles
            self.dessiner_deplacements_possibles(moves) # dessiner les mouvements possibles
             
    def get_deplacements_possibles(self, i, j):
        taille = self.plateau.get_tailles()
        possible_moves = []
        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)):
                    possible_moves.append((x, y))
        return possible_moves

    def dessiner_deplacements_possibles(self, moves):
        for move in moves: # pour chaque mouvement possible (x, y)
            x, y = move
            x0 = y * (self.canvas_width / self.plateau.get_taille())
            y0 = x * (self.canvas_height / self.plateau.get_taille())
            x1 = (y + 1) * (self.canvas_width / self.plateau.get_taille())
            y1 = (x + 1) * (self.canvas_height / self.plateau.get_taille())
            self.canvas.create_rectangle(x0, y0, x1, y1, tags="previsualisation") # dessiner le mouvement possible

    def effacer_previsualisation(self):
        self.canvas.delete("previsualisation")

    def check_victoire(self):
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
        self.update_tkinter() # mettre à jour le jeu tkinter
        self.root.mainloop() # lancer le jeu
