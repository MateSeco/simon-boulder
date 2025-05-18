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

### Selected Hardware Components

#### Button and LED Kit (SKU: PRT1050)

- Used for game colors (RED, GREEN, BLUE, YELLOW)
- Package includes:
  - 4x Tactile push buttons
  - 4x LEDs (Red, Green, Blue, Yellow)
  - 4x 220Ω resistors

#### Reset Button (SKU: PRT1044)

- Dedicated tactile push button for reset functionality
- High-quality momentary switch
- 4-pin configuration
- Reliable tactile feedback

#### Active Buzzer Module (SKU: MK0077)

- KY-012 Active Buzzer Module
- Operating voltage: 3.3V-5V (compatible with Pico's 3.3V)
- Built-in drive circuit
- Clean, stable tone output
- Low power consumption

#### Microcontroller

- **Raspberry Pi Pico**
  - Microcontroller: RP2040
  - Operating voltage: 3.3V
  - Maximum current per GPIO pin: 12mA
  - Recommended input voltage (VSYS): 5V via USB

#### Breadboard and Cables

- **1x Breadboard**
  - Minimum 400 points
  - With power rails
- **20x Male-to-male Dupont cables**
  - Length: 10-20cm

#### USB Cable

- **1x Micro USB Cable**
  - For programming and power

## Hardware Connections

### Pin Layout Overview

![Raspberry Pi Pico Pinout](pico-pinout.svg)

For quick reference, here's a simplified diagram showing our pin assignments:

```
                  ┌─────────────────────────┐
                  │ O                     O │
                  │                         │
     RED LED    ──┤ GP2                GP0 │
    GREEN LED   ──┤ GP3                GP1 │
     BLUE LED   ──┤ GP4               GP16 │
   YELLOW LED   ──┤ GP5               GP17 │
     RED BTN    ──┤ GP6               GP18 │
    GREEN BTN   ──┤ GP7               GP19 │
     BLUE BTN   ──┤ GP8               GP20 │
   YELLOW BTN   ──┤ GP9               GP21 │
    RESET BTN   ──┤ GP10              GP22 │
                  │ GP11              GP26 │
                  │ GP12              GP27 │
                  │ GP13              GP28 │
                  │ GP14               RUN │
     BUZZER     ──┤ GP15              GP26│
                  │ GND                GND │
                  │ VSYS              VBUS │
                  │ 3V3               VSYS │
                  │                         │
                  │ O                     O │
                  └─────────────────────────┘
```

> **Note**: The SVG image above shows the complete pinout of the Raspberry Pi Pico. Our project uses specific pins highlighted in the ASCII diagram below it. Use both references when making your connections.

### Component Connections

#### LED Circuits

```
GPIO Pin ──┬──[220Ω]──┬── LED (+)
           │          └── LED (-) ── GND
```

| Color  | GPIO | Forward Voltage |
| ------ | ---- | --------------- |
| Red    | GP2  | ~2.0V           |
| Green  | GP3  | ~2.2V           |
| Blue   | GP4  | ~3.0V           |
| Yellow | GP5  | ~2.1V           |

All LEDs:

- Current limiting: 220Ω resistor
- Maximum current: 20mA
- Polarity: Long leg (+) to resistor

#### Button Circuits

```
GPIO Pin ─────┬─── Button ─── GND
              │
         Pull-up
         (internal)
```

| Button | GPIO | Function    |
| ------ | ---- | ----------- |
| Red    | GP6  | Color input |
| Green  | GP7  | Color input |
| Blue   | GP8  | Color input |
| Yellow | GP9  | Color input |
| Reset  | GP10 | Game reset  |

All buttons:

- Type: Momentary (normally open)
- Configuration: 4-pin tactile
- Uses internal pull-up resistor

#### Buzzer Module (KY-012)

```
3.3V ─── VCC ┐
             ├── Buzzer Module
GP15 ─── SIG │
GND  ─── GND ┘
```

- Signal pin: GP15
- Operating voltage: 3.3V
- Built-in driver circuit
- No external components needed

### Safety Considerations

1. **Power Requirements**

   - Operating voltage: 3.3V
   - Maximum current per GPIO: 12mA
   - Total current draw should not exceed 50mA

2. **GPIO Protection**

   - Never connect LEDs directly to GPIO pins without resistors
   - Verify button connections to prevent shorts
   - Double-check ground connections

3. **Voltage Levels**
   - All components must be 3.3V compatible
   - Do not use 5V components without level shifting

### Connection Verification

To verify your connections, connect to the Pico using screen:

```bash
screen /dev/ttyACM0 115200
```

Once connected:

1. The test program will run automatically
2. Follow the on-screen instructions to test each component
3. The program will guide you through testing:
   - Individual LED functionality
   - Button responses
   - Buzzer operation
   - Complete interactive testing

To exit screen when finished:

1. Press Ctrl+A
2. Then press K
3. Confirm with 'y'

If you need to run the test program again, simply press the reset button on the Pico.

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

The project follows a modular architecture that separates hardware interaction from game logic, making it possible to run the game both on physical hardware and in a command-line simulation mode.

### Core Components

#### Interfaces (`interfaces/`)

The game uses an interface-based design pattern that allows switching between hardware and CLI modes:

- `interfaces/hardware.py`: Hardware Interface Implementation

  - Manages physical components (LEDs, buttons, buzzer)
  - Provides hardware status monitoring and error handling
  - Implements automatic fallback to simulation for missing components
  - Features:
    - Component auto-detection
    - Real-time hardware status verification
    - Debounced button input handling
    - Timeout handling for user input
    - Graceful error handling for hardware failures

- `interfaces/cli.py`: Command-Line Interface Implementation
  - Provides a text-based interface for testing and development
  - Simulates all hardware components through keyboard input
  - Features:
    - Color input validation
    - Simple text-based game state display
    - Keyboard interrupt handling
    - Clean exit management

The interface selection is handled automatically based on the environment:

- On Raspberry Pi Pico: Uses hardware mode
- On regular computers: Uses CLI mode

No configuration is needed - the mode is automatically selected based on whether the code is running on MicroPython (Pico) or standard Python (computer).

#### Hardware Controllers (`hardware/`)

Low-level hardware management components:

- `hardware/leds.py`: LED Management

  - Individual LED control for each color
  - Automatic pin configuration
  - Error handling for connection issues
  - Simulation mode for missing LEDs

- `hardware/buttons.py`: Button Management

  - Hardware interrupt-based button detection
  - Software debouncing implementation
  - Callback registration system
  - Automatic pin configuration with pull-up resistors

- `hardware/buzzer.py`: Sound Management
  - PWM-based tone generation
  - Frequency and duration control
  - Note sequence playback
  - Simulation mode for testing without hardware

#### Game Logic (`game.py`)

Core game implementation that manages:

- Game State

  - Sequence generation and tracking
  - Player input handling
  - Platform-specific optimizations for MicroPython/Python

- Game Flow
  - Round progression and difficulty increase
  - Input validation and feedback
  - Visual and sound effects
  - Reset and error handling

The game automatically adapts to available hardware, providing appropriate feedback through LEDs, sounds, and debug messages.

#### Configuration and Utilities

- `config.py`: System Configuration

  - Hardware pin mappings
  - Game parameters
  - Interface mode selection
  - Sound frequencies
  - Timing constants

- `tones.py`: Sound System

  - Musical note definitions
  - Success/failure melodies
  - Color-specific tones
  - Hardware-independent sound interface

- `utils/`: Support Utilities
  - Custom exception definitions
  - Hardware error handling
  - Debug utilities

#### Entry Points

- `main.py`: Application Entry Point

  - Environment detection
  - Interface selection
  - Game initialization
  - Error handling and cleanup

- `test.py`: Hardware Test Suite
  - Component testing utilities
  - Interactive hardware verification
  - Diagnostic tools
  - Connection validation

## Software Installation

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/simon-boulder.git
cd simon-boulder/RP-Pico
```

2. **Upload files to the Pico**:

```bash
# Make sure the Pico is connected and MicroPython is running

# Upload main files
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put config.py
ampy --port /dev/ttyACM0 put game.py
ampy --port /dev/ttyACM0 put tones.py
ampy --port /dev/ttyACM0 put test.py

# Create and upload directories with their files
ampy --port /dev/ttyACM0 mkdir interfaces
ampy --port /dev/ttyACM0 put interfaces/__init__.py interfaces/__init__.py
ampy --port /dev/ttyACM0 put interfaces/hardware.py interfaces/hardware.py
ampy --port /dev/ttyACM0 put interfaces/cli.py interfaces/cli.py

ampy --port /dev/ttyACM0 mkdir utils
ampy --port /dev/ttyACM0 put utils/__init__.py utils/__init__.py
ampy --port /dev/ttyACM0 put utils/exceptions.py utils/exceptions.py

ampy --port /dev/ttyACM0 mkdir hardware
ampy --port /dev/ttyACM0 put hardware/__init__.py hardware/__init__.py
ampy --port /dev/ttyACM0 put hardware/leds.py hardware/leds.py
ampy --port /dev/ttyACM0 put hardware/buttons.py hardware/buttons.py
ampy --port /dev/ttyACM0 put hardware/buzzer.py hardware/buzzer.py
```

## Game Usage

### On the Raspberry Pi Pico

The game is designed to run on the Pico with physical components connected:

1. Ensure all hardware is connected according to the pinout diagram
2. Connect the Pico to your computer via USB
3. Upload all files using the commands in the Software Installation section
4. Once uploaded, you have two options to run the game:
   - Disconnect from computer and power the Pico via a USB power supply - the game will start automatically
   - Keep connected to computer and use screen to see debug messages:
     ```bash
     screen /dev/ttyACM0 115200
     ```

When using screen:

- The game will start automatically
- You'll see hardware detection messages and game state
- To exit: Press Ctrl+A, then K, then confirm with 'y'
- To restart the game: Press the reset button on the Pico

If any hardware component is missing:

- The game will detect this automatically
- Missing components will be simulated
- You can still play using available hardware
- Debug messages will show which components are active

### On Your Computer (Development/Testing)

For development and testing without hardware:

```bash
cd RP-Pico
python3 main.py
```

In this mode:

- The game automatically runs in CLI mode
- Use keyboard input to simulate buttons
- Type color names (RED, GREEN, BLUE, YELLOW) and press Enter
- Type RESET to restart the game
- Debug messages will show game state

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
