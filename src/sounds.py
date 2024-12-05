import threading 
from playsound import playsound


class Sounds():
    def __init__(self):
        self.sounds = {
            'sucess': 'assets/sounds/sucess.wav',
            'loss': 'assets/sounds/loss.wav',
            'select': 'assets/sounds/select.wav'
        }
        
    def play_sound(self, sound):
        # joue un son dans un thread en parallèle temporaire (1 sec max) pour ne pas bloquer le jeu et avoir un jeu fluide
        threading.Thread(target=playsound, args=(self.sounds[sound],)).start()