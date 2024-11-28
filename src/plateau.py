class Plateau:
    def __init__(self, taille, joueurs):
        self.taille = taille
        self.plateau = [[(None, None) for _ in range(taille)]
                        for _ in range(taille)]  # i = ligne, j = colonne
        self.initialise_plateau(joueurs)

    def get_plateau(self):
        return self.plateau

    def get_taille(self):
        return self.taille
    
    def initialise_plateau(self, joueurs):
        nombre_pions = (self.taille**2)//4-1  # nombre forcément impair
        # placement initial des tours
        nombre_lignes_pions = self.taille//2 # nombre de pions par ligne et nombre de lignes
        for i in range(nombre_lignes_pions):
            for j in range(nombre_lignes_pions):
                self.plateau[self.taille-1-i][j] = (2, 0) # tour joueur 1
                self.plateau[i][self.taille-1-j] = (2, 1) # tour joueur 2

        # 1 = reine / 2 = tour // 0 = joueur 1 / 1 = joueur 2
        self.plateau[self.taille-1][0] = (1, 0) # reine joueur 1
        self.plateau[0][self.taille-1] = (1, 1) # reine joueur 2
        joueurs[0].set_tours_restantes(nombre_pions)
        joueurs[0].set_coordonnees_reine(self.taille-1, 0)
        joueurs[1].set_tours_restantes(nombre_pions)
        joueurs[1].set_coordonnees_reine(0, self.taille-1)