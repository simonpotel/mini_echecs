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
        self.root.title = ("mini_echecs")
        self.canvas_width = 800
        self.canvas_height = 800
        self.canvas = tk.Canvas(
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.draw_plateau()

    def draw_plateau(self):
        taille = self.plateau.get_taille()
        cell_width = self.canvas_width / taille
        cell_height = self.canvas_height / taille
        margin = 10

        for i in range(taille + 1):
            self.canvas.create_line(0, i * cell_height, self.canvas_width,
                                    i * cell_height)
            self.canvas.create_line(i * cell_width, 0, i * cell_width, self.canvas_height)
        
        for i in range(taille):
            for j in range(taille):
                piece, joueur = self.plateau.get_plateau()[i][j]
                if piece is not None:
                    if piece == 1:  # reine
                        color = ref_couleurs[f"reine_joueur_{joueur + 1}"]
                    elif piece == 2:  # tour
                        color = ref_couleurs[f"tours_joueur_{joueur + 1}"]
                    x0 = j * cell_width + margin
                    y0 = i * cell_height + margin
                    x1 = (j + 1) * cell_width - margin
                    y1 = (i + 1) * cell_height - margin
                    self.canvas.create_oval(x0, y0, x1, y1, fill=color)
                    

    def run(self):
        self.root.mainloop()