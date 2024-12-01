class Player:
    """
    class Player : représente un player
    avec ses coordonnées de queen et le number de towers restants
    """

    def __init__(self):
        self.coords_queen = (None, None)
        self.towers_remains = None

    def set_towers_remains(self, number_towers):
        self.towers_remains = number_towers

    def loose_tower(self):
        self.towers_remains -= 1

    def set_coords_queen(self, coords):
        self.coords_queen = coords

    def get_coords_queen(self):
        return self.coords_queen

    def get_towers_remains(self):
        return self.towers_remains
