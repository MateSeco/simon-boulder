# Simon Says for Raspberry Pi Pico

Simon Says project for Raspberry Pi Pico using MicroPython, LEDs, buttons, and a buzzer.

## Current Project Status

This README describes the current refactored repository structure, without legacy modules.

Main structure:

```text
simon-boulder/
├── README.md
├── pico-pinout.svg
└── RP-Pico/
    ├── main.py
    ├── config.py
    ├── boot.py
    ├── upload_to_pico.sh
    └── hardware/
        ├── __init__.py
        ├── leds.py
        └── buzzer.py
```

## Features

- Random and progressive Simon Says color sequences.
- Interrupt-driven button capture with software debounce and event-queue processing.
- Visual feedback (LEDs) and sound feedback (buzzer).
- `RESET` button to restart the game during execution.
- Optional auto-start when the board is powered (`boot.py`).

## Hardware Requirements

- 1x Raspberry Pi Pico
- 4x LEDs (red, green, blue, yellow)
- 4x color buttons (or equivalent)
- 1x additional reset button
- 1x buzzer (for example, KY-012)
- Breadboard and Dupont wires

## Pin Map

### GPIO Assignment (configurable in `RP-Pico/config.py`)

- Red LED: `GP2`
- Green LED: `GP3`
- Blue LED: `GP4`
- Yellow LED: `GP5`
- Red button: `GP6`
- Green button: `GP7`
- Blue button: `GP8`
- Yellow button: `GP9`
- Reset button: `GP10`
- Buzzer signal: `GP15`

### Pico Physical Pin Mapping

| Function | GPIO | Physical Pin |
|---|---:|---:|
| LED RED | GP2 | 4 |
| LED GREEN | GP3 | 5 |
| LED BLUE | GP4 | 6 |
| LED YELLOW | GP5 | 7 |
| BTN RED | GP6 | 9 |
| BTN GREEN | GP7 | 10 |
| BTN BLUE | GP8 | 11 |
| BTN YELLOW | GP9 | 12 |
| BTN RESET | GP10 | 14 |
| BUZZER SIG | GP15 | 20 |

> Visual reference: `pico-pinout.svg`

## Recommended Wiring

### LEDs

- LED anode -> resistor -> color GPIO.
- LED cathode -> GND.

### Buttons

- One button terminal -> corresponding GPIO.
- Other button terminal -> GND.
- Firmware uses internal pull-up (`Pin.PULL_UP`), so idle state is `1` and pressed state is `0`.

### RESET Button (game logic)

- Wire it like all other buttons:
  - One terminal -> `GP10` (physical pin 14)
  - Other terminal -> GND
- Function: restarts the game while it is waiting for user input.

### Buzzer

For a KY-012 type module:

- `SIG` -> `GP15` (pin 20)
- `GND` -> GND
- `VCC` -> 3V3

## Install MicroPython Firmware

1. Hold `BOOTSEL` while connecting the Pico through USB.
2. Copy the MicroPython `.uf2` firmware to the `RPI-RP2` device.
3. The Pico reboots and usually appears as a serial port (for example `/dev/ttyACM0` on Linux).

## Upload Project to Pico

From the `RP-Pico` folder:

```bash
cd RP-Pico
chmod +x upload_to_pico.sh
./upload_to_pico.sh
```

The script:

1. Uploads required files (`config.py`, `main.py`, `hardware/*`).
2. Runs `main.py` for validation.
3. Asks whether to upload `boot.py` for auto-start.

## Manual Run (without script)

```bash
cd RP-Pico
ampy --port /dev/ttyACM0 put config.py
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 mkdir hardware
ampy --port /dev/ttyACM0 put hardware/__init__.py hardware/__init__.py
ampy --port /dev/ttyACM0 put hardware/leds.py hardware/leds.py
ampy --port /dev/ttyACM0 put hardware/buzzer.py hardware/buzzer.py
ampy --port /dev/ttyACM0 run main.py
```

To enable auto-start after validation:

```bash
ampy --port /dev/ttyACM0 put boot.py
```

## Game Usage

- On startup, the game shows a color sequence.
- Repeat the sequence using the color buttons.
- A wrong press ends the current game and starts a new one.
- Press `RESET` to restart the game.

## Quick Troubleshooting

- If `/dev/ttyACM0` does not appear, reconnect the board and verify it is not in BOOTSEL mode.
- If the board is locked by a bad `boot.py`, enter BOOTSEL mode and reinstall MicroPython.
- If `ampy` fails due to a busy port, close other serial tools (`screen`, etc.).
- If an LED does not turn on, check polarity and resistor wiring.
- If a button does not respond, verify it is connected to both GND and the correct GPIO.
