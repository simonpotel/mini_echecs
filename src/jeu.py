from loguru import logger
import tkinter as tk
from src.joueur import Joueur
from src.plateau import Plateau
from src.render import Render


class Jeu:
    def __init__(self, taille_plateau):
        self.plateau = Plateau(taille_plateau)
        self.joueurs = [Joueur(), Joueur()]  # joueur 1 et joueur 2
        self.render = Render(self.plateau)
