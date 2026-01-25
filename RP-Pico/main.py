"""
Simon Says - Con interrupciones y manejo robusto de eventos
Usa configuración de config.py
"""
from machine import Pin, PWM
from urandom import getrandbits
import time

# Importar configuración
from config import (
    PIN_CONFIG,
    COLORS,
    DEBOUNCE_TIME,
    SEQUENCE_DELAY,
    SOUND_FREQUENCIES,
    POWER_SAVE_TIMEOUT
)

# =============================================================================
# CONFIGURACIÓN DERIVADA
# =============================================================================
# Extraer pines de PIN_CONFIG
LED_PINS = {color: PIN_CONFIG[color]['led'] for color in COLORS}
BUTTON_PINS = {color: PIN_CONFIG[color]['button'] for color in COLORS}
BUTTON_PINS['RESET'] = PIN_CONFIG['RESET']['button']
BUZZER_PIN = PIN_CONFIG['BUZZER']

# Tiempos (convertir a milisegundos donde sea necesario)
DEBOUNCE_MS = int(DEBOUNCE_TIME * 1000)
SEQUENCE_DELAY_MS = int(SEQUENCE_DELAY * 1000)
INPUT_TIMEOUT_MS = int(POWER_SAVE_TIMEOUT * 1000)  # Usar power save como timeout
SHOW_COLOR_MS = 400
PAUSE_BETWEEN_MS = 100

# =============================================================================
# ESTADOS DEL JUEGO
# =============================================================================
STATE_IDLE = 0
STATE_SHOWING = 1      # Mostrando secuencia
STATE_WAITING = 2      # Esperando input del jugador
STATE_GAMEOVER = 3

