import sys
from time import sleep
from config import PIN_CONFIG
from hardware.buzzer import BuzzerManager

# Detectar si estamos en MicroPython o Python estándar
try:
    from machine import Pin, PWM
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False

# Definición de notas (frecuencias en Hz)
NOTES = {
    'E3': 165,  # Azul
    'A3': 220,  # Rojo  
    'C#4': 277, # Amarillo
    'E4': 330,  # Verde
    'G4': 392,
    'C5': 523,
}

# Melodías para cada evento
SUCCESS_MELODY = [
    ('E4', 150), ('G4', 150), ('C5', 300)  # Melodía ascendente alegre
]

FAIL_MELODY = [
    ('E4', 300), ('C#4', 300), ('A3', 500)  # Melodía descendente triste
]

INTRO_MELODY = [
    ('C#4', 200), ('E4', 200), ('G4', 200), 
    ('C5', 400), ('G4', 200), ('E4', 400)  # Melodía más elaborada
]

def convert_melody_to_freq(melody):
    """Convierte una melodía de notas a frecuencias"""
    return [(NOTES[note], duration) for note, duration in melody]

class TonePlayer:
    def __init__(self):
        self.buzzer = BuzzerManager() if HARDWARE_MODE else None

    def playsong(self, notes):
        """Reproduce una secuencia de notas"""
        if HARDWARE_MODE and self.buzzer:
            try:
                freq_sequence = convert_melody_to_freq(notes)
                self.buzzer.play_sequence(freq_sequence)
            except Exception as e:
                print(f"Error reproduciendo melodía: {e}")
            finally:
                self.buzzer.cleanup()  # Asegurar que el buzzer se limpia
        else:
            # Modo simulación - solo imprime las notas
            for note, duration in notes:
                print(f"Playing note {note} for {duration}ms")
                sleep(duration/1000)

    def cleanup(self):
        """Limpia los recursos"""
        if self.buzzer:
            self.buzzer.cleanup()

# Instancia global del reproductor de tonos
_tone_player = TonePlayer()

def play_success():
    """Reproduce melodía de éxito"""
    _tone_player.playsong(SUCCESS_MELODY)

def play_fail():
    """Reproduce melodía de fallo"""
    _tone_player.playsong(FAIL_MELODY)

def play_intro():
    """Reproduce melodía de introducción"""
    _tone_player.playsong(INTRO_MELODY)

def play_color(color):
    """Reproduce el tono asociado a cada color"""
    if color == "BLUE":
        note = [('E3', 300)]
    elif color == "RED":
        note = [('A3', 300)]
    elif color == "YELLOW":
        note = [('C#4', 300)]
    elif color == "GREEN":
        note = [('E4', 300)]
    else:
        return
    _tone_player.playsong(note)

def cleanup():
    """Limpia los recursos del reproductor de tonos"""
    _tone_player.cleanup()
