#!/bin/bash
# Script to upload all files to Raspberry Pi Pico
# Without automatic boot.py to avoid lockups

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

echo "Uploading main files..."
ampy --port $PORT put main.py
ampy --port $PORT put config.py

echo ""
echo "Main files uploaded!"
echo ""
echo "Testing game (Ctrl+C to stop)..."
echo ""
ampy --port $PORT run main.py

# If we get here without error, ask to upload boot.py
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
