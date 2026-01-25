#!/bin/bash
# Script to upload all files to Raspberry Pi Pico
# Ahora sin boot.py automático para evitar bloqueos

PORT="/dev/ttyACM0"

echo "=========================================="
echo "Uploading Simon Says to Raspberry Pi Pico"
echo "=========================================="
echo ""

# Check if port exists
if [ ! -e "$PORT" ]; then
    echo "❌ Error: $PORT not found"
    echo "Please connect your Pico and try again"
    echo ""
    echo "Si la Pico no responde:"
    echo "  1. Mantené BOOTSEL y conectá"
    echo "  2. Cargá flash_nuke.uf2"
    echo "  3. Cargá MicroPython de nuevo"
    exit 1
fi

echo "📤 Uploading main files..."
ampy --port $PORT put main.py
ampy --port $PORT put config.py
ampy --port $PORT put game.py
ampy --port $PORT put tones.py

echo ""
echo "📁 Creating directories..."
ampy --port $PORT mkdir interfaces 2>/dev/null || true
ampy --port $PORT mkdir hardware 2>/dev/null || true
ampy --port $PORT mkdir utils 2>/dev/null || true

echo ""
echo "📤 Uploading interfaces..."
ampy --port $PORT put interfaces/__init__.py interfaces/__init__.py
ampy --port $PORT put interfaces/hardware.py interfaces/hardware.py
ampy --port $PORT put interfaces/cli.py interfaces/cli.py

echo ""
echo "📤 Uploading hardware..."
ampy --port $PORT put hardware/__init__.py hardware/__init__.py
ampy --port $PORT put hardware/leds.py hardware/leds.py
ampy --port $PORT put hardware/buttons.py hardware/buttons.py
ampy --port $PORT put hardware/buzzer.py hardware/buzzer.py

echo ""
echo "📤 Uploading utils..."
ampy --port $PORT put utils/__init__.py utils/__init__.py
ampy --port $PORT put utils/exceptions.py utils/exceptions.py

echo ""
echo "✅ Main files uploaded!"
echo ""
echo "🧪 Testing game (Ctrl+C to stop)..."
echo ""
ampy --port $PORT run main.py

# Si llegamos acá sin error, preguntar si subir boot.py
echo ""
echo "=========================================="
read -p "¿El juego funcionó bien? Subir boot.py para arranque automático? (s/n): " response
if [[ "$response" =~ ^[Ss]$ ]]; then
    echo "📤 Uploading boot.py..."
    ampy --port $PORT put boot.py
    echo "✅ boot.py uploaded!"
    echo ""
    echo "🎮 El juego arrancará automáticamente al conectar la Pico."
else
    echo "⏭️  boot.py no subido."
    echo "   Para subir manualmente: ampy --port $PORT put boot.py"
fi

echo ""
echo "=========================================="
echo "Done!"
echo "=========================================="
