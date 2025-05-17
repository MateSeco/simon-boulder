from machine import Pin, Timer
import time
from utils.exceptions import ButtonError
from config import PIN_CONFIG, DEBOUNCE_TIME

class ButtonManager:
    def __init__(self):
        self.buttons = {}
        self.callbacks = {}
        self.last_press = {}
        self.setup_buttons()

    def setup_buttons(self):
        try:
            for color, pins in PIN_CONFIG.items():
                if 'button' in pins:
                    self.buttons[color] = Pin(pins['button'], Pin.IN, Pin.PULL_UP)
                    self.last_press[color] = 0
                    # Configurar interrupciones
                    self.buttons[color].irq(trigger=Pin.IRQ_FALLING, 
                                          handler=lambda p, c=color: self._button_callback(c))
        except Exception as e:
            raise ButtonError(f"Error setting up buttons: {str(e)}")

    def _button_callback(self, color):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_press.get(color, 0)) > DEBOUNCE_TIME * 1000:
            self.last_press[color] = current_time
            if color in self.callbacks:
                self.callbacks[color]()

    def register_callback(self, color, callback):
        self.callbacks[color] = callback

    def cleanup(self):
        for button in self.buttons.values():
            button.irq(handler=None)
