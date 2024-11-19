class Joueur:
    def __init__(self):
        self.coordonnees_reine = (None, None)
        self.pieces_restantes = None

    def set_pieces_restantes(self, nombre_pieces):
        self.pieces_restantes = nombre_pieces

    def set_coordonnees_reine(self, x, y):
        self.coordonnees_reine = (x, y)

    def get_coordonnees_reine(self):
        return self.coordonnees_reine

    def get_pieces_restantes(self):
        return self.pieces_restantes
