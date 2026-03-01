"""
Simon Says - With interrupts and robust event handling
Uses hardware modules for LED and buzzer control
"""
from machine import Pin
from urandom import getrandbits
import time

from config import (
    PIN_CONFIG,
    COLORS,
    DEBOUNCE_TIME,
    SEQUENCE_DELAY,
    POWER_SAVE_TIMEOUT,
    SHOW_COLOR_MS,
    PAUSE_BETWEEN_MS,
    FEEDBACK_MS
)
from hardware.leds import LEDManager
from hardware.buzzer import BuzzerManager

# =============================================================================
# DERIVED CONFIGURATION
# =============================================================================
BUTTON_PINS = {color: PIN_CONFIG[color]['button'] for color in COLORS}
BUTTON_PINS['RESET'] = PIN_CONFIG['RESET']['button']

DEBOUNCE_MS = int(DEBOUNCE_TIME * 1000)
SEQUENCE_DELAY_MS = int(SEQUENCE_DELAY * 1000)
INPUT_TIMEOUT_MS = int(POWER_SAVE_TIMEOUT * 1000)

# =============================================================================
# GAME STATES
# =============================================================================
STATE_IDLE = 0
STATE_SHOWING = 1
STATE_WAITING = 2

# =============================================================================
# MAIN CLASS
# =============================================================================
class SimonGame:
    def __init__(self):
        # Game state
        self.state = STATE_IDLE
        self.sequence = []
        self.current_index = 0
        self.running = False
        
        # Event queue
        self.event_queue = []
        self.last_press_time = {}
        
        # Hardware managers
        self.leds = LEDManager()
        self.buzzer = BuzzerManager()
        
        # Setup buttons with interrupts
        self.buttons = {}
        for color, pin in BUTTON_PINS.items():
            self.buttons[color] = Pin(pin, Pin.IN, Pin.PULL_UP)
            self.last_press_time[color] = 0
            self.buttons[color].irq(
                trigger=Pin.IRQ_FALLING,
                handler=self._make_handler(color)
            )
        
        print("Simon Says initialized!")
    
    def _make_handler(self, color):
        """Creates an interrupt handler for each color"""
        def handler(pin):
            self._button_pressed(color)
        return handler
    
    def _button_pressed(self, color):
        """Interrupt callback - runs when a button is pressed"""
        current_time = time.ticks_ms()
        last_time = self.last_press_time.get(color, 0)
        
        if time.ticks_diff(current_time, last_time) < DEBOUNCE_MS:
            return
        
        self.last_press_time[color] = current_time
        
        if self.state == STATE_WAITING:
            self.event_queue.append(color)
            print(f"[IRQ] {color} pressed")
        elif color == 'RESET':
            self.event_queue.append('RESET')
            print("[IRQ] RESET pressed")
    
    def clear_events(self):
        """Clears the event queue"""
        self.event_queue = []
    
    def get_event(self):
        """Gets the next event from the queue"""
        if self.event_queue:
            return self.event_queue.pop(0)
        return None
    
    # =========================================================================
    # DISPLAY FUNCTIONS
    # =========================================================================
    def show_color(self, color):
        """Shows a color with sound (for the sequence)"""
        self.leds.turn_on(color)
        self.buzzer.play_color(color, SHOW_COLOR_MS)
        self.leds.turn_off(color)
        time.sleep_ms(PAUSE_BETWEEN_MS)
    
    def feedback_color(self, color):
        """Feedback when pressing a button"""
        self.leds.turn_on(color)
        self.buzzer.play_color(color, FEEDBACK_MS)
        self.leds.turn_off(color)
    
    # =========================================================================
    # GAME LOGIC
    # =========================================================================
    def random_color(self):
        return COLORS[getrandbits(2)]
    
    def show_sequence(self):
        """Shows the current sequence"""
        self.state = STATE_SHOWING
        self.clear_events()
        
        print(f"Showing sequence: {self.sequence}")
        time.sleep_ms(SEQUENCE_DELAY_MS)
        
        for color in self.sequence:
            self.show_color(color)
        
        time.sleep_ms(300)
    
    def wait_for_input(self):
        """Waits for player input for the entire sequence"""
        self.state = STATE_WAITING
        self.clear_events()
        self.current_index = 0
        
        print(f"Your turn! ({len(self.sequence)} colors)")
        
        while self.current_index < len(self.sequence):
            expected = self.sequence[self.current_index]
            start_time = time.ticks_ms()
            
            while True:
                event = self.get_event()
                
                if event is not None:
                    if event == 'RESET':
                        print("Reset requested")
                        self.buzzer.play_reset()
                        return 'reset'
                    
                    self.feedback_color(event)
                    
                    if event == expected:
                        print(f"  Correct! ({self.current_index + 1}/{len(self.sequence)})")
                        self.current_index += 1
                        break
                    else:
                        print(f"  Wrong! Expected {expected}, got {event}")
                        return 'fail'
                
                if time.ticks_diff(time.ticks_ms(), start_time) > INPUT_TIMEOUT_MS:
                    print("  Timeout!")
                    return 'timeout'
                
                if 'RESET' in self.event_queue:
                    self.event_queue.remove('RESET')
                    self.buzzer.play_reset()
                    return 'reset'
                
                time.sleep_ms(10)
        
        return 'success'
    
    def play_round(self):
        """Plays a complete round"""
        self.sequence.append(self.random_color())
        print(f"\n=== Round {len(self.sequence)} ===")
        
        self.show_sequence()
        result = self.wait_for_input()
        
        if result == 'success':
            print("Round completed!")
            self.buzzer.play_success()
        
        return result
    
    def game_over(self):
        """Handles game over"""
        print(f"\nGAME OVER - You reached round {len(self.sequence)}")
        self.buzzer.play_fail()
        self.leds.flash_all(times=5, delay_ms=100)
    
    def play_intro(self):
        """Intro animation and sound"""
        print("Starting Simon Says...")
        for color in COLORS:
            self.show_color(color)
        time.sleep_ms(300)
    
    def start(self):
        """Main game loop"""
        self.running = True
        print("\n" + "=" * 40)
        print("SIMON SAYS")
        print("=" * 40)
        
        while self.running:
            self.sequence = []
            self.state = STATE_IDLE
            self.clear_events()
            
            self.play_intro()
            
            while self.running:
                result = self.play_round()
                
                if result == 'fail':
                    self.game_over()
                    time.sleep_ms(1500)
                    break
                
                if result == 'timeout':
                    print("Time's up!")
                    self.leds.flash_all(times=2, delay_ms=150)
                    time.sleep_ms(500)
                    break
                
                if result == 'reset':
                    print("Restarting...")
                    self.leds.flash_all(times=2, delay_ms=100)
                    time.sleep_ms(500)
                    break
                
                time.sleep_ms(1000)
    
    def cleanup(self):
        """Cleanup on exit"""
        for btn in self.buttons.values():
            btn.irq(handler=None)
        self.leds.turn_all_off()
        self.buzzer.cleanup()
        print("Cleanup completed")

# =============================================================================
# ENTRY POINT
# =============================================================================
def main():
    game = SimonGame()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        game.cleanup()

if __name__ == "__main__":
    main()
