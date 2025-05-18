# Simon Says for Raspberry Pi Pico

An implementation of the classic Simon Says game for Raspberry Pi Pico. The game challenges players to repeat increasingly longer color sequences, combining LEDs, buttons, and sound effects for a complete interactive experience.

## Main Features

- Random and progressive color sequences
- Hardware interface with LEDs, buttons, and sound feedback
- CLI mode on computer for development and testing
- Unique sounds for each color
- Special melodies for game events
- Button debouncing
- Power-saving mode
- Modular and easy-to-modify design

## Required Components

### Microcontroller

- **Raspberry Pi Pico**
  - Microcontroller: RP2040
  - Operating voltage: 3.3V
  - Maximum current per GPIO pin: 12mA
  - Recommended input voltage (VSYS): 5V via USB

### LEDs

- **4x General purpose LEDs**
  - Forward current (If): 20mA maximum
  - Colors: Red, Green, Blue, Yellow
  - Mounting type: Through-hole

### Resistors

- **4x LED Resistors**
  - Value: 220Ω
  - Tolerance: ±5%
  - Power: 1/4W

### Buttons

- **5x Tactile Push Buttons**
  - Type: Momentary (normally open)
  - Configuration: 4 pins
  - Dimensions: 6mm x 6mm x 5mm

### Buzzer

- **1x Active Buzzer Module (KY-012)**
  - Operating voltage: 3.5V - 5.5V (3.3V compatible)
  - Operating current: <25mA
  - Frequency: 2300 ± 500 Hz
  - Pins: VCC, GND, S (signal)

### Breadboard and Cables

- **1x Breadboard**
  - Minimum 400 points
  - With power rails
- **20x Male-to-male Dupont cables**
  - Length: 10-20cm

### USB Cable

- **1x Micro USB Cable**
  - For programming and power

## Breadboard Assembly

### LED Connections

1. Connect the LEDs observing polarity:
   - Anode (longer leg) → 220Ω Resistor → GPIO Pin
   - Cathode (shorter leg) → GND
   ```
   Red LED    → GP2
   Green LED  → GP3
   Blue LED   → GP4
   Yellow LED → GP5
   ```

### Button Connections

1. Connect one pin of each button to the corresponding GPIO and the other to GND:
   ```
   Red Button    → GP6
   Green Button  → GP7
   Blue Button   → GP8
   Yellow Button → GP9
   Reset Button  → GP10
   ```

### Buzzer Module Connection (KY-012)

1. Connect the three module pins:
   ```
   VCC → 3.3V from Pico
   GND → GND
   S (signal) → GP15
   ```

### Verification

1. Check for short circuits
2. Verify polarity of all LEDs
3. Confirm buttons make good contact
4. Ensure all GND and 3.3V connections are correct

## Initial Setup

### Install MicroPython on the Pico

1. Hold down the BOOTSEL button on the Pico
2. Connect the Pico to your computer while holding BOOTSEL
3. Release BOOTSEL - the Pico will appear as a USB drive
4. Download the MicroPython firmware from [the official page](https://micropython.org/download/rp2-pico/)
5. Copy the .uf2 file to the RPI-RP2 drive
6. The Pico will restart automatically

### Configure Permissions (Linux)

```bash
# Add your user to the dialout group
sudo usermod -a -G dialout $USER

# Give permissions to the serial port
sudo chmod 666 /dev/ttyACM0

# Important: Log out and back in for changes to take effect
```

## Project Structure

- `main.py`: Program entry point
- `game.py`: Main game logic
- `config.py`: Game and hardware configuration
- `tones.py`: Sound and melody handling
- `interfaces/`: Interface implementations (CLI and hardware)
- `hardware/`: LED and button controllers
- `utils/`: Utilities and exception handling

## Software Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/simon-boulder.git
cd simon-boulder/RP-Pico
```

2. **Upload files to the Pico**:

```bash
# Make sure the Pico is connected and MicroPython is running
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put config.py
ampy --port /dev/ttyACM0 put game.py
ampy --port /dev/ttyACM0 put tones.py

# Create and upload directories
ampy --port /dev/ttyACM0 mkdir interfaces
ampy --port /dev/ttyACM0 put interfaces/__init__.py /interfaces/__init__.py
ampy --port /dev/ttyACM0 put interfaces/hardware.py /interfaces/hardware.py
ampy --port /dev/ttyACM0 put interfaces/cli.py /interfaces/cli.py

ampy --port /dev/ttyACM0 mkdir utils
ampy --port /dev/ttyACM0 put utils/exceptions.py /utils/exceptions.py

ampy --port /dev/ttyACM0 mkdir hardware
ampy --port /dev/ttyACM0 put hardware/leds.py /hardware/leds.py
ampy --port /dev/ttyACM0 put hardware/buttons.py /hardware/buttons.py
```

## Game Usage

### On the Raspberry Pi Pico

The game is primarily designed to run on the Pico with physical components connected.

1. Ensure all hardware is connected according to the diagram
2. Connect the Pico to your computer
3. Upload the files:
   ```bash
   cd RP-Pico
   ampy --port /dev/ttyACM0 put main.py
   # ... (rest of the upload commands)
   ```
4. The game will start automatically when the Pico powers on

To view debug messages:

```bash
screen /dev/ttyACM0 115200
```

(To exit screen: Ctrl+A, then K, confirm with 'y')

### On Your Computer (Development/Testing)

To test the game without hardware:

```bash
cd RP-Pico
python3 main.py
```

The game will automatically run in CLI mode, allowing you to test game logic using the keyboard.

## Troubleshooting

### Pico Not Detected

If the Pico appears as a USB drive instead of a serial port:

1. It's probably in BOOTSEL mode
2. You need to reload MicroPython following the "Initial Setup" steps

### Permission Errors

If you receive permission errors:

```bash
sudo chmod 666 /dev/ttyACM0
```

### Issues with ampy

If ampy doesn't respond or times out:

1. Disconnect and reconnect the Pico
2. If it persists, reload MicroPython
3. Verify there are no other active serial connections
