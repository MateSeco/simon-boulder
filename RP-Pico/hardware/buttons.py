from machine import Pin
import time
from config import PIN_CONFIG, DEBOUNCE_TIME

class ButtonManager:
    def __init__(self):
        self.buttons = {}
        self.callbacks = {}
        self.last_press = {}
        self.last_state = {}
        self.setup_buttons()
        self._log_available_buttons()

    def _log_available_buttons(self):
        print("Available buttons:", list(self.buttons.keys()))

    def setup_buttons(self):
        """Setup buttons without interrupts (uses polling)"""
        try:
            for color, config in PIN_CONFIG.items():
                if isinstance(config, dict) and 'button' in config:
                    try:
                        self.buttons[color] = Pin(config['button'], Pin.IN, Pin.PULL_UP)
                        self.last_press[color] = 0
                        self.last_state[color] = 1  # 1 = released
                        print(f"{color} button configured on pin {config['button']}")
                    except Exception as e:
                        print(f"Could not configure {color} button: {e}")
        except Exception as e:
            print(f"Error setting up buttons: {str(e)}")

    def check_buttons(self):
        """
        Checks all buttons (polling).
        Returns the color of the pressed button or None.
        """
        current_time = time.ticks_ms()
        
        for color, button in self.buttons.items():
            current_state = button.value()
            last_state = self.last_state.get(color, 1)
            
            # Detect falling edge (button just pressed)
            if current_state == 0 and last_state == 1:
                # Check debounce
                last_time = self.last_press.get(color, 0)
                if time.ticks_diff(current_time, last_time) > (DEBOUNCE_TIME * 1000):
                    self.last_press[color] = current_time
                    self.last_state[color] = current_state
                    print(f"Button press detected: {color}")
                    
                    # Execute callback if exists
                    if color in self.callbacks:
                        self.callbacks[color]()
                    
                    return color
            
            self.last_state[color] = current_state
        
        return None

    def is_pressed(self, color):
        """Checks if a specific button is pressed"""
        if color in self.buttons:
            return self.buttons[color].value() == 0
        return False

    def register_callback(self, color, callback):
        self.callbacks[color] = callback

    def cleanup(self):
        """Cleanup - no interrupts to disable"""
        pass
