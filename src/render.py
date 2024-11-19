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
        self.label = tk.Label(self.root, text="Mini Echecs")
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.label.pack()
        self.canvas.pack()
        self.label_joueur = tk.Label(self.root, text="Joueur 1", font=("Helvetica, 20"))
        self.label_joueur.pack()
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
                i * largeur_cellule, largeur_bordure, i * largeur_cellule, self.canvas_height + 0.25)  # lignes verticales


        # ligne gauche verticale
        self.canvas.create_line(largeur_bordure, largeur_bordure, largeur_bordure, self.canvas_height)
        # ligne haute horizontale
        self.canvas.create_line(largeur_bordure, largeur_bordure, self.canvas_width, largeur_bordure)

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
                    self.canvas.create_oval(x, y, w, h, fill=color)

    def run(self):
        self.root.mainloop()
