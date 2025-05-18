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
        self.running = False

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
        try:
            play_intro()
        except Exception as e:
            print(f"Error en melodía de intro: {e}")

    def enter_color(self):
        try:
            color = self.interface.read_input()
            if color == 'RESET':
                return None
            play_color(color)
            self.guess.append(color)
            return color
        except Exception as e:
            print(f"Error al procesar entrada: {e}")
            return None

    def enter_guess(self):
        i = 0
        while i < len(self.simon) and self.running:
            color = self.enter_color()
            if color is None:  # Si se presionó RESET o hubo error
                return None
            
            print('GUESS: ', self.simon, ' PLAY: ', self.guess)
            if not self.simon[i] == self.guess[i]:
                print("YOU LOOSE")
                try:
                    play_fail()
                except Exception as e:
                    print(f"Error en melodía de fallo: {e}")
                sleep(1)
                return False
            
            print('SONIDO: ', self.guess[i])
            try:
                play_color(self.guess[i])
            except Exception as e:
                print(f"Error al reproducir sonido: {e}")
            sleep(0.5)
            i += 1
        
        if not self.running:
            return None
            
        print("SUCCESS!")
        try:
            play_success()
        except Exception as e:
            print(f"Error en melodía de éxito: {e}")
        sleep(1)
        self.guess.clear()
        return True

    def show_simon(self):
        for color in self.simon:
            if not self.running:
                return
            print(f'Mostrando: {color}')
            # Intentar reproducir el sonido
            try:
                play_color(color)
            except Exception as e:
                print(f"Error al reproducir sonido: {e}")
            
            # Intentar mostrar el LED
            try:
                self.interface.display_sequence(color)
            except Exception as e:
                print(f"Error al mostrar LED: {e}")
            
            sleep(0.5)

    def start(self):
        self.running = True
        try:
            while self.running:  # Bucle principal
                self.reset_game()
                while self.running:  # Bucle de ronda
                    self.add_color()
                    self.show_simon()
                    result = self.enter_guess()
                    if result is None:  # Si se presionó RESET o hubo error
                        break
                    if not result:  # Si perdió
                        break
                    sleep(0.5)  # Pausa entre rondas exitosas
        except Exception as e:
            print(f"Error en el juego: {e}")
        finally:
            self.running = False
            print("Juego terminado")

    
