import os
from config import INTERFACE_MODE
from game import Game

def main():
    # Seleccionar interfaz basada en la configuración
    if INTERFACE_MODE == 'cli':
        from interfaces.cli import CLIInterface
        interface = CLIInterface()
    else:
        from interfaces.hardware import HardwareInterface
        interface = HardwareInterface()

    try:
        # Inicializar el juego
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