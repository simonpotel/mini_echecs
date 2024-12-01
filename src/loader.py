from src.game import Game
import tkinter as tk
from tkinter import messagebox


class Loader:
    """
    Classe Loader représente le GUI de configuration du jeu avant de lancer une partie.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Echecs: Loader")
        self.setup_initial_ui()
        self.root.mainloop()

    def setup_initial_ui(self):
        """
        procédure qui setup l'interface graphique pour charger le jeu
        """
        tk.Label(self.root, text="Board size (6-12):").pack(pady=10)
        self.entry_size = tk.Entry(self.root)
        self.entry_size.insert(0, "8")
        self.entry_size.pack(pady=10)
        tk.Button(self.root, text="Load Game",
                  command=self.load_game).pack(pady=10)

    def load_game(self):
        """
        procédure qui charge le jeu avec la taille du board entrée par l'utilisateur
        """
        try:
            size_board = int(self.entry_size.get())
            if 6 <= size_board <= 12:
                self.root.destroy()
                game = Game(size_board)
                game.run()
                self.ask_replay()
            else:
                messagebox.showerror(
                    "Erreur", "Board size must be between 6 and 12.")
        except ValueError:
            messagebox.showerror(
                "Erreur", "Please enter a correct number.")

    def ask_replay(self):
        """
        procédure qui demande si l'utilisateur veut rejouer après la fin de la partie 
        ou 
        une fermerture de la fenêtre tkinter du jeu
        """
        replay = messagebox.askyesno(
            "Echecs: Loader", "Do you want to replay a new game ?")
        if replay:
            self.__init__()
