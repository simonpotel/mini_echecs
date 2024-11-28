class Joueur:
    """
    class Joueur : représente un joueur
    avec ses coordonnées de reine et le nombre de tours restants
    """
    def __init__(self):
        self.coordonnees_reine = (None, None)
        self.tours_restantes = None

    def set_tours_restantes(self, nombre_tours):
        self.tours_restantes = nombre_tours

    def perdre_tour(self):
        self.tours_restantes -= 1

    def set_coordonnees_reine(self, x, y):
        self.coordonnees_reine = (x, y)

    def get_coordonnees_reine(self):
        return self.coordonnees_reine

    def get_tours_restantes(self):
        return self.tours_restantes
