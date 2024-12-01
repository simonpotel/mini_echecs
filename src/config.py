from src.game import Game
import tkinter as tk
from tkinter import messagebox


class PreConfig:
    """
    class PreConfig représente le gui de config du game avant de lancer une game
    """

    def __init__(self):
        self.root = None

        # size du board
        self.label_size = None
        self.entry_size = None
        # bouton load game
        self.bouton_load = None

    def load_gui_config(self):
        """
        procédure qui charge le gui de config du game avant de lancer une game
        """
        self.root = tk.Tk()
        self.root.title("Mini Echecs: PreConfig")

        self.label_size = tk.Label(
            self.root, text="Taille du board (6-12):")
        self.label_size.pack(pady=10)

        self.entry_size = tk.Entry(self.root)
        self.entry_size.insert(0, "8")
        self.entry_size.pack(pady=10)

        self.bouton_load = tk.Button(
            # event quand on clique sur le bouton
            self.root, text="Charger", command=self.load_game)
        self.bouton_load.pack(pady=10)

        self.root.mainloop()

    def load_game(self):
        try:
            size_board = int(self.entry_size.get())
            # size comprise entre 6 et 12 (énnoncé)
            if 6 <= size_board <= 12:
                self.root.destroy()  # ferme la fenêtre tkinter de config car plus nécessaire
                # on crée une instance de la classe Game
                game = Game(size_board)
                game.run()  # on lance la game
            else:
                messagebox.showerror(
                    "Erreur", "La size du board doit être entre 6 et 12.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un number correct.")
