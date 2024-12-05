class Bot:
    """
    class Bot : classe qui gère le bot (joueur 2) du jeu
    """

    def __init__(self, game):
        self.game = game

    def play(self):
        """
        méthode: fait jouer le bot (joueur 2) en effectuant le meilleur mouvement possible
        """
        board = self.game.board.get_board()
        size = self.game.board.get_size()
        best_move = None
        max_captures = -1

        for i in range(size):
            for j in range(size):
                if board[i][j][1] == 1:  # si c'est une pièce du bot
                    # récupérer les moves possibles pour le bot avec cette pièce
                    possible_moves = self.game.get_moves_possibles(i, j)
                    # pour chaque move possible (x, y) on simule le mouvement et on compte le nombre de pièces capturées
                    for move in possible_moves:
                        captures = self.simulate_move_and_count_captures(
                            (i, j), move)
                        if captures > max_captures:  # si le nombre de pièces capturées est supérieur au max capturé
                            max_captures = captures  # on met à jour le max capturé
                            # on met à jour le meilleur move
                            best_move = (i, j, move[0], move[1])

        if best_move is not None:
            self.game.round_player[1] = (best_move[0], best_move[1])
            self.game.move_piece(best_move[2], best_move[3])

            if board[best_move[2]][best_move[3]][0] == 1:
                self.game.players[1].set_coords_queen(
                    (best_move[2], best_move[3]))

            self.game.handle_captures(best_move[2], best_move[3])
            if self.game.check_win():  # vérifier si le bot a gagné
                # show le player gagnant
                self.game.render.update_tkinter()
                self.game.render.manage_end_game(self.game.round_player[0])
                return
            else:
                self.game.round_player[1] = (None, None)
                self.game.round_player[0] = 0
                self.game.render.update_tkinter()
        else:
            self.game.render.label_instruction.config(
                text="Bot cannot make a move.")
            self.game.round_player[1] = (None, None)
            self.game.round_player[0] = 0
            self.game.render.update_tkinter()

    def simulate_move_and_count_captures(self, start, end):
        """
        méthode: simule un mouvement et compte le nombre de pièces capturées
        """
        board = self.game.board.get_board()
        temp_board = [row[:] for row in board]  # copier le board

        temp_board[end[0]][end[1]] = temp_board[start[0]
                                                # déplacer la pièce
                                                ][start[1]]
        # supprimer la pièce de l'ancienne position
        temp_board[start[0]][start[1]] = (None, None)

        captures = 0
        # définir les coordonnées de la reine
        queen_coords = self.game.players[1].get_coords_queen()
        # si la pièce déplacée n'est pas sur la même ligne ou colonne que la reine
        if end[0] != queen_coords[0] and end[1] != queen_coords[1]:
            rectangle_sommets = [  # définir les sommets du rectangle formé par la reine et la pièce déplacée
                (end[0], end[1]),
                (end[0], queen_coords[1]),
                queen_coords,
                (queen_coords[0], end[1])
            ]
            # pour chaque sommet du rectangle (sauf la reine)
            for x, y in [rectangle_sommets[1], rectangle_sommets[3]]:
                # si la pièce n'appartient pas au bot
                if temp_board[x][y][1] != 1 and temp_board[x][y][1] is not None:
                    # si c'est une tour (on ne peut pas prendre la reine selon les règles)
                    if temp_board[x][y][0] == 2:
                        captures += 1  # on incrémente le nombre de pièces capturées

        return captures