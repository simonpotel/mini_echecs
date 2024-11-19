from loguru import logger
from src.jeu import Jeu

if __name__ == "__main__":
    jeu = Jeu(taille_plateau=8)
    jeu.run()
