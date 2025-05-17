import sys
from time import sleep

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

def playsong(notes):
    """Reproduce una secuencia de notas"""
    if HARDWARE_MODE:
        buzzer = PWM(Pin(15))
        for note, duration in notes:
            buzzer.freq(NOTES[note])
            buzzer.duty_u16(32768)  # 50% duty cycle
            sleep(duration/1000)
            buzzer.duty_u16(0)
            sleep(0.05)  # Pequeña pausa entre notas
        buzzer.deinit()
    else:
        # Modo simulación - solo imprime las notas
        for note, duration in notes:
            print(f"Playing note {note} for {duration}ms")
            sleep(duration/1000)

def play_success():
    """Reproduce melodía de éxito"""
    playsong(SUCCESS_MELODY)

def play_fail():
    """Reproduce melodía de fallo"""
    playsong(FAIL_MELODY)

def play_intro():
    """Reproduce melodía de introducción"""
    playsong(INTRO_MELODY)

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
    playsong(note)
