import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class Render:
    """
    class Render : gère l'interface graphique du game avec tkinter et les événements de clic sur le canvas
    pour le déplacement des pieces et le déroulement du game.
    """
    ref_colors = {
        "queen_player_1": "purple",
        "towers_player_1": "blue",
        "queen_player_2": "orange",
        "towers_player_2": "red"
    }

    def __init__(self, game):
        self.game = game
        self.bot_game = self.game.bot_game
        self.root = tk.Tk()  # fenêtre principale tkinter
        self.root.title("Mini-Échecs")  # titre de la fenêtre
        self.root.geometry("800x800")  # size de la fenêtre
        self.canvas_width = 600  # height du board
        self.canvas_height = 600  # width du board
        self.label_instruction = tk.Label(self.root, text="Your turn to play :", font=(
            "Roboto, 15"))  # label tkinter instruction de game
        self.label_instruction.pack(pady=(10, 0))  # margin top 10
        self.label_round_player = tk.Label(self.root, text="Player 1", font=(
            "Roboto, 20"))  # label tkinter tower du player
        self.label_round_player.pack(pady=(0, 10))  # margin bottom 10
        self.label_bot_game = tk.Label(self.root, text="Bot Game: Yes" if self.bot_game else "Bot Game: No", font=(
            "Roboto, 15"))  # label tkinter pour indiquer si c'est un bot game
        self.label_bot_game.pack(pady=(0, 10))  # margin bottom 10
        self.canvas = tk.Canvas(
            # canvas tkinter pour draw le board
            self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(pady=(10, 0))  # margin top 10
        self.load_images()
        self.draw_game()  # dessine le board

    def load_images(self):
        """
        procédure: charge les images des pièces et les redimensionne pour s'adapter aux cellules du board.
        """
        self.images = {}
        size = self.game.board.get_size()
        height_cell = self.canvas_height // size

        pieces = ["queen", "tower"]  # liste des pièces
        max_height = 0
        piece_images = {}

        for piece in pieces:  # pour chaque pièce
            for player in [0, 1]:  # pour chaque player
                # chargement de l'image qu'on utilisera sur le canvas
                image_path = f"assets/chess/{player}_{piece}.png"
                image = Image.open(image_path)
                piece_images[f"{piece}_player_{player + 1}"] = image
                if image.height > max_height:  # si la hauteur de l'image est supérieure à la hauteur maximale trouvée
                    max_height = image.height  # on définit la taille maximale des images

        # ratio de redimensionnement pour fait fit les images dans les cellules
        ratio = height_cell / max_height

        # redimensionnement des images avec le ratio
        for key, image in piece_images.items():
            width = int(image.width * ratio)
            height = int(image.height * ratio)
            resized_image = image.resize((width, height), Image.LANCZOS)
            self.images[key] = ImageTk.PhotoImage(resized_image)

    def draw_game(self):
        """
        procédure: dessine le board de game et les pièces sur le canvas.
        """

        self.label_instruction.config(
            text="Your turn to play :", font=("Helvetica, 15"))
        self.label_round_player.config(
            text=f"Player {self.game.round_player[0] + 1}")

        size = self.game.board.get_size()
        width_cell = self.canvas_width / size
        height_cell = self.canvas_height / size
        margin = 10
        width_border = 2.5

        # boucles qui dessinent les cells du board
        for i in range(size):
            for j in range(size):
                piece, player = self.game.board.get_board()[i][j]
                x = j * width_cell  # position x sur le board
                y = i * height_cell  # position y sur le board
                # width de la cell (width)
                w = (j + 1) * width_cell
                # height de la cell (height)
                h = (i + 1) * height_cell
                # couleur de la case
                color = "#EDEED2" if (i + j) % 2 == 0 else "#759656"
                # draw la cell dans le rectangle x, y, w, h
                rect = self.canvas.create_rectangle(
                    x, y, w, h, outline="", fill=color)
                self.canvas.tag_bind(
                    # event click sur la cell
                    rect, '<Button-1>', lambda event, i=i, j=j: self.game.event_click_piece(i, j))
                if piece is not None:  # si la case contient un piece
                    if piece == 1:  # queen
                        image = self.images[f"queen_player_{player + 1}"]
                    elif piece == 2:  # tower
                        image = self.images[f"tower_player_{player + 1}"]
                    # draw le piece sur le canvas
                    image_id = self.canvas.create_image(
                        x + width_cell // 2, y + height_cell // 2, image=image)
                    # event click sur un piece
                    self.canvas.tag_bind(
                        image_id, '<Button-1>', lambda _, i=i, j=j: self.game.event_click_piece(i, j))

        for i in range(size + 1):
            # lines horizontales
            self.canvas.create_line(width_border, i * height_cell, self.canvas_width,
                                    i * height_cell)
            # lines verticales
            self.canvas.create_line(
                i * width_cell, width_border, i * width_cell, self.canvas_height + 0.25)

        # ligne gauche verticale
        self.canvas.create_line(
            width_border, width_border, width_border, self.canvas_height)
        # ligne haute horizontale
        self.canvas.create_line(
            width_border, width_border, self.canvas_width, width_border)

    def show_player_selection(self, i, j):
        """
        procédure: colore la pièce selectionnée en rouge et affiche les déplacements possibles pour cette pièce
        """

        # on redraw le jeu pour faire disparaitre les anciens chemins possibles et restauré la couleur des pièces originales
        self.update_tkinter()

        # calcul dimensions des cellules
        size = self.game.board.get_size()
        width_cell = self.canvas_width / size
        height_cell = self.canvas_height / size

        # coordonnées de la cellule sélectionnée dans le canvas
        x0 = j * width_cell
        y0 = i * height_cell
        x1 = (j + 1) * width_cell
        y1 = (i + 1) * height_cell

        # applique la couleur rouge à la pièce sélectionnée
        overlapping_items = self.canvas.find_overlapping(x0, y0, x1, y1)
        for item in overlapping_items:
            if self.canvas.type(item) == "rectangle":
                self.canvas.itemconfig(item, fill="#D64933")
                break

        # recherche de tous les déplacements possibles pour CETTE pièce sélectionnée
        possible_moves = self.game.get_moves_possibles(i, j)

        for move in possible_moves:
            x, y = move
            # coordonnées des cellules des déplacements possibles dans le canvas
            x0 = y * width_cell
            y0 = x * height_cell
            x1 = (y + 1) * width_cell
            y1 = (x + 1) * height_cell

            # applique la couleur de background de cellule là où le déplacement est possible
            overlapping_items = self.canvas.find_overlapping(x0, y0, x1, y1)
            for item in overlapping_items:
                if self.canvas.type(item) == "rectangle":
                    self.canvas.itemconfig(item, fill="#F39B6D")
                    break

    def update_tkinter(self):
        """
        procédure: met à jour l'interface Tkinter en effaçant et redessinant le canvas,
        et en liant l'événement de clic sur le canvas à une fonction de gestion des événements
        """

        self.canvas.delete("all")  # delete le canvas
        # delete les moves prévisualisés
        self.draw_game()  # redraw le game
        # event click sur le canvas
        self.canvas.bind("<Button-1>", self.event_click_canvas)

    def event_click_canvas(self, event):
        """
        procédure: gère l'événement de clic sur le canvas et affiche les déplacements possibles pour la position cliquée
        """

        x = event.x  # position x du click relative au board (canvas tkinter)
        y = event.y  # position y du click relative au board (canvas tkinter)
        size = self.game.board.get_size()
        width_cell = self.canvas_width / size
        height_cell = self.canvas_height / size
        i = int(y // height_cell)
        j = int(x // width_cell)
        self.show_moves_possibles(i, j)

    def show_moves_possibles(self, i, j):
        """
        procédure: affiche les déplacements possibles pour la pièce située à la position (i, j) sur le board
        """
        # récupérer la pièce sur la case
        piece = self.game.board.get_board()[i][j][0]
        if piece is not None:
            moves = self.game.get_moves_possibles(
                i, j)  # récupérer les moves possibles
            # draw les moves possibles
            self.draw_moves_possibles(moves)

    def draw_moves_possibles(self, moves):
        """
        procédure: dessine les déplacements possibles sur le board de game
        """
        board_size = self.game.board.get_size()
        for move in moves:  # pour chaque move possible (x, y)
            x, y = move
            x0 = y * (self.canvas_width / board_size)
            y0 = x * (self.canvas_height / board_size)
            x1 = (y + 1) * (self.canvas_width / board_size)
            y1 = (x + 1) * (self.canvas_height / board_size)
            # draw le move possible
            self.canvas.create_rectangle(
                x0, y0, x1, y1, tags="prev")

    def manage_end_game(self, winner):
        """
        procédure: affiche un message de victoire pour le player gagnant
        """
        self.label_instruction.config(
            text=f"Player {winner + 1} won the game!", font=("Helvetica, 15"))
        self.label_round_player.config(
            text=f"Player {winner + 1} won the game!", font=("Helvetica, 20"))
        self.canvas.unbind("<Button-1>")
        # forcer le rendu des derniers changements tkinter sur le canvas
        self.game.render.root.update_idletasks()
        messagebox.showinfo("End Game", f"Player {winner + 1} won the game!")
        self.root.destroy()
