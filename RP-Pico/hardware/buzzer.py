from time import sleep
from config import PIN_CONFIG

# Detect if we're running on MicroPython or standard Python
try:
    from machine import Pin, PWM
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False
    print("Running in simulation mode (no hardware)")

class BuzzerManager:
    def __init__(self):
        """Initialize the buzzer"""
        self.buzzer = None
        if HARDWARE_MODE:
            try:
                buzzer_pin = PIN_CONFIG['BUZZER']
                self.buzzer_pin = Pin(buzzer_pin)
                self.buzzer = PWM(self.buzzer_pin)
                print(f"Buzzer configured on pin {buzzer_pin}")
            except Exception as e:
                print(f"Error configuring buzzer: {e}")
                self.buzzer = None
        else:
            print("Buzzer in simulation mode")

    def play_tone(self, freq, duration_ms):
        """Play a tone with specified frequency and duration
        
        Args:
            freq (int): Frequency in Hz
            duration_ms (int): Duration in milliseconds
        """
        if HARDWARE_MODE and self.buzzer:
            try:
                self.buzzer.freq(freq)
                self.buzzer.duty_u16(32768)  # 50% duty cycle
                sleep(duration_ms / 1000.0)
                self.buzzer.duty_u16(0)
            except Exception as e:
                print(f"Error playing tone: {e}")
                self.cleanup()
        else:
            print(f"[SIMULATION] Playing tone at {freq}Hz for {duration_ms}ms")
            sleep(duration_ms / 1000.0)

    def play_sequence(self, sequence):
        """Play a sequence of tones [(frequency, duration_ms),...]"""
        for freq, duration_ms in sequence:
            self.play_tone(freq, duration_ms)
            sleep(0.05)  # Small pause between notes

    def cleanup(self):
        """Clean up buzzer resources"""
        if HARDWARE_MODE and self.buzzer:
            try:
                self.buzzer.duty_u16(0)
                self.buzzer.deinit()
            except Exception as e:
                print(f"Error during buzzer cleanup: {e}") 