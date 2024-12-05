from src.game import Game
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os


class Loader:
    """
    class Loader : représente le GUI de configuration du jeu avant de lancer une partie.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini-Échecs: Loader")
        self.setup_initial_ui()
        self.root.mainloop()

    def setup_initial_ui(self):
        """
        procédure qui setup l'interface graphique pour charger le jeu
        """
        tk.Label(self.root, text="Game Name:").pack(pady=10)
        self.entry_game_name = ttk.Combobox(self.root)
        self.entry_game_name['values'] = self.get_saved_games()
        self.entry_game_name.pack(pady=10)
        self.entry_game_name.bind(
            "<<ComboboxSelected>>", self.on_game_name_change)
        self.entry_game_name.bind("<KeyRelease>", self.on_game_name_change)

        self.board_size_label = tk.Label(self.root, text="Board size (6-12):")
        self.entry_size = tk.Entry(self.root)
        self.entry_size.insert(0, "8")

        self.bot_game_var = tk.BooleanVar()
        self.bot_game_checkbutton = tk.Checkbutton(
            self.root, text="Bot Game", variable=self.bot_game_var)

        tk.Button(self.root, text="Load Game",
                  command=self.load_game).pack(pady=10)

    def get_saved_games(self):
        """
        méthode qui retourne une liste des noms de jeux sauvegardés
        """
        saves_dir = 'saves'
        if not os.path.exists(saves_dir):
            os.makedirs(saves_dir)
        saved_games = []
        for files in os.listdir(saves_dir):
            if files.endswith('.json'):
                saved_games.append(files.replace('.json', ''))
        return saved_games

    def on_game_name_change(self, event):
        """
        méthode qui vérifie si le nom du jeu existe dans les sauvegardes et ajuste l'interface utilisateur
        """
        game_name = self.entry_game_name.get()
        if game_name in self.get_saved_games():
            self.board_size_label.pack_forget()
            self.entry_size.pack_forget()
            self.bot_game_checkbutton.pack_forget()
        else:
            self.board_size_label.pack(pady=10)
            self.entry_size.pack(pady=10)
            self.bot_game_checkbutton.pack(pady=10)

    def load_game(self):
        """
        procédure qui charge le jeu avec la taille du board entrée par l'utilisateur
        """
        try:
            game_name = self.entry_game_name.get()
            size_board = int(self.entry_size.get())
            bot_game = self.bot_game_var.get()
            if not game_name:
                messagebox.showerror("Error", "Please enter a game name.")
                return
            if game_name in self.get_saved_games() or (6 <= size_board <= 12):
                self.root.destroy()
                game = Game(size_board, bot_game, game_name)
                if game_name in self.get_saved_games():
                    game.load_game()
                game.run()
                self.ask_replay()
            else:
                messagebox.showerror(
                    "Error", "Board size must be between 6 and 12.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a correct number.")

    def ask_replay(self):
        """
        procédure qui demande si l'utilisateur veut rejouer après la fin de la partie 
        ou 
        une fermerture de la fenêtre tkinter du jeu
        """
        replay = messagebox.askyesno(
            "Mini-Échecs: Loader", "Do you want to replay a new game ?")
        if replay:
            self.__init__()
