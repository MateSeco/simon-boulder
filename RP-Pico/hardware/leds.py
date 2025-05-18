from machine import Pin
from utils.exceptions import LEDError
from config import PIN_CONFIG

class LEDManager:
    def __init__(self):
        self.leds = {}
        self.setup_leds()
        self._log_available_leds()

    def _log_available_leds(self):
        print("LEDs disponibles:", list(self.leds.keys()))

    def setup_leds(self):
        try:
            for color, config in PIN_CONFIG.items():
                # Verificar si config es un diccionario y tiene una entrada para 'led'
                if isinstance(config, dict) and 'led' in config:
                    try:
                        self.leds[color] = Pin(config['led'], Pin.OUT)
                        print(f"LED {color} configurado en pin {config['led']}")
                    except Exception as e:
                        print(f"No se pudo configurar LED {color}: {e}")
        except Exception as e:
            raise LEDError(f"Error setting up LEDs: {str(e)}")

    def turn_on(self, color):
        try:
            if color in self.leds:
                self.leds[color].value(1)
            else:
                print(f"Simulando LED {color} encendido (no conectado)")
        except Exception as e:
            print(f"Error al encender LED {color}: {e}")

    def turn_off(self, color):
        try:
            if color in self.leds:
                self.leds[color].value(0)
            else:
                print(f"Simulando LED {color} apagado (no conectado)")
        except Exception as e:
            print(f"Error al apagar LED {color}: {e}")

    def cleanup(self):
        for led in self.leds.values():
            led.value(0)
