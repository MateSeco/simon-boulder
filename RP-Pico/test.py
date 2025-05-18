from machine import Pin, PWM
from time import sleep
import random
from config import PIN_CONFIG
from hardware.leds import LEDManager
from hardware.buttons import ButtonManager
from hardware.buzzer import BuzzerManager
import select
import sys

# Global variables for test state
current_test = 0
MAX_TESTS = 4

def wait_for_user(message="Presiona ENTER para continuar..."):
    """Espera input del usuario para continuar"""
    print("\n" + message)
    input()

def get_game_colors():
    """Retorna solo los colores del juego (excluyendo RESET)"""
    return ['RED', 'GREEN', 'BLUE', 'YELLOW']

def test_single_led(led_manager):
    """Test 1: Prueba de LEDs uno por uno con tiempo para reconexión"""
    print("\n=== Test 1: Probando LEDs ===")
    print("Este test requiere reconectar el LED para cada color.")
    print("Asegúrate de tener a mano el diagrama de pines.")
    
    for color in get_game_colors():
        print(f"\n--- Prueba de LED {color} ---")
        print(f"1. Conecta el LED al pin correspondiente para {color}")
        print(f"   Pin para LED {color}: {PIN_CONFIG[color]['led']}")
        wait_for_user("Presiona ENTER cuando hayas conectado el LED...")
        
        print(f"\nProbando LED {color}:")
        for _ in range(3):  # Parpadear 3 veces
            print("LED ON")
            led_manager.turn_on(color)
            sleep(1)
            print("LED OFF")
            led_manager.turn_off(color)
            sleep(0.5)
        
        wait_for_user("¿El LED parpadeó correctamente? Presiona ENTER para continuar...")

def test_single_button(button_manager, led_manager):
    """Test 2: Prueba de botones uno por uno con tiempo para reconexión"""
    print("\n=== Test 2: Probando Botones ===")
    print("Este test requiere reconectar el botón para cada color.")
    print("También necesitarás reconectar el LED para ver el feedback visual.")
    
    for color in get_game_colors():
        print(f"\n--- Prueba de Botón {color} ---")
        print(f"1. Conecta el botón al pin correspondiente para {color}")
        print(f"   Pin para Botón {color}: {PIN_CONFIG[color]['button']}")
        print(f"2. Conecta el LED al pin correspondiente para {color}")
        print(f"   Pin para LED {color}: {PIN_CONFIG[color]['led']}")
        
        wait_for_user("Presiona ENTER cuando hayas conectado el botón y LED...")
        
        print(f"\nPrueba del botón {color}:")
        print("Presiona el botón 3 veces. El LED debería encenderse con cada presión.")
        
        count = 0
        last_state = 1
        timeout = 0
        while count < 3 and timeout < 100:  # 10 segundos máximo
            if color in button_manager.buttons:
                current_state = button_manager.buttons[color].value()
                if current_state == 0 and last_state == 1:  # Botón presionado
                    print(f"Botón {color} presionado!")
                    led_manager.turn_on(color)
                    sleep(0.2)
                    led_manager.turn_off(color)
                    count += 1
                last_state = current_state
            sleep(0.1)
            timeout += 1
        
        if count == 3:
            print("¡Prueba exitosa!")
        else:
            print("No se detectaron suficientes presiones del botón.")
        
        wait_for_user()

