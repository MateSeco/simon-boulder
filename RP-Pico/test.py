from machine import Pin
from time import sleep
from config import PIN_CONFIG
from hardware.leds import LEDManager
from hardware.buttons import ButtonManager
from hardware.buzzer import BuzzerManager
import sys

# Global variables for test state
current_test = 0
MAX_TESTS = 4

def wait_for_user(message="Press ENTER to continue..."):
    """Wait for user input to continue"""
    print("\n" + message)
    input()

def get_game_colors():
    """Returns only game colors (excluding RESET)"""
    return ['RED', 'GREEN', 'BLUE', 'YELLOW']

def test_single_led(led_manager):
    """Test 1: Testing LEDs one by one with time for reconnection"""
    print("\n=== Test 1: Testing LEDs ===")
    print("This test requires reconnecting the LED for each color.")
    print("Make sure you have the pin diagram handy.")
    
    for color in get_game_colors():
        print(f"\n--- Testing {color} LED ---")
        print(f"1. Connect the LED to the corresponding pin for {color}")
        print(f"   Pin for {color} LED: {PIN_CONFIG[color]['led']}")
        wait_for_user("Press ENTER when you have connected the LED...")
        
        print(f"\nTesting {color} LED:")
        for _ in range(3):  # Blink 3 times
            print("LED ON")
            led_manager.turn_on(color)
            sleep(1)
            print("LED OFF")
            led_manager.turn_off(color)
            sleep(0.5)
        
        wait_for_user("Did the LED blink correctly? Press ENTER to continue...")

def test_single_button(button_manager, led_manager):
    """Test 2: Testing buttons one by one with time for reconnection"""
    print("\n=== Test 2: Testing Buttons ===")
    print("This test requires reconnecting the button for each color.")
    print("You will also need to reconnect the LED for visual feedback.")
    
    for color in get_game_colors():
        print(f"\n--- Testing {color} Button ---")
        print(f"1. Connect the button to the corresponding pin for {color}")
        print(f"   Pin for {color} Button: {PIN_CONFIG[color]['button']}")
        print(f"2. Connect the LED to the corresponding pin for {color}")
        print(f"   Pin for {color} LED: {PIN_CONFIG[color]['led']}")
        
        wait_for_user("Press ENTER when you have connected the button and LED...")
        
        print(f"\nTesting {color} button:")
        print("Press the button 3 times. The LED should light up with each press.")
        
        count = 0
        last_state = 1
        timeout = 0
        while count < 3 and timeout < 100:  # 10 seconds maximum
            if color in button_manager.buttons:
                current_state = button_manager.buttons[color].value()
                if current_state == 0 and last_state == 1:  # Button pressed
                    print(f"{color} button pressed!")
                    led_manager.turn_on(color)
                    sleep(0.2)
                    led_manager.turn_off(color)
                    count += 1
                last_state = current_state
            sleep(0.1)
            timeout += 1
        
        if count == 3:
            print("Test successful!")
        else:
            print("Not enough button presses detected.")
        
        wait_for_user()

def test_buzzer(buzzer_manager):
    """Test 3: Testing buzzer with different tones"""
    print("\n=== Test 3: Testing Buzzer ===")
    print("This test uses a single buzzer for all tests.")
    print(f"Connect the buzzer to pin {PIN_CONFIG['BUZZER']}")
    
    wait_for_user("Press ENTER when you have connected the buzzer...")
    
    # Musical notes to test
    notes = {
        'C4': 262,
        'E4': 330,
        'G4': 392,
        'C5': 523
    }
    
    # Test individual notes
    print("\nTesting individual notes...")
    for name, freq in notes.items():
        print(f"Playing {name} ({freq}Hz)")
        buzzer_manager.play_tone(freq, 500)
        wait_for_user("Did you hear the note? Press ENTER for the next one...")
    
    # Test melody
    print("\nNow we'll test a complete melody...")
    wait_for_user("Press ENTER to hear the melody...")
    
    melody = [
        (notes['C4'], 300),
        (notes['E4'], 300),
        (notes['G4'], 300),
        (notes['C5'], 500)
    ]
    buzzer_manager.play_sequence(melody)

def test_interactive_single(led_manager, button_manager, buzzer_manager):
    """Test 4: Interactive test with a single set of components"""
    print("\n=== Test 4: Interactive Test ===")
    print("This test requires moving components for each color.")
    print("We will test each color with its LED, button, and corresponding sound.")
    
    frequencies = {
        'RED': 262,    # C4
        'GREEN': 330,  # E4
        'BLUE': 392,   # G4
        'YELLOW': 440  # A4
    }
    
    for color in get_game_colors():
        print(f"\n--- Complete Test for {color} ---")
        print(f"1. Connect the LED to pin {PIN_CONFIG[color]['led']}")
        print(f"2. Connect the button to pin {PIN_CONFIG[color]['button']}")
        print(f"3. Make sure the buzzer is connected to pin {PIN_CONFIG['BUZZER']}")
        
        wait_for_user("Press ENTER when you have connected everything...")
        
        print(f"\nTesting {color} set:")
        print("Test by pressing the button several times.")
        print("The LED should light up and the buzzer should sound.")
        
        # Give time to test (10 seconds)
        timeout = 100  # 10 seconds (100 * 0.1)
        last_state = 1
        count = 0
        
        while count < timeout:
            try:
                # Check button
                if button_manager.buttons[color].value() == 0 and last_state == 1:
                    print(f"{color} activated!")
                    led_manager.turn_on(color)
                    buzzer_manager.play_tone(frequencies[color], 200)
                    led_manager.turn_off(color)
                last_state = button_manager.buttons[color].value()
                    
            except Exception as e:
                print(f"Error in interactive test: {str(e)}")
                break
            
            sleep(0.1)
            count += 1
        
        wait_for_user(f"\n{color} test completed. Press ENTER to continue...")

def input_available():
    """Verifies if input is available without blocking"""
    try:
        return False  # In MicroPython, we simply return False and use normal input()
    except:
        return False

def main():
    print("\n=== Hardware Test Program ===")
    print("This program is designed to test the hardware")
    print("with a single set of components (1 LED, 1 button, 1 buzzer)")
    print("It will guide you to reconnect components as needed.")
    
    # Initialize components
    led_manager = LEDManager()
    button_manager = ButtonManager()
    buzzer_manager = BuzzerManager()
    
    try:
        while True:
            print("\nAvailable tests:")
            print("1. LED Test")
            print("2. Button Test")
            print("3. Buzzer Test")
            print("4. Interactive Test")
            print("5. Exit")
            
            try:
                option = int(input("\nSelect a test (1-5): "))
                if option == 1:
                    test_single_led(led_manager)
                elif option == 2:
                    test_single_button(button_manager, led_manager)
                elif option == 3:
                    test_buzzer(buzzer_manager)
                elif option == 4:
                    test_interactive_single(led_manager, button_manager, buzzer_manager)
                elif option == 5:
                    break
                else:
                    print("Invalid option")
            except ValueError:
                print("Please enter a valid number")
    
    except Exception as e:
        print(f"Error during test: {str(e)}")
    finally:
        # Clean up state
        led_manager.cleanup()
        buzzer_manager.cleanup()
        print("\nTest program finished.")

if __name__ == "__main__":
    main()