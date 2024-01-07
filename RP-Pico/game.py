import random
import math
import sys
from utime import sleep
from tones import playsong, sounds

colors = ['RED', 'GREEN', 'BLUE', 'YELLOW']

class Game:
    def __init__(self):
        self.guess = []
        self.play = []

    def __random_color(self):
        return colors[int(math.floor(random.random() * 4))]
    
    def add_guess(self):
        self.guess.append(self.__random_color())
    
    def reset_game(self):
        print("RESET")
        self.guess.clear()
        self.play.clear()

    def enter_color(self):
        print('Enter a color: ')
        color = sys.stdin.readline().rstrip('\n')
        playsong(sounds[color])
        self.play.append(color)

    def enter_play(self):
        i = 0
        while i < len(self.guess):
            self.enter_color()
            print('GUESS: ', self.guess, ' PLAY: ', self.play)
            if not self.guess[i] == self.play[i]:
                print("YOU LOOSE")
                playsong(sounds["FAIL"])
                sleep(2)
                return self.reset_game()
            print('SONIDO: ', self.play[i])
            playsong(sounds[self.play[i]])
            sleep(1)
            i += 1
        print("SUCCESS!")
        playsong(sounds["SUCCESS"])
        sleep(2)
        self.play.clear()

    def show_guess(self):
        for color in self.guess:
            print('SHOW: ',color)
            playsong(sounds[color])
            sleep(1)
            