def test_buzzer(buzzer_manager):
    """Test 3: Prueba del buzzer con diferentes tonos"""
    print("\n=== Test 3: Probando Buzzer ===")
    print("Este test usa un solo buzzer para todas las pruebas.")
    print(f"Conecta el buzzer al pin {PIN_CONFIG['BUZZER']}")
    
    wait_for_user("Presiona ENTER cuando hayas conectado el buzzer...")
    
    # Notas musicales para probar
    notes = {
        'Do': 262,
        'Mi': 330,
        'Sol': 392,
        'Do_alto': 523
    }
    
    # Test de notas individuales
    print("\nProbando notas individuales...")
    for name, freq in notes.items():
        print(f"Reproduciendo {name} ({freq}Hz)")
        buzzer_manager.play_tone(freq, 500)
        wait_for_user("¿Escuchaste la nota? Presiona ENTER para la siguiente...")
    
    # Melodía de prueba
    print("\nAhora probaremos una melodía completa...")
    wait_for_user("Presiona ENTER para escuchar la melodía...")
    
    melody = [
        (notes['Do'], 300),
        (notes['Mi'], 300),
        (notes['Sol'], 300),
        (notes['Do_alto'], 500)
    ]
    buzzer_manager.play_sequence(melody)

def test_interactive_single(led_manager, button_manager, buzzer_manager):
    """Test 4: Prueba interactiva con un solo set de componentes"""
    print("\n=== Test 4: Prueba Interactiva ===")
    print("Esta prueba requiere mover los componentes para cada color.")
    print("Probaremos cada color con su LED, botón y sonido correspondiente.")
    
    frequencies = {
        'RED': 262,    # Do
        'GREEN': 330,  # Mi
        'BLUE': 392,   # Sol
        'YELLOW': 440  # La
    }
    
    for color in get_game_colors():
        print(f"\n--- Prueba Completa para {color} ---")
        print(f"1. Conecta el LED al pin {PIN_CONFIG[color]['led']}")
        print(f"2. Conecta el botón al pin {PIN_CONFIG[color]['button']}")
        print(f"3. Asegúrate que el buzzer esté en el pin {PIN_CONFIG['BUZZER']}")
        
        wait_for_user("Presiona ENTER cuando hayas conectado todo...")
        
        print(f"\nPrueba del conjunto {color}:")
        print("Prueba presionando el botón varias veces.")
        print("El LED debería encenderse y el buzzer sonar.")
        
        # Dar tiempo para probar (20 segundos)
        timeout = 200  # 20 segundos (200 * 0.1)
        last_state = 1
        count = 0
        
        while count < timeout:
            try:
                # Verificar el botón
                if button_manager.buttons[color].value() == 0 and last_state == 1:
                    print(f"¡{color} activado!")
                    led_manager.turn_on(color)
                    buzzer_manager.play_tone(frequencies[color], 200)
                    led_manager.turn_off(color)
                last_state = button_manager.buttons[color].value()
                    
            except Exception as e:
                print(f"Error en test interactivo: {str(e)}")
                break
            
            sleep(0.1)
            count += 1
        
        wait_for_user(f"\nPrueba de {color} completada. Presiona ENTER para continuar...")

def input_available():
    """Verifica si hay input disponible sin bloquear"""
    try:
        return False  # En MicroPython, simplemente retornamos False y usamos input() normal
    except:
        return False

def main():
    print("\n=== Programa de Pruebas de Hardware ===")
    print("Este programa está diseñado para probar el hardware")
    print("con un solo set de componentes (1 LED, 1 botón, 1 buzzer)")
    print("Te guiará para reconectar los componentes según sea necesario.")
    
    # Inicializar componentes
    led_manager = LEDManager()
    button_manager = ButtonManager()
    buzzer_manager = BuzzerManager()
    
    try:
        while True:
            print("\nTests disponibles:")
            print("1. Prueba de LEDs")
            print("2. Prueba de Botones")
            print("3. Prueba de Buzzer")
            print("4. Prueba Interactiva")
            print("5. Salir")
            
            try:
                option = int(input("\nSelecciona una prueba (1-5): "))
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
                    print("Opción no válida")
            except ValueError:
                print("Por favor, ingresa un número válido")
    
    except Exception as e:
        print(f"Error durante la prueba: {str(e)}")
    finally:
        # Limpiar estado
        led_manager.cleanup()
        buzzer_manager.cleanup()
        print("\nPrograma de pruebas finalizado.")

if __name__ == "__main__":
    main()