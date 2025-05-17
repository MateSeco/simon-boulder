import os

# Detectar si estamos en MicroPython o Python estándar
try:
    import sys
    is_micropython = sys.implementation.name == 'micropython'
except:
    is_micropython = False

def get_interface_mode():
    if not is_micropython:
        # En la computadora, siempre CLI
        return 'cli'
    else:
        # En la Pico, permitir elegir entre 'cli' y 'hardware'
        try:
            # Por defecto usar hardware en la Pico
            return os.getenv('SIMON_INTERFACE', 'hardware')
        except:
            return 'hardware'

INTERFACE_MODE = get_interface_mode()

# Configuración de pines
PIN_CONFIG = {
    'RED': {'led': 2, 'button': 6},
    'GREEN': {'led': 3, 'button': 7},
    'BLUE': {'led': 4, 'button': 8},
    'YELLOW': {'led': 5, 'button': 9},
    'RESET': {'button': 10}
}

# Configuración del juego
COLORS = ['RED', 'GREEN', 'BLUE', 'YELLOW']
DEBOUNCE_TIME = 0.2  # segundos
SEQUENCE_DELAY = 0.5  # segundos
POWER_SAVE_TIMEOUT = 60  # segundos sin interacción

# Configuración de sonidos
SOUND_FREQUENCIES = {
    'RED': 262,     # Do
    'GREEN': 294,   # Re
    'BLUE': 330,    # Mi
    'YELLOW': 349,  # Fa
    'SUCCESS': [262, 294, 330, 349],
    'FAIL': [349, 330, 294, 262],
    'RESET': [262, 262, 262]
}
