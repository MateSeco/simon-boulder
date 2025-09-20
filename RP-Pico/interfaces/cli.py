import sys
from config import COLORS

class CLIInterface:
    def __init__(self):
        self.callbacks = {}

    def setup(self):
        print("Simon Says - CLI Mode")
        print("Available colors:", ", ".join(COLORS))
        print("Type a color and press Enter to play")

    def read_input(self):
        while True:
            try:
                color = input("Enter color: ").strip().upper()
                if color in COLORS:
                    return color
            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                print("Invalid input. Try again.")

    def show_color(self, color):
        print(f"Simon says: {color}")

    def show_intro(self):
        print("Game starting...")

    def show_success(self):
        print("Success!")

    def show_failure(self):
        print("Game Over!")

    def cleanup(self):
        # Nothing to clean up in CLI mode
        pass
