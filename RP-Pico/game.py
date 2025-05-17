import sys
import math

# Para MicroPython usamos random de una manera diferente
if hasattr(sys.implementation, 'name') and sys.implementation.name == 'micropython':
    from urandom import getrandbits
else:
    from random import randint

from time import sleep
from tones import play_color, play_success, play_fail, play_intro

colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']

class Game:
    def __init__(self, interface):
        self.interface = interface
        self.simon = []
        self.guess = []

    def __random_color(self):
        if hasattr(sys.implementation, 'name') and sys.implementation.name == 'micropython':
            return colors[getrandbits(2)]  # 2 bits dan números de 0 a 3
        else:
            return colors[randint(0, 3)]
    
    def add_color(self):
        self.simon.append(self.__random_color())
    
    def reset_game(self):
        print("RESET")
        self.simon.clear()
        self.guess.clear()
        play_intro()

    def enter_color(self):
        color = None
        while color is None:
            print('Enter a color: ')
            # TODO: Replace for press button 
            color = sys.stdin.readline().rstrip('\n')
            print('LUEGO a color: ')
        play_color(color)
        # TODO: Turn on associated light
        self.guess.append(color)

    def enter_guess(self):
        i = 0
        while i < len(self.simon):
            self.enter_color()
            print('GUESS: ', self.simon, ' PLAY: ', self.guess)
            if not self.simon[i] == self.guess[i]:
                print("YOU LOOSE")
                play_fail()
                sleep(2)
                return False  # Indica que perdió pero no termina el juego
            print('SONIDO: ', self.guess[i])
            play_color(self.guess[i])
            sleep(1)
            i += 1
        print("SUCCESS!")
        play_success()
        sleep(2)
        self.guess.clear()
        return True

    def show_simon(self):
        for color in self.simon:
            print('SHOW: ',color)
            play_color(color)
            # TODO: Turn on associated light 
            sleep(1)

    def start(self):
        while True:  # Bucle infinito principal
            self.reset_game()  # Reinicia el juego
            while True:  # Bucle de la ronda actual
                self.add_color()
                self.show_simon()
                if not self.enter_guess():
                    break  # Sale al bucle principal para reiniciar
                sleep(1)  # Pausa entre rondas exitosas
            
