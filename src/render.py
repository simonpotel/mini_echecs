import tkinter as tk

ref_couleurs = {
    "reine_joueur_1": "purple",
    "tours_joueur_1": "blue",
    "reine_joueur_2": "orange",
    "tours_joueur_2": "red"
}


class Render:
    def __init__(self, plateau):
        self.plateau = plateau
        self.root = tk.Tk()
        self.root.title("mini_echecs")
        self.root.geometry("800x800")
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draw_plateau()

    def draw_plateau(self):
        taille = self.plateau.get_taille()
        largeur_cellule = self.canvas_width / taille
        hauteur_cellule = self.canvas_height / taille
        margin = 10

        largeur_bordure = 2.5

        for i in range(taille + 1):
            self.canvas.create_line(largeur_bordure, i * hauteur_cellule, self.canvas_width,
                                    i * hauteur_cellule)  # lignes horizontales
            self.canvas.create_line(
                # lignes verticales
                i * largeur_cellule, largeur_bordure, i * largeur_cellule, self.canvas_height + 0.25)

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
        self.plateau.get_plateau()[i][j] = (None, None)
        self.update_plateau()

    def update_plateau(self):
        self.canvas.delete("all")
        self.draw_plateau()

    def run(self):
        self.root.mainloop()
