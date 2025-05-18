from machine import Pin, PWM
from time import sleep
import random
from config import PIN_CONFIG
from hardware.leds import LEDManager
from hardware.buttons import ButtonManager
from hardware.buzzer import BuzzerManager

# Global variables for test state
current_test = 0
MAX_TESTS = 4

def save_test_state(state):
    with open('test_state.txt', 'w') as f:
        f.write(str(state))

def load_test_state():
    try:
        with open('test_state.txt', 'r') as f:
            return int(f.read())
    except:
        return 0

def test_all_leds(led_manager):
    """Test 1: Secuencia de prueba de LEDs"""
    print("\n=== Test 1: Probando LEDs ===")
    colors = list(PIN_CONFIG.keys())
    colors = [c for c in colors if 'led' in PIN_CONFIG[c]]
    
    # Test individual
    for color in colors:
        print(f"Probando LED {color}")
        led_manager.turn_on(color)
        sleep(1)
        led_manager.turn_off(color)
        sleep(0.5)
    
    # Test secuencia rápida
    print("Secuencia rápida...")
    for _ in range(5):
        for color in colors:
            led_manager.turn_on(color)
            sleep(0.2)
            led_manager.turn_off(color)
    
    # Test todos juntos
    print("Todos los LEDs juntos...")
    for _ in range(3):
        for color in colors:
            led_manager.turn_on(color)
        sleep(0.5)
        for color in colors:
            led_manager.turn_off(color)
        sleep(0.5)

def test_all_buttons(button_manager, led_manager):
    """Test 2: Prueba de botones con feedback LED"""
    print("\n=== Test 2: Probando Botones ===")
    print("Presiona cada botón para ver su LED correspondiente")
    print("Mantén cualquier botón por 3 segundos para terminar la prueba")
    
    end_test = False
    press_duration = 0
    
    while not end_test:
        for color, button in button_manager.buttons.items():
            if button.value() == 0:  # Botón presionado
                led_manager.turn_on(color)
                press_duration += 1
                if press_duration > 30:  # ~3 segundos
                    end_test = True
                    break
            else:
                led_manager.turn_off(color)
                press_duration = 0
        sleep(0.1)

def test_buzzer(buzzer_manager):
    """Test 3: Prueba de diferentes tonos del buzzer"""
    print("\n=== Test 3: Probando Buzzer ===")
    
    # Test de frecuencias
    frequencies = [262, 330, 392, 440, 523]  # Notas Do, Mi, Sol, La, Do
    for freq in frequencies:
        print(f"Reproduciendo {freq}Hz")
        buzzer_manager.play_tone(freq, 0.5)
        sleep(0.2)
    
    # Melodía simple
    print("Reproduciendo melodía de prueba...")
    melody = [(392, 0.3), (440, 0.3), (493, 0.3), (523, 0.5)]
    buzzer_manager.play_sequence(melody)

def test_interactive(led_manager, button_manager, buzzer_manager):
    """Test 4: Prueba interactiva de todos los componentes"""
    print("\n=== Test 4: Prueba Interactiva ===")
    print("Presiona los botones para activar LED y sonido")
    print("Mantén cualquier botón por 3 segundos para terminar")
    
    frequencies = {
        'RED': 262,    # Do
        'GREEN': 330,  # Mi
        'BLUE': 392,   # Sol
        'YELLOW': 440  # La
    }
    
    end_test = False
    press_duration = 0
    
    while not end_test:
        any_button_pressed = False
        for color, button in button_manager.buttons.items():
            if button.value() == 0:  # Botón presionado
                any_button_pressed = True
                led_manager.turn_on(color)
                if color in frequencies:
                    buzzer_manager.play_tone(frequencies[color], 0.1)
                press_duration += 1
                if press_duration > 30:  # ~3 segundos
                    end_test = True
                    break
            else:
                led_manager.turn_off(color)
        
        if not any_button_pressed:
            press_duration = 0
        sleep(0.1)

def main():
    # Inicializar componentes
    led_manager = LEDManager()
    button_manager = ButtonManager()
    buzzer_manager = BuzzerManager()
    
    # Cargar el estado del test
    current_test = load_test_state()
    current_test = (current_test + 1) % MAX_TESTS  # Avanzar al siguiente test
    save_test_state(current_test)
    
    # Indicador de inicio
    print(f"\nIniciando Test #{current_test + 1}")
    for _ in range(current_test + 1):  # Parpadea LED onboard según número de test
        Pin("LED", Pin.OUT).value(1)
        sleep(0.2)
        Pin("LED", Pin.OUT).value(0)
        sleep(0.2)
    
    try:
        if current_test == 0:
            test_all_leds(led_manager)
        elif current_test == 1:
            test_all_buttons(button_manager, led_manager)
        elif current_test == 2:
            test_buzzer(buzzer_manager)
        elif current_test == 3:
            test_interactive(led_manager, button_manager, buzzer_manager)
    
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
    finally:
        # Limpiar estado
        led_manager.cleanup()
        buzzer_manager.cleanup()
        print("\nPrueba completada. Presiona reset para la siguiente prueba.")

if __name__ == "__main__":
    main()