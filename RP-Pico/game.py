import sys

# For MicroPython we use random differently
if hasattr(sys.implementation, 'name') and sys.implementation.name == 'micropython':
    from urandom import getrandbits
else:
    from random import randint

from time import sleep
from config import COLORS as colors

class Game:
    def __init__(self, interface):
        self.interface = interface
        self.simon = []
        self.guess = []
        self.running = False

    def __random_color(self):
        if hasattr(sys.implementation, 'name') and sys.implementation.name == 'micropython':
            return colors[getrandbits(2)]  # 2 bits give numbers from 0 to 3
        else:
            return colors[randint(0, 3)]
    
    def add_color(self):
        self.simon.append(self.__random_color())
    
    def reset_game(self):
        print("RESET")
        self.simon.clear()
        self.guess.clear()
        try:
            self.interface.show_intro()
        except Exception as e:
            print(f"Error playing intro melody: {e}")
        sleep(1.0)

    def enter_color(self):
        try:
            color = self.interface.read_input()
            if color == 'RESET':
                return None
            self.guess.append(color)
            return color
        except Exception as e:
            print(f"Error processing input: {e}")
            return None

    def enter_guess(self):
        i = 0
        while i < len(self.simon) and self.running:
            color = self.enter_color()
            if color is None:  # If RESET was pressed or there was an error
                return None
            
            print('GUESS: ', self.simon, ' PLAY: ', self.guess)
            if not self.simon[i] == self.guess[i]:
                print("YOU LOSE")
                try:
                    self.interface.show_failure()
                except Exception as e:
                    print(f"Error playing fail melody: {e}")
                sleep(1)
                return False
            
            print('SOUND: ', self.guess[i])
            i += 1
        
        if not self.running:
            return None
            
        print("SUCCESS!")
        try:
            self.interface.show_success()
        except Exception as e:
            print(f"Error playing success melody: {e}")
        sleep(1)
        self.guess.clear()
        return True

    def show_simon(self):
        for color in self.simon:
            if not self.running:
                return
            
            # Try to show the LED
            print(f'Showing: {color}')
            try:
                self.interface.show_color(color)
            except Exception as e:
                print(f"Error displaying LED: {e}")
            
            sleep(0.5)

    def start(self):
        self.running = True
        try:
            while self.running:  # Main loop
                self.reset_game()
                while self.running:  # Round loop
                    self.add_color()
                    self.show_simon()
                    result = self.enter_guess()
                    if result is None:  # If RESET was pressed or there was an error
                        break
                    if not result:  # If lost
                        break
                    sleep(0.5)  # Pause between successful rounds
        except Exception as e:
            print(f"Game error: {e}")
        finally:
            self.running = False
            print("Game over")

    