# =============================================================================
# CLASE PRINCIPAL
# =============================================================================
class SimonGame:
    def __init__(self):
        # Estado del juego
        self.state = STATE_IDLE
        self.sequence = []
        self.current_index = 0
        self.running = False
        
        # Cola de eventos (pulsaciones pendientes)
        self.event_queue = []
        self.last_press_time = {}
        
        # Configurar LEDs
        self.leds = {}
        for color, pin in LED_PINS.items():
            self.leds[color] = Pin(pin, Pin.OUT)
            self.leds[color].value(0)
        
        # Configurar buzzer
        self.buzzer = PWM(Pin(BUZZER_PIN))
        self.buzzer.duty_u16(0)
        
        # Configurar botones con interrupciones
        self.buttons = {}
        for color, pin in BUTTON_PINS.items():
            self.buttons[color] = Pin(pin, Pin.IN, Pin.PULL_UP)
            self.last_press_time[color] = 0
            # Configurar interrupción en flanco de bajada
            self.buttons[color].irq(
                trigger=Pin.IRQ_FALLING,
                handler=self._make_handler(color)
            )
        
        print("Simon Says inicializado!")
    
    def _make_handler(self, color):
        """Crea un handler de interrupción para cada color"""
        def handler(pin):
            self._button_pressed(color)
        return handler
    
    def _button_pressed(self, color):
        """Callback de interrupción - se ejecuta cuando se presiona un botón"""
        current_time = time.ticks_ms()
        last_time = self.last_press_time.get(color, 0)
        
        # Debounce: ignorar si es muy pronto desde la última pulsación
        if time.ticks_diff(current_time, last_time) < DEBOUNCE_MS:
            return
        
        self.last_press_time[color] = current_time
        
        # Solo registrar eventos si estamos esperando input
        if self.state == STATE_WAITING:
            self.event_queue.append(color)
            print(f"[IRQ] {color} presionado")
        elif color == 'RESET':
            # RESET siempre se procesa
            self.event_queue.append('RESET')
            print("[IRQ] RESET presionado")
    
    def clear_events(self):
        """Limpia la cola de eventos"""
        self.event_queue = []
    
    def get_event(self):
        """Obtiene el próximo evento de la cola (o None si está vacía)"""
        if self.event_queue:
            return self.event_queue.pop(0)
        return None
    
    # =========================================================================
    # FUNCIONES DE AUDIO/VIDEO
    # =========================================================================
    def play_tone(self, color, duration_ms=300):
        """Reproduce el tono del color usando SOUND_FREQUENCIES"""
        if color in SOUND_FREQUENCIES:
            freq = SOUND_FREQUENCIES[color]
            if isinstance(freq, int):
                self.buzzer.freq(freq)
                self.buzzer.duty_u16(32768)
                time.sleep_ms(duration_ms)
                self.buzzer.duty_u16(0)
    
    def beep(self, freq=440, duration_ms=100):
        """Beep genérico"""
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(32768)
        time.sleep_ms(duration_ms)
        self.buzzer.duty_u16(0)
    
    def play_melody(self, frequencies, duration_ms=150):
        """Reproduce una secuencia de frecuencias"""
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
        """Muestra un color con sonido (para la secuencia)"""
        self.led_on(color)
        self.play_tone(color, SHOW_COLOR_MS)
        self.led_off(color)
        time.sleep_ms(PAUSE_BETWEEN_MS)
    
    def feedback_color(self, color):
        """Feedback al presionar un botón (más corto)"""
        self.led_on(color)
        self.play_tone(color, 150)
        self.led_off(color)
    
    def flash_all(self, times=3, speed_ms=100):
        """Parpadea todos los LEDs"""
        for _ in range(times):
            for led in self.leds.values():
                led.value(1)
            time.sleep_ms(speed_ms)
            for led in self.leds.values():
                led.value(0)
            time.sleep_ms(speed_ms)
    
    # =========================================================================
    # MELODÍAS (usando SOUND_FREQUENCIES de config)
    # =========================================================================
    def play_success(self):
        """Melodía de ronda completada"""
        if 'SUCCESS' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['SUCCESS'], 100)
        else:
            self.beep(523, 100)
            self.beep(659, 100)
            self.beep(784, 200)
    
    def play_gameover(self):
        """Melodía de game over"""
        if 'FAIL' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['FAIL'], 200)
        else:
            self.beep(200, 300)
            self.beep(150, 500)
    
    def play_reset_sound(self):
        """Sonido de reset"""
        if 'RESET' in SOUND_FREQUENCIES:
            self.play_melody(SOUND_FREQUENCIES['RESET'], 100)
        else:
            self.beep(440, 100)
    
    def play_intro(self):
        """Animación y sonido de inicio"""
        print("Iniciando Simon Says...")
        for color in COLORS:
            self.show_color(color)
        time.sleep_ms(300)
    
    # =========================================================================
    # LÓGICA DEL JUEGO
    # =========================================================================
    def random_color(self):
        return COLORS[getrandbits(2)]
    
    def show_sequence(self):
        """Muestra la secuencia actual"""
        self.state = STATE_SHOWING
        self.clear_events()  # Ignorar pulsaciones durante la secuencia
        
        print(f"Mostrando secuencia: {self.sequence}")
        time.sleep_ms(SEQUENCE_DELAY_MS)
        
        for color in self.sequence:
            self.show_color(color)
        
        # Pequeña pausa antes de esperar input
        time.sleep_ms(300)
    
    def wait_for_input(self):
        """
        Espera el input del jugador para toda la secuencia.
        Retorna: 'success', 'fail', 'timeout', o 'reset'
        """
        self.state = STATE_WAITING
        self.clear_events()
        self.current_index = 0
        
        print(f"Tu turno! ({len(self.sequence)} colores)")
        
        while self.current_index < len(self.sequence):
            expected = self.sequence[self.current_index]
            start_time = time.ticks_ms()
            
            # Esperar evento con timeout
            while True:
                event = self.get_event()
                
                if event is not None:
                    # Procesar evento
                    if event == 'RESET':
                        print("Reset solicitado")
                        self.play_reset_sound()
                        return 'reset'
                    
                    # Dar feedback visual/sonoro
                    self.feedback_color(event)
                    
                    if event == expected:
                        print(f"  Correcto! ({self.current_index + 1}/{len(self.sequence)})")
                        self.current_index += 1
                        break
                    else:
                        print(f"  Error! Esperaba {expected}, presionaste {event}")
                        return 'fail'
                
                # Verificar timeout
                if time.ticks_diff(time.ticks_ms(), start_time) > INPUT_TIMEOUT_MS:
                    print("  Timeout!")
                    return 'timeout'
                
                # Verificar RESET aunque no estemos procesando eventos
                if 'RESET' in self.event_queue:
                    self.event_queue.remove('RESET')
                    self.play_reset_sound()
                    return 'reset'
                
                time.sleep_ms(10)  # Pequeña pausa para no saturar CPU
        
        return 'success'
    
    def play_round(self):
        """Juega una ronda completa"""
        # Agregar nuevo color
        self.sequence.append(self.random_color())
        print(f"\n=== Ronda {len(self.sequence)} ===")
        
        # Mostrar secuencia
        self.show_sequence()
        
        # Esperar input
        result = self.wait_for_input()
        
        if result == 'success':
            print("Ronda completada!")
            self.play_success()
        
        return result
    
    def game_over(self):
        """Maneja el fin del juego"""
        self.state = STATE_GAMEOVER
        print(f"\nGAME OVER - Llegaste a ronda {len(self.sequence)}")
        self.play_gameover()
        self.flash_all(times=5, speed_ms=100)
    
    def start(self):
        """Loop principal del juego"""
        self.running = True
        print("\n" + "=" * 40)
        print("SIMON SAYS")
        print("=" * 40)
        
        while self.running:
            # Nuevo juego
            self.sequence = []
            self.state = STATE_IDLE
            self.clear_events()
            
            # Intro
            self.play_intro()
            
            # Loop de rondas
            while self.running:
                result = self.play_round()
                
                if result == 'fail':
                    self.game_over()
                    time.sleep_ms(1500)
                    break
                
                if result == 'timeout':
                    print("Tiempo agotado!")
                    self.flash_all(times=2, speed_ms=150)
                    time.sleep_ms(500)
                    break
                
                if result == 'reset':
                    print("Reiniciando...")
                    self.flash_all(times=2, speed_ms=100)
                    time.sleep_ms(500)
                    break
                
                # Éxito - pausa antes de siguiente ronda
                time.sleep_ms(1000)
    
    def cleanup(self):
        """Limpieza al salir"""
        # Desactivar interrupciones
        for btn in self.buttons.values():
            btn.irq(handler=None)
        self.all_leds_off()
        self.buzzer_off()
        print("Cleanup completado")

# =============================================================================
# PUNTO DE ENTRADA
# =============================================================================
def main():
    game = SimonGame()
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nJuego terminado por usuario")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        game.cleanup()

if __name__ == "__main__":
    main()
