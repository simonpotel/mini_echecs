from loguru import logger 

class Tour():
    def __init__(self, joueur):
        self.coordonnes = (None, None)
        self.joueur = joueur
    
    def get_coordonnes(self):
        return self.coordonnes

    def set_coordonnes(self, coordonnes):
        self.coordonnes = coordonnes

    def get_joueur(self):
        return self.joueur