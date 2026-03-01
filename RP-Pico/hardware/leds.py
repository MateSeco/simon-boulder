from machine import Pin
from config import PIN_CONFIG

class LEDManager:
    def __init__(self):
        self.leds = {}
        self.setup_leds()

    def setup_leds(self):
        """Setup all LEDs from PIN_CONFIG"""
        for color, config in PIN_CONFIG.items():
            if isinstance(config, dict) and 'led' in config:
                try:
                    self.leds[color] = Pin(config['led'], Pin.OUT)
                    self.leds[color].value(0)
                except Exception as e:
                    print(f"Could not configure {color} LED: {e}")

    def turn_on(self, color):
        """Turn on a specific LED"""
        if color in self.leds:
            self.leds[color].value(1)

    def turn_off(self, color):
        """Turn off a specific LED"""
        if color in self.leds:
            self.leds[color].value(0)

    def turn_all_off(self):
        """Turn off all LEDs"""
        for led in self.leds.values():
            led.value(0)

    def flash_all(self, times=3, delay_ms=100):
        """Flash all LEDs"""
        import time
        for _ in range(times):
            for led in self.leds.values():
                led.value(1)
            time.sleep_ms(delay_ms)
            for led in self.leds.values():
                led.value(0)
            time.sleep_ms(delay_ms)
