#!/bin/bash
# Script to upload Simon Says to Raspberry Pi Pico

PORT="/dev/ttyACM0"

echo "=========================================="
echo "Uploading Simon Says to Raspberry Pi Pico"
echo "=========================================="
echo ""

# Check if port exists
if [ ! -e "$PORT" ]; then
    echo "Error: $PORT not found"
    echo "Please connect your Pico and try again"
    echo ""
    echo "If Pico is not responding:"
    echo "  1. Hold BOOTSEL and connect"
    echo "  2. Copy flash_nuke.uf2"
    echo "  3. Reload MicroPython"
    exit 1
fi

echo "Uploading files..."

# Main files
echo "  -> config.py"
ampy --port $PORT put config.py

echo "  -> main.py"
ampy --port $PORT put main.py

# Hardware directory
echo "  -> hardware/"
ampy --port $PORT mkdir hardware 2>/dev/null || true
ampy --port $PORT put hardware/__init__.py hardware/__init__.py
ampy --port $PORT put hardware/leds.py hardware/leds.py
ampy --port $PORT put hardware/buzzer.py hardware/buzzer.py

echo ""
echo "Files uploaded!"
echo ""
echo "Testing game (Ctrl+C to stop)..."
echo ""
ampy --port $PORT run main.py

# Ask to upload boot.py
echo ""
echo "=========================================="
read -p "Did the game work? Upload boot.py for auto-start? (y/n): " response
if [[ "$response" =~ ^[Yy]$ ]]; then
    echo "Uploading boot.py..."
    ampy --port $PORT put boot.py
    echo "boot.py uploaded!"
    echo ""
    echo "Game will start automatically when Pico is connected."
else
    echo "boot.py not uploaded."
    echo "To upload manually: ampy --port $PORT put boot.py"
fi

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
