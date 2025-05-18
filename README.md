# Simon Says para Raspberry Pi Pico

Una implementación del clásico juego Simon Says para Raspberry Pi Pico. El juego desafía a los jugadores a repetir secuencias de colores cada vez más largas, combinando LEDs, botones y efectos de sonido para una experiencia interactiva completa.

## Características Principales

- Secuencias de colores aleatorias y progresivas
- Interfaz hardware con LEDs, botones y feedback sonoro
- Modo CLI en computadora para desarrollo y pruebas
- Sonidos únicos para cada color
- Melodías especiales para eventos del juego
- Debouncing para los botones
- Modo de ahorro de energía
- Diseño modular y fácil de modificar

## Componentes Necesarios

### Microcontrolador

- **Raspberry Pi Pico**
  - Microcontrolador: RP2040
  - Voltaje de operación: 3.3V
  - Corriente máxima por pin GPIO: 12mA
  - Voltaje de entrada recomendado (VSYS): 5V vía USB

### LEDs

- **4x LEDs de propósito general**
  - Corriente directa (If): 20mA máximo
  - Colores: Rojo, Verde, Azul, Amarillo
  - Tipo de montaje: Through-hole

### Resistencias

- **4x Resistencias para LEDs**
  - Valor: 220Ω
  - Tolerancia: ±5%
  - Potencia: 1/4W

### Pulsadores

- **5x Pulsadores táctiles**
  - Tipo: Momentáneo (normalmente abierto)
  - Configuración: 4 pines
  - Dimensiones: 6mm x 6mm x 5mm

### Buzzer

- **1x Módulo Buzzer Activo (KY-012)**
  - Voltaje de operación: 3.5V - 5.5V (compatible con 3.3V)
  - Corriente de operación: <25mA
  - Frecuencia: 2300 ± 500 Hz
  - Pines: VCC, GND, S (señal)

### Protoboard y Cables

- **1x Protoboard**
  - Mínimo 400 puntos
  - Con líneas de alimentación
- **20x Cables Dupont macho-macho**
  - Longitud: 10-20cm

### Cable USB

- **1x Cable Micro USB**
  - Para programación y alimentación

## Montaje en Protoboard

### Conexión de LEDs

1. Conecta los LEDs respetando la polaridad:
   - Ánodo (pata más larga) → Resistencia 220Ω → Pin GPIO
   - Cátodo (pata más corta) → GND
   ```
   LED Rojo   → GP2
   LED Verde  → GP3
   LED Azul   → GP4
   LED Amarillo → GP5
   ```

### Conexión de Botones

1. Conecta un pin de cada botón al GPIO correspondiente y el otro a GND:
   ```
   Botón Rojo    → GP6
   Botón Verde   → GP7
   Botón Azul    → GP8
   Botón Amarillo → GP9
   Botón Reset   → GP10
   ```

### Conexión del Módulo Buzzer (KY-012)

1. Conecta los tres pines del módulo:
   ```
   VCC → 3.3V de la Pico
   GND → GND
   S (señal) → GP15
   ```

### Verificación

1. Revisa que no haya cortocircuitos
2. Verifica la polaridad de todos los LEDs
3. Confirma que los botones hacen buen contacto
4. Asegúrate de que todas las conexiones a GND y 3.3V estén correctas

## Configuración Inicial

### Instalar MicroPython en la Pico

1. Mantén presionado el botón BOOTSEL en la Pico
2. Conecta la Pico a tu computadora mientras mantienes BOOTSEL
3. Suelta BOOTSEL - la Pico aparecerá como una unidad USB
4. Descarga el firmware de MicroPython desde [la página oficial](https://micropython.org/download/rp2-pico/)
5. Copia el archivo .uf2 a la unidad RPI-RP2
6. La Pico se reiniciará automáticamente

### Configurar Permisos (Linux)

```bash
# Agregar tu usuario al grupo dialout
sudo usermod -a -G dialout $USER

# Dar permisos al puerto serial
sudo chmod 666 /dev/ttyACM0

# Importante: Cierra sesión y vuelve a iniciar para que los cambios surtan efecto
```

## Estructura del Proyecto

- `main.py`: Punto de entrada del programa
- `game.py`: Lógica principal del juego
- `config.py`: Configuración del juego y hardware
- `tones.py`: Manejo de sonidos y melodías
- `interfaces/`: Implementaciones de las interfaces (CLI y hardware)
- `hardware/`: Controladores para LEDs y botones
- `utils/`: Utilidades y manejo de excepciones

## Instalación del Software

1. **Clonar el repositorio**:

```bash
git clone https://github.com/tu-usuario/simon-boulder.git
cd simon-boulder/RP-Pico
```

2. **Cargar archivos a la Pico**:

```bash
# Asegúrate de que la Pico está conectada y MicroPython está funcionando
ampy --port /dev/ttyACM0 put main.py
ampy --port /dev/ttyACM0 put config.py
ampy --port /dev/ttyACM0 put game.py
ampy --port /dev/ttyACM0 put tones.py

# Crear y cargar directorios
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

## Uso del Juego

### En la Raspberry Pi Pico

El juego está diseñado principalmente para ejecutarse en la Pico con los componentes físicos conectados.

1. Asegúrate de que todo el hardware está conectado según el diagrama
2. Conecta la Pico a tu computadora
3. Carga los archivos:
   ```bash
   cd RP-Pico
   ampy --port /dev/ttyACM0 put main.py
   # ... (resto de los comandos de carga)
   ```
4. El juego iniciará automáticamente al encender la Pico

Para ver los mensajes de debug:

```bash
screen /dev/ttyACM0 115200
```

(Para salir de screen: Ctrl+A, luego K, confirmar con 'y')

### En tu Computadora (Desarrollo/Testing)

Para probar el juego sin hardware:

```bash
cd RP-Pico
python3 main.py
```

El juego correrá automáticamente en modo CLI, permitiendo probar la lógica del juego usando el teclado.

## Solución de Problemas

### La Pico no es detectada

Si la Pico aparece como unidad USB en lugar de puerto serial:

1. Probablemente está en modo BOOTSEL
2. Necesitas recargar MicroPython siguiendo los pasos de "Configuración Inicial"

### Error de Permisos

Si recibes errores de permisos:

```bash
sudo chmod 666 /dev/ttyACM0
```

### Problemas con ampy

Si ampy no responde o da timeout:

1. Desconecta y vuelve a conectar la Pico
2. Si persiste, recarga MicroPython
3. Verifica que no hay otras conexiones seriales activas
