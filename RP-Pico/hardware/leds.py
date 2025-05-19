from machine import Pin
from utils.exceptions import LEDError
from config import PIN_CONFIG

class LEDManager:
    def __init__(self):
        self.leds = {}
        self.setup_leds()
        self._log_available_leds()

    def _log_available_leds(self):
        print("Available LEDs:", list(self.leds.keys()))

    def setup_leds(self):
        try:
            for color, config in PIN_CONFIG.items():
                # Check if config is a dictionary and has a 'led' entry
                if isinstance(config, dict) and 'led' in config:
                    try:
                        self.leds[color] = Pin(config['led'], Pin.OUT)
                        print(f"{color} LED configured on pin {config['led']}")
                    except Exception as e:
                        print(f"Could not configure {color} LED: {e}")
        except Exception as e:
            raise LEDError(f"Error setting up LEDs: {str(e)}")

    def turn_on(self, color):
        try:
            if color in self.leds:
                self.leds[color].value(1)
            else:
                print(f"Simulating {color} LED ON (not connected)")
        except Exception as e:
            print(f"Error turning on {color} LED: {e}")

    def turn_off(self, color):
        try:
            if color in self.leds:
                self.leds[color].value(0)
            else:
                print(f"Simulating {color} LED OFF (not connected)")
        except Exception as e:
            print(f"Error turning off {color} LED: {e}")

    def cleanup(self):
        for led in self.leds.values():
            led.value(0)
