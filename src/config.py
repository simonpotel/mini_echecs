from src.jeu import Jeu
import tkinter as tk
from tkinter import messagebox


class PreConfig:
    def __init__(self):
        self.root = None
        self.label_taille = None
        self.entry_taille = None
        self.bouton_charger = None

    def charger_menu_configuration(self):
        self.root = tk.Tk()
        self.root.title("Mini Echecs: PreConfig")

        self.label_taille = tk.Label(
            self.root, text="Taille du plateau (6-12):")
        self.label_taille.pack(pady=10)

        self.entry_taille = tk.Entry(self.root)
        self.entry_taille.insert(0, "8")
        self.entry_taille.pack(pady=10)

        self.bouton_charger = tk.Button(
            self.root, text="Charger", command=self.charger_partie)
        self.bouton_charger.pack(pady=10)

        self.root.mainloop()

    def charger_partie(self):
        try:
            taille_plateau = int(self.entry_taille.get())
            if 6 <= taille_plateau <= 12:
                self.root.destroy()
                jeu = Jeu(taille_plateau)
                jeu.run()
            else:
                messagebox.showerror(
                    "Erreur", "La taille du plateau doit être entre 6 et 12.")
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer un nombre valide.")
