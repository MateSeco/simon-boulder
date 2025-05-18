from time import sleep
from config import PIN_CONFIG

# Detectar si estamos en MicroPython o Python estándar
try:
    from machine import Pin, PWM
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False
    print("Ejecutando en modo simulación (sin hardware)")

class BuzzerManager:
    def __init__(self):
        """Inicializa el buzzer"""
        self.buzzer = None
        if HARDWARE_MODE:
            try:
                # El pin del buzzer está directamente en PIN_CONFIG['BUZZER']
                buzzer_pin = PIN_CONFIG['BUZZER']
                self.buzzer_pin = Pin(buzzer_pin)
                self.buzzer = PWM(self.buzzer_pin)
                print(f"Buzzer configurado en pin {buzzer_pin}")
            except Exception as e:
                print(f"Error al configurar buzzer: {e}")
                self.buzzer = None
        else:
            print("Buzzer en modo simulación")

    def play_tone(self, freq, duration_ms):
        """Reproduce un tono con la frecuencia y duración especificadas
        
        Args:
            freq (int): Frecuencia en Hz
            duration_ms (int): Duración en milisegundos
        """
        if HARDWARE_MODE and self.buzzer:
            try:
                self.buzzer.freq(freq)
                self.buzzer.duty_u16(32768)  # 50% duty cycle
                sleep(duration_ms / 1000.0)  # Convertir ms a segundos
                self.buzzer.duty_u16(0)
            except Exception as e:
                print(f"Error al reproducir tono: {e}")
                self.cleanup()
        else:
            print(f"[SIMULACIÓN] Reproduciendo tono de {freq}Hz por {duration_ms}ms")
            sleep(duration_ms / 1000.0)  # También convertir en modo simulación

    def play_sequence(self, sequence):
        """Reproduce una secuencia de tonos [(frecuencia, duración_ms),...]"""
        for freq, duration_ms in sequence:
            self.play_tone(freq, duration_ms)
            sleep(0.05)  # Pequeña pausa entre notas

    def cleanup(self):
        """Limpia los recursos del buzzer"""
        if HARDWARE_MODE and self.buzzer:
            try:
                self.buzzer.duty_u16(0)
                self.buzzer.deinit()
            except Exception as e:
                print(f"Error durante cleanup del buzzer: {e}") 