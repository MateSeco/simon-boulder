from machine import Pin
from utime import sleep
from game import Game

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
game = Game()
while True:
    try:
        game.add_guess()
        game.show_guess()
        game.enter_play()
        sleep(2) # sleep 1sec
    except KeyboardInterrupt:
        break
print("Finished.")