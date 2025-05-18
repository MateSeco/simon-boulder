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
        self._log_available_buttons()  # Agregar logging de botones disponibles

    def _log_available_buttons(self):
        print("Botones disponibles:", list(self.buttons.keys()))

    def setup_buttons(self):
        try:
            for color, config in PIN_CONFIG.items():
                # Verificar si config es un diccionario y tiene una entrada para 'button'
                if isinstance(config, dict) and 'button' in config:
                    try:
                        self.buttons[color] = Pin(config['button'], Pin.IN, Pin.PULL_UP)
                        self.last_press[color] = 0
                        # Configurar interrupciones solo para botones existentes
                        self.buttons[color].irq(trigger=Pin.IRQ_FALLING, 
                                              handler=lambda p, c=color: self._button_callback(c))
                        print(f"Botón {color} configurado en pin {config['button']}")
                    except Exception as e:
                        print(f"No se pudo configurar botón {color}: {e}")
        except Exception as e:
            raise ButtonError(f"Error setting up buttons: {str(e)}")

    def _button_callback(self, color):
        try:
            current_time = time.ticks_ms()
            last_time = self.last_press.get(color, 0)
            if time.ticks_diff(current_time, last_time) > (DEBOUNCE_TIME * 1000):  # Convertir a ms
                print(f"Button press detected: {color}")  # Debug
                self.last_press[color] = current_time
                if color in self.callbacks:
                    self.callbacks[color]()
        except Exception as e:
            print(f"Error in button callback: {e}")

    def register_callback(self, color, callback):
        self.callbacks[color] = callback

    def cleanup(self):
        for button in self.buttons.values():
            button.irq(handler=None)
