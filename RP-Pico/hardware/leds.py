from machine import Pin
from utils.exceptions import LEDError
from config import PIN_CONFIG

class LEDManager:
    def __init__(self):
        self.leds = {}
        self.setup_leds()

    def setup_leds(self):
        try:
            for color, pins in PIN_CONFIG.items():
                if 'led' in pins:
                    self.leds[color] = Pin(pins['led'], Pin.OUT)
        except Exception as e:
            raise LEDError(f"Error setting up LEDs: {str(e)}")

    def turn_on(self, color):
        try:
            self.leds[color].value(1)
        except Exception as e:
            raise LEDError(f"Error turning on LED {color}: {str(e)}")

    def turn_off(self, color):
        try:
            self.leds[color].value(0)
        except Exception as e:
            raise LEDError(f"Error turning off LED {color}: {str(e)}")

    def cleanup(self):
        for led in self.leds.values():
            led.value(0)
