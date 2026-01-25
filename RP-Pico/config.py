# Detect if we're running on MicroPython or standard Python
try:
    import sys
    is_micropython = sys.implementation.name == 'micropython'
except:
    is_micropython = False

def get_interface_mode():
    return 'hardware' if is_micropython else 'cli'

INTERFACE_MODE = get_interface_mode()

# Pin configuration
PIN_CONFIG = {
    'RED': {'led': 2, 'button': 6},
    'GREEN': {'led': 3, 'button': 7},
    'BLUE': {'led': 4, 'button': 8},
    'YELLOW': {'led': 5, 'button': 9},
    'RESET': {'button': 10},
    'BUZZER': 15
}

# Game configuration
COLORS = ['RED', 'GREEN', 'BLUE', 'YELLOW']
DEBOUNCE_TIME = 0.2  # seconds
SEQUENCE_DELAY = 0.5  # seconds
POWER_SAVE_TIMEOUT = 60  # seconds without interaction

# Display timing
SHOW_COLOR_MS = 400  # Duration to show each color in sequence
PAUSE_BETWEEN_MS = 100  # Pause between colors
FEEDBACK_MS = 150  # Duration of button press feedback

# Sound configuration
SOUND_FREQUENCIES = {
    'RED': 262,     # C4
    'GREEN': 294,   # D4
    'BLUE': 330,    # E4
    'YELLOW': 349,  # F4
    'SUCCESS': [262, 294, 330, 349],
    'FAIL': [349, 330, 294, 262],
    'RESET': [262, 262, 262]
}
