"""
Simon Says - With interrupts and robust event handling
Uses configuration from config.py
"""
from machine import Pin, PWM
from urandom import getrandbits
import time

# Import configuration
from config import (
    PIN_CONFIG,
    COLORS,
    DEBOUNCE_TIME,
    SEQUENCE_DELAY,
    SOUND_FREQUENCIES,
    POWER_SAVE_TIMEOUT
)

# =============================================================================
# DERIVED CONFIGURATION
# =============================================================================
# Extract pins from PIN_CONFIG
LED_PINS = {color: PIN_CONFIG[color]['led'] for color in COLORS}
BUTTON_PINS = {color: PIN_CONFIG[color]['button'] for color in COLORS}
BUTTON_PINS['RESET'] = PIN_CONFIG['RESET']['button']
BUZZER_PIN = PIN_CONFIG['BUZZER']

# Timing (convert to milliseconds where needed)
DEBOUNCE_MS = int(DEBOUNCE_TIME * 1000)
SEQUENCE_DELAY_MS = int(SEQUENCE_DELAY * 1000)
INPUT_TIMEOUT_MS = int(POWER_SAVE_TIMEOUT * 1000)
SHOW_COLOR_MS = 400
PAUSE_BETWEEN_MS = 100

# =============================================================================
# GAME STATES
# =============================================================================
STATE_IDLE = 0
STATE_SHOWING = 1
STATE_WAITING = 2
STATE_GAMEOVER = 3

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
        
        # Event queue (pending button presses)
        self.event_queue = []
        self.last_press_time = {}
        
        # Setup LEDs
        self.leds = {}
        for color, pin in LED_PINS.items():
            self.leds[color] = Pin(pin, Pin.OUT)
            self.leds[color].value(0)
        
        # Setup buzzer
        self.buzzer = PWM(Pin(BUZZER_PIN))
        self.buzzer.duty_u16(0)
        
        # Setup buttons with interrupts
        self.buttons = {}
        for color, pin in BUTTON_PINS.items():
            self.buttons[color] = Pin(pin, Pin.IN, Pin.PULL_UP)
            self.last_press_time[color] = 0
            # Setup interrupt on falling edge
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
        
        # Debounce: ignore if too soon since last press
        if time.ticks_diff(current_time, last_time) < DEBOUNCE_MS:
            return
        
        self.last_press_time[color] = current_time
        
        # Only register events if waiting for input
        if self.state == STATE_WAITING:
            self.event_queue.append(color)
            print(f"[IRQ] {color} pressed")
        elif color == 'RESET':
            # RESET is always processed
            self.event_queue.append('RESET')
            print("[IRQ] RESET pressed")
    
    def clear_events(self):
        """Clears the event queue"""
        self.event_queue = []
    
    def get_event(self):
        """Gets the next event from the queue (or None if empty)"""
        if self.event_queue:
            return self.event_queue.pop(0)
        return None
    
    # =========================================================================
    # AUDIO/VIDEO FUNCTIONS
    # =========================================================================
    def play_tone(self, color, duration_ms=300):
        """Plays the tone for a color using SOUND_FREQUENCIES"""
        if color in SOUND_FREQUENCIES:
            freq = SOUND_FREQUENCIES[color]
            if isinstance(freq, int):
                self.buzzer.freq(freq)
                self.buzzer.duty_u16(32768)
                time.sleep_ms(duration_ms)
                self.buzzer.duty_u16(0)
    
    def beep(self, freq=440, duration_ms=100):
        """Generic beep"""
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(32768)
        time.sleep_ms(duration_ms)
        self.buzzer.duty_u16(0)
    
    def play_melody(self, frequencies, duration_ms=150):
        """Plays a sequence of frequencies"""
        for freq in frequencies:
            self.beep(freq, duration_ms)
            time.sleep_ms(50)
    
    def led_on(self, color):
        if color in self.leds:
            self.leds[color].value(1)
    
    def led_off(self, color):
        if color in self.leds:
            self.leds[color].value(0)
    
    def all_leds_off(self):
        for led in self.leds.values():
            led.value(0)
    
    def buzzer_off(self):
        self.buzzer.duty_u16(0)
    
    def show_color(self, color):
        """Shows a color with sound (for the sequence)"""
        self.led_on(color)
        self.play_tone(color, SHOW_COLOR_MS)
        self.led_off(color)
        time.sleep_ms(PAUSE_BETWEEN_MS)
    
    def feedback_color(self, color):
        """Feedback when pressing a button (shorter)"""
        self.led_on(color)
        self.play_tone(color, 150)
        self.led_off(color)
    
    def flash_all(self, times=3, speed_ms=100):
        """Flashes all LEDs"""
        for _ in range(times):
            for led in self.leds.values():
                led.value(1)
            time.sleep_ms(speed_ms)
            for led in self.leds.values():
                led.value(0)
            time.sleep_ms(speed_ms)
    
    # =========================================================================
    # MELODIES (using SOUND_FREQUENCIES from config)
    # =========================================================================
    def play_success(self):
        """Round completed melody"""
        if 'SUCCESS' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['SUCCESS'], 100)
        else:
            self.beep(523, 100)
            self.beep(659, 100)
            self.beep(784, 200)
    
    def play_gameover(self):
        """Game over melody"""
        if 'FAIL' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['FAIL'], 200)
        else:
            self.beep(200, 300)
            self.beep(150, 500)
    
    def play_reset_sound(self):
        """Reset sound"""
        if 'RESET' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['RESET'], 100)
        else:
            self.beep(440, 100)
    
    def play_intro(self):
        """Intro animation and sound"""
        print("Starting Simon Says...")
        for color in COLORS:
            self.show_color(color)
        time.sleep_ms(300)
    
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
        """
        Waits for player input for the entire sequence.
        Returns: 'success', 'fail', 'timeout', or 'reset'
        """
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
                        self.play_reset_sound()
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
                    self.play_reset_sound()
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
            self.play_success()
        
        return result
    
    def game_over(self):
        """Handles game over"""
        self.state = STATE_GAMEOVER
        print(f"\nGAME OVER - You reached round {len(self.sequence)}")
        self.play_gameover()
        self.flash_all(times=5, speed_ms=100)
    
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
                    self.flash_all(times=2, speed_ms=150)
                    time.sleep_ms(500)
                    break
                
                if result == 'reset':
                    print("Restarting...")
                    self.flash_all(times=2, speed_ms=100)
                    time.sleep_ms(500)
                    break
                
                time.sleep_ms(1000)
    
    def cleanup(self):
        """Cleanup on exit"""
        for btn in self.buttons.values():
            btn.irq(handler=None)
        self.all_leds_off()
        self.buzzer_off()
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
