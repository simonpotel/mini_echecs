from src.joueur import Joueur
from src.plateau import Plateau
from src.rendu import Rendu


class Jeu:
    """
    class Jeu : représente le mini jeu d'échecs avec les règles et les composants du jeu.
    """

    ref_couleurs = {
        "reine_joueur_1": "purple",
        "tours_joueur_1": "blue",
        "reine_joueur_2": "orange",
        "tours_joueur_2": "red"
    }

    def __init__(self, taille_plateau):
        """
        procédure: initialise les composants du jeu et l'interface graphique.
        """
        self.joueurs = [Joueur(), Joueur()]  # 0 = joueur 1 / 1 = joueur 2
        # plateau de jeu (board) avec tableau de tuples (piece, joueur)
        self.plateau = Plateau(taille_plateau, self.joueurs)
        # [joueur_actuel, pion_selectionne(x, y)]
        self.tour_joueur = [0, (None, None)]
        self.rendu = Rendu(self)  # rendu graphique Tkinter du jeu

    def mouvement_valide(self, start, end):
        """
        fonction: vérifie si un mouvement est valide pour une pièce donnée sur un plateau d'échecs
        return True ou False si le mouvement est valide ou non
        """

        start_x, start_y = start  # position de départ
        end_x, end_y = end  # position d'arrivée
        piece, _ = self.plateau.get_plateau(
        )[start_x][start_y]  # pièce à déplacer
        destination_piece, _ = self.plateau.get_plateau(
        )[end_x][end_y]  # pièce à la destination

        if destination_piece is not None:
            return False  # la case d'arrivée n'est pas vide

        if piece == 1:  # reine
            # déplacement diagonale ou orthogonal
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y:
                return self.chemin_libre(start, end)
        elif piece == 2:  # tour
            if start_x == end_x or start_y == end_y:  # déplacement orthogonal
                return self.chemin_libre(start, end)
        return False

    def chemin_libre(self, start, end):
        """
        fonction: vérifie si le chemin entre deux cases est libre pour un mouvement. (start(x,y) -> end(x,y))
        return True ou False si le chemin est libre ou non
        """

        # vérifie si le chemin entre deux cases est libre pour un mouvement
        start_x, start_y = start
        end_x, end_y = end

        step_x = (end_x - start_x) // max(1, abs(end_x - start_x))  # pas x
        step_y = (end_y - start_y) // max(1, abs(end_y - start_y))  # pas y

        actuel_x, actuel_y = start_x + step_x, start_y + step_y  # position actuelle
        # tant que la position actuelle n'est pas la destination
        while (actuel_x, actuel_y) != (end_x, end_y):
            # si la case n'est pas vide
            if self.plateau.get_plateau()[actuel_x][actuel_y][0] is not None:
                return False  # le chemin n'est pas libre
            # avancer d'un pas
            actuel_x += step_x
            actuel_y += step_y
        return True  # le chemin est libre

    def deplacer_pion(self, i, j):
        """
        procédure: déplace un pion sur le plateau de jeu si le mouvement est valide
        return True ou False si le mouvement est valide ou non
        """

        # si le mouvement est valide
        if self.mouvement_valide(self.tour_joueur[1], (i, j)):
            plateau = self.plateau.get_plateau()
            plateau[i][j] = plateau[self.tour_joueur[1][0]
                                    # déplacer le pion
                                    ][self.tour_joueur[1][1]]
            plateau[self.tour_joueur[1][0]][self.tour_joueur[1][1]] = (
                None, None)  # vider la case de départ
            # effacer les mouvements prévisualisés
            self.rendu.effacer_previsualisation()
            return True
        else:
            # le mouvement n'est pas valide
            self.rendu.label_instruction.config(text="Mouvement invalide")
            return False

    def event_click_pion(self, i, j):
        """
        procédure: gère les événements de clic sur un pion dans le jeu d'échecs
        permet la selection du pion et le déplacement des pions
        """

        plateau = self.plateau.get_plateau()
        case = plateau[i][j]
        if case[0] is None:  # case vide (aucun pion)
            if self.tour_joueur[1] == (None, None):  # aucun pion selectionné
                self.rendu.label_instruction.config(
                    text="Vous devez sélectionner un de vos pions avant de bouger.")
                return
            else:  # pion selectionné
                # bouger le pion du joueur vers cette case vide
                if not self.deplacer_pion(i, j):
                    return

                reine_coords = self.joueurs[self.tour_joueur[0]
                                            ].get_coordonnees_reine()
                if i != reine_coords[0] and j != reine_coords[1]:
                    rectangle_sommets = [
                        (i, j),
                        (i, reine_coords[1]),
                        reine_coords,
                        (reine_coords[0], j)
                    ]  # rectangle formé par les 4 sommets
                    # condition de sortie
                    for x, y in [rectangle_sommets[1], rectangle_sommets[3]]:
                        if plateau[x][y][1] != self.tour_joueur[0] and plateau[x][y][1] is not None:
                            self.joueurs[plateau[x][y][1]].perdre_tour()
                            plateau[x][y] = (None, None)

                if self.check_victoire():  # vérifier si un joueur a gagné
                    # afficher le joueur gagnant
                    self.rendu.label_tour_joueur.config(
                        text="Victoire pour le joueur " + str(self.tour_joueur[0] + 1))
                # effacer les mouvements prévisualisés
                self.rendu.effacer_previsualisation()
        else:
            # la case a un pion qui n'appartient pas au joueur
            if self.tour_joueur[0] != case[1]:
                # on ne peut pas sélectionner un pion qui n'est pas le notre
                self.rendu.label_instruction.config(
                    text="Ce n'est pas votre pion.")
                return
            else:  # la case a un pion qui appartient au joueur
                # on remplace l'ancienne selection par la nouvelle
                match case[0]:
                    case 1:  # reine
                        pion_type_msg = "votre reine"
                        self.joueurs[self.tour_joueur[0]
                                     ].set_coordonnees_reine((i, j))
                    case 2:  # tour
                        pion_type_msg = "une tour"

                self.rendu.label_instruction.config(text=f"Vous avez sélectionné {
                                                    pion_type_msg} ({i}, {j})")
                self.tour_joueur[1] = (i, j)

                self.rendu.afficher_selection_joueur(i, j)
                return

        # réinitialiser la case selectionnée pour le prochain joueur
        self.tour_joueur[1] = (None, None)
        # définition du tour du joueur suivant
        self.tour_joueur[0] = 0 if self.tour_joueur[0] == 1 else 1
        self.rendu.update_tkinter()  # mettre à jour le jeu tkinter

    def get_deplacements_possibles(self, i, j):
        """
        fonction: retourne une liste de tuples représentant les mouvements possibles pour une pièce donnée
        """
        taille = self.plateau.get_taille()
        possible_moves = []
        for x in range(taille):
            for y in range(taille):
                if self.mouvement_valide((i, j), (x, y)):
                    possible_moves.append((x, y))
        return possible_moves

    def check_victoire(self):
        """
        fonction : vérifie si un joueur a gagné la partie 
        return True/False si un joueur a gagné ou non
        """
        plateau = self.plateau.get_plateau()
        taille = self.plateau.get_taille()
        pions_joueur_1 = 0
        pions_joueur_2 = 0

        # permet de compter le nombre de pions restants pour chaque joueur
        for i in range(taille):
            for j in range(taille):
                piece, joueur = plateau[i][j]
                if piece is not None:
                    if joueur == 0:
                        pions_joueur_1 += 1
                    else:
                        pions_joueur_2 += 1

        # règles de victoire
        if pions_joueur_1 < 3:
            print("Joueur 2 a gagné")
            return True
        elif pions_joueur_2 < 3:
            print("Joueur 1 a gagné")
            return True
        return False

    def run(self):
        """
        procédure : lance le jeu et met à jour le jeu tkinter
        """
        self.rendu.update_tkinter()  # mettre à jour le jeu tkinter
        self.rendu.root.mainloop()  # lancer le jeu
