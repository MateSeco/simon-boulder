from machine import Pin, PWM
from utime import sleep
import sys

def test_hardware():
    # Test LED onboard
    led = Pin("LED", Pin.OUT)
    print("Testing onboard LED...")
    for _ in range(3):
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)

    # Test input
    print("\nTesting input (type 'exit' to finish)...")
    while True:
        print('Enter command: ')
        command = sys.stdin.readline().rstrip('\n')
        if command.lower() == 'exit':
            break
        print('Received: ', command)

    # Test buzzer if connected
    try:
        buzzer = PWM(Pin(15))  # Ajusta el pin según tu configuración
        print("\nTesting buzzer...")
        buzzer.freq(440)  # Nota La (A4)
        buzzer.duty_u16(32768)  # 50% duty cycle
        sleep(1)
        buzzer.duty_u16(0)
    except:
        print("Buzzer test skipped")

if __name__ == "__main__":
    try:
        test_hardware()
        print("\nAll tests completed successfully!")
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"\nError during tests: {str(e)}")
    finally:
        print("Finished.")