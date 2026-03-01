from machine import Pin, PWM
from config import PIN_CONFIG, SOUND_FREQUENCIES
import time

class BuzzerManager:
    def __init__(self):
        """Initialize the buzzer"""
        self.buzzer = None
        try:
            buzzer_pin = PIN_CONFIG['BUZZER']
            self.buzzer = PWM(Pin(buzzer_pin))
            self.buzzer.duty_u16(0)
        except Exception as e:
            print(f"Error configuring buzzer: {e}")

    def play_tone(self, freq, duration_ms=300):
        """Play a tone with specified frequency and duration"""
        if self.buzzer:
            try:
                self.buzzer.freq(freq)
                self.buzzer.duty_u16(32768)
                time.sleep_ms(duration_ms)
                self.buzzer.duty_u16(0)
            except Exception as e:
                print(f"Error playing tone: {e}")

    def play_color(self, color, duration_ms=300):
        """Play the tone for a specific color"""
        if color in SOUND_FREQUENCIES:
            freq = SOUND_FREQUENCIES[color]
            if isinstance(freq, int):
                self.play_tone(freq, duration_ms)

    def play_melody(self, frequencies, duration_ms=150):
        """Play a sequence of frequencies"""
        for freq in frequencies:
            self.play_tone(freq, duration_ms)
            time.sleep_ms(50)

    def play_success(self):
        """Play success melody"""
        if 'SUCCESS' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['SUCCESS'], 100)

    def play_fail(self):
        """Play fail melody"""
        if 'FAIL' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['FAIL'], 200)

    def play_reset(self):
        """Play reset sound"""
        if 'RESET' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['RESET'], 100)

    def cleanup(self):
        """Clean up buzzer resources"""
        if self.buzzer:
            try:
                self.buzzer.duty_u16(0)
                self.buzzer.deinit()
            except:
                pass
