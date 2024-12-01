import tkinter as tk


class Rendu:
    """
    class Rendu : gère l'interface graphique du jeu avec tkinter et les événements de clic sur le canvas
    pour le déplacement des pions et le déroulement du jeu.
    """

    def __init__(self, jeu):
        self.jeu = jeu
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
        self.label_tour_joueur.config(
            text=f"Joueur {self.jeu.tour_joueur[0] + 1}")

        taille = self.jeu.plateau.get_taille()
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
                piece, joueur = self.jeu.plateau.get_plateau()[i][j]
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
                    rect, '<Button-1>', lambda event, i=i, j=j: self.jeu.event_click_pion(i, j))
                if piece is not None:  # si la case contient un pion
                    if piece == 1:  # reine
                        # couleur de la reine en fonction du joueur
                        color = self.jeu.ref_couleurs[f"reine_joueur_{
                            joueur + 1}"]
                    elif piece == 2:  # tour
                        # couleur de la tour en fonction du joueur
                        color = self.jeu.ref_couleurs[f"tours_joueur_{
                            joueur + 1}"]
                    # dessiner le pion sur le canvas
                    pion = self.canvas.create_oval(x, y, w, h, fill=color)
                    # event click sur un pion
                    self.canvas.tag_bind(
                        pion, '<Button-1>', lambda event, i=i, j=j: self.jeu.event_click_pion(i, j))

    def afficher_selection_joueur(self, i, j):
        """
        procédure: Affiche la sélection du joueur et les mouvements possibles sur le plateau.
        """

        # effacer les mouvements prévisualisés auparavant
        self.canvas.delete("previsualisation")
        taille = self.jeu.plateau.get_taille()
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
                if self.jeu.mouvement_valide((i, j), (x, y)):
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
        taille = self.jeu.plateau.get_taille()
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
        piece = self.jeu.plateau.get_plateau()[i][j][0]
        if piece is not None:
            moves = self.jeu.get_deplacements_possibles(
                i, j)  # récupérer les mouvements possibles
            # dessiner les mouvements possibles
            self.dessiner_deplacements_possibles(moves)

    def dessiner_deplacements_possibles(self, moves):
        """
        procédure: dessine les déplacements possibles sur le plateau de jeu
        """
        for move in moves:  # pour chaque mouvement possible (x, y)
            x, y = move
            x0 = y * (self.canvas_width / self.jeu.plateau.get_taille())
            y0 = x * (self.canvas_height / self.jeu.plateau.get_taille())
            x1 = (y + 1) * (self.canvas_width / self.jeu.plateau.get_taille())
            y1 = (x + 1) * (self.canvas_height / self.jeu.plateau.get_taille())
            # dessiner le mouvement possible
            self.canvas.create_rectangle(
                x0, y0, x1, y1, tags="previsualisation")
