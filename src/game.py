from src.player import Player
from src.board import Board
from src.render import Render
from src.bot import Bot
from src.sounds import Sounds
import json
import os


class Game:
    """
    class Game : représente le mini game d'échecs avec les règles et les composants du game.
    """

    def __init__(self, size_board, bot_game, game_name):
        """
        procédure: initialise les composants du game et l'interface graphique.
        """
        self.players = [Player(), Player()]  # 0 = player 1 / 1 = player 2
        # board de game (board) avec tableau de tuples (piece, player)
        self.board = Board(size_board, self.players)
        # [player_current, piece_selectionne(x, y)]
        self.round_player = [0, (None, None)]
        self.render = None
        # true si le jeu est en mode bot sinon false, on considère le joueur 2 comme le bot si bot_game est True
        self.bot_game = bot_game
        self.bot = None if not bot_game else Bot(game=self)
        self.game_name = game_name
        self.sounds = Sounds()
        self.sounds.play_sound('sucess')

    def is_correct_move(self, start, end):
        """
        méthode: vérifie si un move est correct pour une pièce donnée sur un board d'échecs
        return True ou False si le move est correct ou non
        """

        start_x, start_y = start  # position de départ
        end_x, end_y = end  # position d'arrivée
        piece, _ = self.board.get_board(
        )[start_x][start_y]  # pièce à déplacer
        destination_piece, _ = self.board.get_board(
        )[end_x][end_y]  # pièce à la destination

        if destination_piece is not None:
            return False  # la case d'arrivée n'est pas vide

        if piece == 1:  # queen
            # déplacement diagonale ou orthogonal
            if abs(start_x - end_x) == abs(start_y - end_y) or start_x == end_x or start_y == end_y:
                return self.is_path_free(start, end)
        elif piece == 2:  # tower
            if start_x == end_x or start_y == end_y:  # déplacement orthogonal
                return self.is_path_free(start, end)
        return False

    def is_path_free(self, start, end):
        """
        méthode: vérifie si le path entre deux cases est free pour un move. (start(x,y) -> end(x,y))
        return True ou False si le path est free ou non
        """

        # vérifie si le path entre deux cases est free pour un move
        start_x, start_y = start
        end_x, end_y = end

        step_x = (end_x - start_x) // max(1, abs(end_x - start_x))  # pas x
        step_y = (end_y - start_y) // max(1, abs(end_y - start_y))  # pas y

        current_x, current_y = start_x + step_x, start_y + step_y  # position currentle
        # tant que la position currentle n'est pas la destination
        while (current_x, current_y) != (end_x, end_y):
            # si la case n'est pas vide
            if self.board.get_board()[current_x][current_y][0] is not None:
                return False  # le path n'est pas free
            # avancer d'un pas
            current_x += step_x
            current_y += step_y
        return True  # le path est free

    def move_piece(self, i, j):
        """
        procédure: déplace un piece sur le board de game si le move est correct
        return True ou False si le move est correct ou non
        """

        # si le move est correct
        if self.is_correct_move(self.round_player[1], (i, j)):
            board = self.board.get_board()
            board[i][j] = board[self.round_player[1][0]
                                # déplacer le piece
                                ][self.round_player[1][1]]
            board[self.round_player[1][0]][self.round_player[1][1]] = (
                None, None)  # vider la case de départ
            # delete les moves prévisualisés
            self.render.update_tkinter()
            self.sounds.play_sound('sucess')
            return True
        else:
            # le move n'est pas correct
            self.render.label_instruction.config(text="Mouvement incorrect")
            return False

    def event_click_piece(self, i, j):
        """
        procédure: gère les événements de clic sur un piece dans le game d'échecs
        permet la selection du piece et le déplacement des pieces
        """

        board = self.board.get_board()
        case = board[i][j]
        if case[0] is None:  # case vide (aucun piece)
            if self.round_player[1] == (None, None):  # aucun piece selectionné
                self.render.label_instruction.config(
                    text="Please select a piece before moving.")
                return
            else:  # piece selectionné
                # bouger le piece du player vers cette case vide
                if not self.move_piece(i, j):
                    return

                # conditions de sorties des pions adverses
                self.handle_captures(i, j)

                if self.check_win():  # vérifier si un player a gagné
                    # show le player gagnant
                    self.render.update_tkinter()
                    self.render.manage_end_game(self.round_player[0])
                    return
        else:
            # la case a un piece qui n'appartient pas au player
            if self.round_player[0] != case[1]:
                # on ne peut pas sélectionner un piece qui n'est pas le notre
                self.render.label_instruction.config(
                    text="This piece is not yours.")
                return
            else:  # la case a un piece qui appartient au player
                if self.get_moves_possibles(i, j) == []:  # aucun move possible
                    if self.round_player[1] != (None, None):
                        self.round_player[1] = (None, None)
                        self.render.update_tkinter()
                    self.render.label_instruction.config(
                        text="No possible moves for this piece.")
                    return
                # on remplace l'ancienne selection par la nouvelle
                match case[0]:
                    case 1:  # queen
                        piece_type_msg = "votre queen"
                        self.players[self.round_player[0]
                                     ].set_coords_queen((i, j))
                    case 2:  # tower
                        piece_type_msg = "une tower"

                self.render.label_instruction.config(text=f"You have selected the piece {
                    piece_type_msg} ({i}, {j})")
                self.round_player[1] = (i, j)

                self.render.show_player_selection(i, j)
                self.save_game()
                self.sounds.play_sound('select')
                return

        # réinitialiser la case selectionnée pour le prochain player
        self.round_player[1] = (None, None)
        # définition du tower du player suivant
        self.round_player[0] = 0 if self.round_player[0] == 1 else 1
        self.render.update_tkinter()  # mettre à jour le game tkinter

        if self.bot_game and self.round_player[0] == 1:
            self.bot.play()
        self.save_game()

    def handle_captures(self, i, j):
        """
        méthode: gère la capture des pions dans le rectangle formé par la reine et la pièce déplacée
        """
        board = self.board.get_board()
        queen_coords = self.players[self.round_player[0]].get_coords_queen()
        captured = False
        if i != queen_coords[0] and j != queen_coords[1]:
            rectangle_sommets = [
                (i, j),
                (i, queen_coords[1]),
                queen_coords,
                (queen_coords[0], j)
            ]  # rectangle formé par les 4 sommets

            # conditions de sorties des pions adverses
            for x, y in [rectangle_sommets[1], rectangle_sommets[3]]:
                if board[x][y][1] != self.round_player[0] and board[x][y][1] is not None:
                    if board[x][y][0] == 2:
                        self.players[board[x][y][1]].loose_tower()
                        board[x][y] = (None, None)
                        captured = True
        if captured:
            self.sounds.play_sound('loss')

    def get_moves_possibles(self, i, j):
        """
        méthode: retowerne une liste de tuples représentant les moves possibles pour une pièce donnée
        """
        size = self.board.get_size()
        possible_moves = []  # liste des moves possibles pour cette pièce sur i,j
        for x in range(size):
            for y in range(size):
                if self.is_correct_move((i, j), (x, y)):
                    possible_moves.append((x, y))
        return possible_moves

    def check_win(self):
        """
        méthode : vérifie si un player a gagné la game 
        return True/False si un player a gagné ou non
        """
        board = self.board.get_board()
        size = self.board.get_size()
        pieces_player_1 = 0
        pieces_player_2 = 0

        # permet de compter le number de pieces restants pour chaque player
        for i in range(size):
            for j in range(size):
                piece, player = board[i][j]
                if piece is not None:
                    if player == 0:
                        pieces_player_1 += 1
                    else:
                        pieces_player_2 += 1

        # règles de win
        if pieces_player_1 < 3:
            return True
        elif pieces_player_2 < 3:
            return True
        return False

    def save_game(self):
        """
        méthode: sauvegarde l'état actuel du jeu dans un fichier JSON
        """
        game_state = {
            'board': self.board.get_board(),
            'round_player': self.round_player,
            'bot_game': self.bot_game,
            'players': [
                {
                    'coords_queen': player.get_coords_queen(),
                    'towers_remains': player.get_towers_remains()
                } for player in self.players
            ]
        }

        os.makedirs("saves", exist_ok=True)
        with open(f"saves/{self.game_name}.json", 'w') as file:
            json.dump(game_state, file, indent=4)

    def load_game(self):
        """
        méthode: charge l'état du jeu à partir d'un fichier JSON
        """
        file_path = f"saves/{self.game_name}.json"

        with open(file_path, 'r') as file:
            game_state = json.load(file)

        # board
        self.board.set_board(game_state['board'])
        self.board.set_size(len(game_state['board']))

        # joueurs
        for index in range(len(game_state['players'])):
            player_data = game_state['players'][index]
            player = self.players[index]
            player.set_coords_queen(
                (player_data['coords_queen'][0], player_data['coords_queen'][1]))
            player.set_towers_remains(player_data['towers_remains'])

        # round player
        self.round_player = game_state['round_player']

        # bot game
        self.bot_game = game_state['bot_game']
        self.bot = None if not self.bot_game else Bot(game=self)

    def run(self):
        """
        procédure : lance le game et met à jour le game tkinter
        """
        self.render = Render(self)  # render graphique Tkinter du game
        self.sounds.play_sound('sucess')
        self.render.root.mainloop()  # lancer le game
