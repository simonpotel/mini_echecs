class Board:
    """
    class Board: représente le board de game avec ses cases
    et les pieces présents sur celles-ci.
    """

    def __init__(self, size, players):
        self.size = size
        self.board = [[(None, None) for _ in range(size)]
                      for _ in range(size)]  # i = ligne, j = colonne
        self.initialise_board(players)

    def get_board(self):  # getter
        return self.board

    def set_board(self, board):  # setter
        self.board = board

    def get_size(self):  # getter
        return self.size

    def set_size(self, size):  # setter
        self.size = size

    def initialise_board(self, players):
        """
        procédure qui initialise le board de game avec les pieces de chaque player
        et set les coordonnées de la queen et le number de towers restants pour chaque player (par défaut en début de game)
        """
        #pieces_number = (self.size**2)//4-1  # number forcément impair
        
        # placement initial des towers
        # number de pieces par ligne et number de lines
        number_pieces_lines = self.size//2
        created_towers = 0
        for i in range(number_pieces_lines):
            for j in range(number_pieces_lines):
                self.board[self.size-1-i][j] = (2, 0)  # tower player 1
                self.board[i][self.size-1-j] = (2, 1)  # tower player 2
                created_towers += 1
        created_towers -= 1
        # 1 = queen / 2 = tower // 0 = player 1 / 1 = player 2
        self.board[self.size-1][0] = (1, 0)  # queen player 1
        self.board[0][self.size-1] = (1, 1)  # queen player 2
        # set le number de towers restants pour chaque player
        players[0].set_towers_remains(created_towers)
        # set les coordonnées de la queen pour chaque player
        players[0].set_coords_queen((self.size-1, 0))
        # set le number de towers restants pour chaque player
        players[1].set_towers_remains(created_towers)
        # set les coordonnées de la queen pour chaque player
        players[1].set_coords_queen((0, self.size-1))
