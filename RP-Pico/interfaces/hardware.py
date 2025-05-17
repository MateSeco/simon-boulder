from hardware.buttons import ButtonManager
from hardware.leds import LEDManager
from config import COLORS

class HardwareInterface:
    def __init__(self):
        self.buttons = ButtonManager()
        self.leds = LEDManager()

    def setup(self):
        print("Simon Says - Hardware Mode")

    def read_input(self):
        # Temporary CLI fallback for testing
        return input("Enter color: ").strip().upper()

    def display_sequence(self, color):
        self.leds.turn_on(color)
        self.leds.turn_off(color)

    def show_success(self):
        print("Success!")

    def show_failure(self):
        print("Game Over!")

    def cleanup(self):
        self.leds.cleanup()
