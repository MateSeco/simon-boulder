import sys
from time import sleep
from config import PIN_CONFIG
from hardware.buzzer import BuzzerManager

# Detect if we're running on MicroPython or standard Python
try:
    from machine import Pin, PWM
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False

# Note definitions (frequencies in Hz)
NOTES = {
    'E3': 165,  # Blue
    'A3': 220,  # Red  
    'C#4': 277, # Yellow
    'E4': 330,  # Green
    'G4': 392,
    'C5': 523,
}

# Melodies for each event
SUCCESS_MELODY = [
    ('E4', 150), ('G4', 150), ('C5', 300)  # Happy ascending melody
]

FAIL_MELODY = [
    ('E4', 300), ('C#4', 300), ('A3', 500)  # Sad descending melody
]

INTRO_MELODY = [
    ('C#4', 200), ('E4', 200), ('G4', 200), 
    ('C5', 400), ('G4', 200), ('E4', 400)  # More elaborate melody
]

def convert_melody_to_freq(melody):
    """Converts a melody from notes to frequencies"""
    return [(NOTES[note], duration) for note, duration in melody]

class TonePlayer:
    def __init__(self):
        self.buzzer = BuzzerManager() if HARDWARE_MODE else None

    def playsong(self, notes):
        """Plays a sequence of notes"""
        if HARDWARE_MODE and self.buzzer:
            try:
                freq_sequence = convert_melody_to_freq(notes)
                self.buzzer.play_sequence(freq_sequence)
            except Exception as e:
                print(f"Error playing melody: {e}")
            finally:
                self.buzzer.cleanup()  # Ensure buzzer is cleaned up
        else:
            # Simulation mode - just print the notes
            for note, duration in notes:
                print(f"Playing note {note} for {duration}ms")
                sleep(duration/1000)

    def cleanup(self):
        """Clean up resources"""
        if self.buzzer:
            self.buzzer.cleanup()

# Global instance of tone player
_tone_player = TonePlayer()

def play_success():
    """Play success melody"""
    _tone_player.playsong(SUCCESS_MELODY)

def play_fail():
    """Play fail melody"""
    _tone_player.playsong(FAIL_MELODY)

def play_intro():
    """Play intro melody"""
    _tone_player.playsong(INTRO_MELODY)

def play_color(color):
    """Play the tone associated with each color"""
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
    """Clean up tone player resources"""
    _tone_player.cleanup()
