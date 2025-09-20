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
        self.last_button_time = 0
        self.reset_pressed = False
        self.led_turn_off_time = {}  # Track when to turn off LEDs
        self.hardware_status = {
            'leds': {},
            'buttons': {},
            'buzzer': False
        }
        
    def setup(self):
        print("\n=== Simon Says - Hardware Mode ===")
        print("Starting with partial hardware...")
        
        # Check available hardware
        self._check_available_hardware()
        
        # Register callbacks only for available buttons
        for color in COLORS + ['RESET']:
            if color in self.buttons.buttons:
                self.buttons.register_callback(color, lambda c=color: self._handle_button(c))
                
        # Check initial component status
        self._verify_components()
    
    def _verify_components(self):
        """Verify component status and update hardware_status"""
        # Check LEDs (without turning them on)
        for color in COLORS:
            try:
                if color in self.leds.leds:
                    self.hardware_status['leds'][color] = True
                else:
                    self.hardware_status['leds'][color] = False
            except Exception as e:
                print(f"Error checking {color} LED: {e}")
                self.hardware_status['leds'][color] = False
        
        # Check buttons
        for color in COLORS + ['RESET']:
            self.hardware_status['buttons'][color] = color in self.buttons.buttons
        
        # Check buzzer
        try:
            if 'BUZZER' in PIN_CONFIG:
                play_color('RED')  # Quick buzzer test
                cleanup()
                self.hardware_status['buzzer'] = True
            else:
                self.hardware_status['buzzer'] = False
        except Exception as e:
            print(f"Error checking buzzer: {e}")
            self.hardware_status['buzzer'] = False
    
    def _check_available_hardware(self):
        # Count available components
        leds_count = len(self.leds.leds)
        buttons_count = len(self.buttons.buttons)
        
        print(f"\nDetected hardware:")
        print(f"- LEDs: {leds_count}/4")
        print(f"- Buttons: {buttons_count}/4")
        print(f"- RESET Button: {'RESET' in self.buttons.buttons}")
        print(f"- Buzzer: {'BUZZER' in PIN_CONFIG}")
        
        if leds_count == 0 and buttons_count == 0:
            print("\n⚠️  WARNING: No hardware detected. Game will run in simulation mode.")
        else:
            print("\n✓ Game will run with available hardware.")
            print("  Missing components will be simulated.")
            
        # Check initial status
        self._verify_components()
    
    def _handle_button(self, color):
        if color == 'RESET':
            self.reset_pressed = True
            print("RESET pressed!")
            cleanup()  # Clean up buzzer when reset is pressed
        else:
            self.current_color = color
            print(f"Button pressed: {color}")
    
    def read_input(self, timeout=30.0):
        # Check hardware status before reading
        if not any(self.hardware_status['buttons'].values()):
            print("\nNo physical buttons available. Using keyboard input.")
            while True:
                try:
                    color = input("Enter color (RED/GREEN/BLUE/YELLOW/RESET): ").strip().upper()
                    if color in COLORS or color == 'RESET':
                        return color
                except:
                    pass
                print("Invalid color")
        
        # Wait for hardware input with timeout
        self.current_color = None
        self.reset_pressed = False
        start_time = time.ticks_ms()
        
        while True:
            if self.reset_pressed:
                cleanup()  # Ensure buzzer is cleaned up
                return 'RESET'
            
            if self.current_color:
                result = self.current_color
                # Provide immediate feedback (LED + sound)
                self.show_color(result)
                # Schedule LED to turn off after 200ms
                if self.hardware_status['leds'].get(result, False):
                    self.led_turn_off_time[result] = time.ticks_ms() + 200
                self.current_color = None
                return result
            
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, start_time) > (timeout * 1000):
                print("\nTimeout: No input received in 30 seconds")
                print("Game will restart...")
                cleanup()  # Clean up buzzer on timeout
                return 'RESET'  # Return RESET instead of None to restart the game
            
            # Check if any LEDs need to be turned off
            for color, turn_off_time in list(self.led_turn_off_time.items()):
                if time.ticks_diff(current_time, turn_off_time) >= 0:
                    if self.hardware_status['leds'].get(color, False):
                        self.leds.turn_off(color)
                    del self.led_turn_off_time[color]
                
            time.sleep(0.1)

    def show_color(self, color):
        print(f"DEBUG: Showing color {color}")
        try:
            # Check if LED is available
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_on(color)
            
            # Play sound if buzzer is available
            if self.hardware_status['buzzer']:
                play_color(color)
                
            time.sleep(0.5)  # Keep LED on
        except Exception as e:
            print(f"Error showing color: {e}")
            raise HardwareError(f"Hardware error showing {color}")
        finally:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_off(color)
            cleanup()  # Ensure buzzer is cleaned up
        time.sleep(0.2)  # Pause between colors

    def show_intro(self):
        print("Game starting...")
        try:
            if self.hardware_status['buzzer']:
                play_intro()
        finally:
            cleanup()

    def show_success(self):
        print("Success!")
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
            cleanup()  # Clean up buzzer
        except Exception as e:
            print(f"Error during cleanup: {e}")

def play_tone(self, frequency):
    print(f"DEBUG: Playing tone {frequency}Hz")
    # existing code...