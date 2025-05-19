import sys
from config import INTERFACE_MODE
from game import Game

def is_micropython():
    """Detects if we're running on MicroPython"""
    return hasattr(sys.implementation, 'name') and sys.implementation.name == 'micropython'

def main():
    print("Starting Simon Says game...")  # Initial debug
    
    # Select interface based on configuration
    if INTERFACE_MODE == 'cli':
        from interfaces.cli import CLIInterface
        interface = CLIInterface()
    else:
        from interfaces.hardware import HardwareInterface
        interface = HardwareInterface()

    try:
        # Initialize the game
        interface.setup()
        game = Game(interface)
        game.start()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        interface.cleanup()

if __name__ == "__main__":
    main()