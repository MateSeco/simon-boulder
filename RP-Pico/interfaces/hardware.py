from hardware.buttons import ButtonManager
from hardware.leds import LEDManager
from config import COLORS, PIN_CONFIG
from tones import play_color, play_success, play_fail, play_intro, cleanup
import time

class HardwareError(Exception):
    pass

class HardwareInterface:
    def __init__(self):
        self.buttons = ButtonManager()
        self.leds = LEDManager()
        self.current_color = None
        self.reset_pressed = False
        self.hardware_status = {
            'leds': {},
            'buttons': {},
            'buzzer': False
        }
        
    def setup(self):
        print("\n=== Simon Says - Hardware Mode ===")
        self._check_available_hardware()
        self._verify_components()
    
    def _verify_components(self):
        """Verify component status"""
        # Check LEDs
        for color in COLORS:
            self.hardware_status['leds'][color] = color in self.leds.leds
        
        # Check buttons
        for color in COLORS + ['RESET']:
            self.hardware_status['buttons'][color] = color in self.buttons.buttons
        
        # Check buzzer
        try:
            if 'BUZZER' in PIN_CONFIG:
                self.hardware_status['buzzer'] = True
        except:
            self.hardware_status['buzzer'] = False
    
    def _check_available_hardware(self):
        leds_count = len(self.leds.leds)
        buttons_count = len(self.buttons.buttons)
        
        print(f"\nDetected hardware:")
        print(f"- LEDs: {leds_count}/4")
        print(f"- Buttons: {buttons_count}/5")
        print(f"- Buzzer: {'BUZZER' in PIN_CONFIG}")
        
        if leds_count == 0 and buttons_count == 0:
            print("\nWARNING: No hardware detected.")
        else:
            print("\nGame ready with available hardware.")

    def read_input(self, timeout=30.0):
        """Read input using polling (no interrupts)"""
        start_time = time.ticks_ms()
        
        while True:
            # Check buttons with polling
            pressed = self.buttons.check_buttons()
            
            if pressed == 'RESET':
                cleanup()
                return 'RESET'
            
            if pressed in COLORS:
                # Immediate feedback
                self.show_color(pressed)
                return pressed
            
            # Check timeout
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, start_time) > (timeout * 1000):
                print("\nTimeout: No input received")
                cleanup()
                return 'RESET'
            
            time.sleep(0.02)  # Small pause to not saturate CPU

    def show_color(self, color):
        """Shows a color (LED + sound)"""
        try:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_on(color)
            
            if self.hardware_status['buzzer']:
                play_color(color)
                
            time.sleep(0.4)
        except Exception as e:
            print(f"Error showing color: {e}")
        finally:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_off(color)
            cleanup()
        time.sleep(0.1)

    def show_sequence(self, sequence):
        """Shows a sequence of colors"""
        for color in sequence:
            self.show_color(color)

    def show_intro(self):
        print("Game starting...")
        try:
            if self.hardware_status['buzzer']:
                play_intro()
        finally:
            cleanup()

    def show_success(self):
        print("Success!")
        # Flash all LEDs
        for _ in range(2):
            for color in COLORS:
                if self.hardware_status['leds'].get(color, False):
                    self.leds.turn_on(color)
            time.sleep(0.2)
            for color in COLORS:
                if self.hardware_status['leds'].get(color, False):
                    self.leds.turn_off(color)
            time.sleep(0.2)
        
        try:
            if self.hardware_status['buzzer']:
                play_success()
        finally:
            cleanup()

    def show_failure(self):
        print("Game Over!")
        try:
            if self.hardware_status['buzzer']:
                play_fail()
        finally:
            cleanup()

    def cleanup(self):
        try:
            self.buttons.cleanup()
            self.leds.cleanup()
            cleanup()
        except Exception as e:
            print(f"Error during cleanup: {e}")
