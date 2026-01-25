# boot.py - Inicia Simon Says automáticamente
import time

print("Simon Says - Iniciando en 2 segundos...")
print("(Presiona BOOTSEL + desconecta para cancelar)")
time.sleep(2)

try:
    import main
    main.main()
except Exception as e:
    print(f"Error: {e}")
    # Mantener LEDs apagados en caso de error
    from machine import Pin
    for p in [2, 3, 4, 5]:
        Pin(p, Pin.OUT).value(0)
