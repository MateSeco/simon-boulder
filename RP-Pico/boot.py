# boot.py - Starts Simon Says automatically
import time

print("Simon Says - Starting in 2 seconds...")
print("(Press BOOTSEL + disconnect to cancel)")
time.sleep(2)

try:
    import main
    main.main()
except Exception as e:
    print(f"Error: {e}")
    # Keep LEDs off in case of error
    from machine import Pin
    for p in [2, 3, 4, 5]:
        Pin(p, Pin.OUT).value(0)
