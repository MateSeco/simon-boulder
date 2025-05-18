from hardware.buttons import ButtonManager
from hardware.leds import LEDManager
from config import COLORS, PIN_CONFIG
from tones import play_color, play_success, play_fail, cleanup
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
        self.hardware_status = {
            'leds': {},
            'buttons': {},
            'buzzer': False
        }
        
    def setup(self):
        print("\n=== Simon Says - Modo Hardware ===")
        print("Iniciando con hardware parcial...")
        
        # Verificar hardware disponible
        self._check_available_hardware()
        
        # Registrar callbacks solo para botones disponibles
        for color in COLORS + ['RESET']:
            if color in self.buttons.buttons:
                self.buttons.register_callback(color, lambda c=color: self._handle_button(c))
                
        # Verificar estado inicial de componentes
        self._verify_components()
    
    def _verify_components(self):
        """Verifica el estado de los componentes y actualiza hardware_status"""
        # Verificar LEDs
        for color in COLORS:
            try:
                if color in self.leds.leds:
                    self.leds.turn_on(color)
                    time.sleep(0.1)
                    self.leds.turn_off(color)
                    self.hardware_status['leds'][color] = True
                else:
                    self.hardware_status['leds'][color] = False
            except Exception as e:
                print(f"Error verificando LED {color}: {e}")
                self.hardware_status['leds'][color] = False
        
        # Verificar botones
        for color in COLORS + ['RESET']:
            self.hardware_status['buttons'][color] = color in self.buttons.buttons
        
        # Verificar buzzer
        try:
            if 'BUZZER' in PIN_CONFIG:
                play_color('RED')  # Prueba rápida del buzzer
                cleanup()
                self.hardware_status['buzzer'] = True
            else:
                self.hardware_status['buzzer'] = False
        except Exception as e:
            print(f"Error verificando buzzer: {e}")
            self.hardware_status['buzzer'] = False
    
    def _check_available_hardware(self):
        # Contar componentes disponibles
        leds_count = len(self.leds.leds)
        buttons_count = len(self.buttons.buttons)
        
        print(f"\nHardware detectado:")
        print(f"- LEDs: {leds_count}/4")
        print(f"- Botones: {buttons_count}/4")
        print(f"- Botón RESET: {'RESET' in self.buttons.buttons}")
        print(f"- Buzzer: {'BUZZER' in PIN_CONFIG}")
        
        if leds_count == 0 and buttons_count == 0:
            print("\n⚠️  ADVERTENCIA: No se detectó hardware. El juego funcionará en modo simulación.")
        else:
            print("\n✓ El juego funcionará con el hardware disponible.")
            print("  Los componentes faltantes serán simulados.")
            
        # Verificar estado inicial
        self._verify_components()
    
    def _handle_button(self, color):
        current_time = time.ticks_ms()
        if time.ticks_diff(current_time, self.last_button_time) > 200:  # Debounce de 200ms
            if color == 'RESET':
                self.reset_pressed = True
                print("¡RESET presionado!")
                cleanup()  # Limpiar el buzzer al presionar reset
            else:
                self.current_color = color
            self.last_button_time = current_time
            print(f"Botón presionado: {color}")
    
    def read_input(self, timeout=30.0):
        # Verificar estado del hardware antes de leer
        if not any(self.hardware_status['buttons'].values()):
            print("\nNo hay botones físicos disponibles. Usar entrada por teclado.")
            while True:
                try:
                    color = input("Ingrese color (RED/GREEN/BLUE/YELLOW/RESET): ").strip().upper()
                    if color in COLORS or color == 'RESET':
                        return color
                except:
                    pass
                print("Color inválido")
        
        # Esperar entrada de hardware con timeout
        self.current_color = None
        self.reset_pressed = False
        start_time = time.ticks_ms()
        
        while True:
            if self.reset_pressed:
                cleanup()  # Asegurar que el buzzer se limpia
                return 'RESET'
            
            if self.current_color:
                result = self.current_color
                self.current_color = None
                return result
            
            current_time = time.ticks_ms()
            if time.ticks_diff(current_time, start_time) > (timeout * 1000):
                print("\nTimeout: No se recibió entrada en 30 segundos")
                print("El juego se reiniciará...")
                cleanup()  # Limpiar el buzzer en caso de timeout
                return 'RESET'  # En lugar de None, retornamos RESET para reiniciar el juego
                
            # Verificar estado del hardware periódicamente
            if time.ticks_diff(current_time, start_time) % 5000 == 0:  # Cada 5 segundos
                self._verify_components()
                
            time.sleep(0.1)

    def display_sequence(self, color):
        print(f"DEBUG: Mostrando color {color}")
        try:
            # Verificar si el LED está disponible
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_on(color)
            
            # Reproducir sonido si el buzzer está disponible
            if self.hardware_status['buzzer']:
                play_color(color)
                
            time.sleep(0.5)  # Mantener LED encendido
        except Exception as e:
            print(f"Error mostrando secuencia: {e}")
            raise HardwareError(f"Error en hardware al mostrar {color}")
        finally:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_off(color)
            cleanup()  # Asegurar que el buzzer se limpia
        time.sleep(0.2)  # Pausa entre colores

    def show_success(self):
        print("¡Éxito!")
        try:
            if self.hardware_status['buzzer']:
                play_success()
        finally:
            cleanup()

    def show_failure(self):
        print("¡Game Over!")
        try:
            if self.hardware_status['buzzer']:
                play_fail()
        finally:
            cleanup()

    def cleanup(self):
        try:
            self.buttons.cleanup()
            self.leds.cleanup()
            cleanup()  # Limpiar el buzzer
        except Exception as e:
            print(f"Error durante la limpieza: {e}")

    def show_color(self, color):
        print(f"DEBUG: Mostrando color {color}")
        try:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_on(color)
            if self.hardware_status['buzzer']:
                play_color(color)
            time.sleep(0.5)
        except Exception as e:
            print(f"Error mostrando color {color}: {e}")
        finally:
            if self.hardware_status['leds'].get(color, False):
                self.leds.turn_off(color)
            cleanup()  # Asegurar que el buzzer se limpia

def play_tone(self, frequency):
    print(f"DEBUG: Reproduciendo tono {frequency}Hz")
    # código existente...