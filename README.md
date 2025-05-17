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

## Lista de Componentes

### Componentes Principales

- 1x Raspberry Pi Pico
- 1x Protoboard (mínimo 400 puntos)
- 1x Cable micro USB

### LEDs (5mm)

- 1x LED Rojo (Vf ≈ 2.0V, If = 20mA)
- 1x LED Verde (Vf ≈ 2.1V, If = 20mA)
- 1x LED Azul (Vf ≈ 3.0V, If = 20mA)
- 1x LED Amarillo (Vf ≈ 2.1V, If = 20mA)
- 4x Resistencias 220Ω (para LEDs)

### Botones y Buzzer

- 5x Pulsadores momentáneos (táctiles) de 4 pines (6x6x5mm)
- 1x Buzzer activo (5V, ~23mm diámetro)

### Cables

- 20x Cables Dupont macho-macho para conexiones
- Opcional: Cable para protoboard (22 AWG) para conexiones más limpias

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

## Montaje en Protoboard

### Preparación

1. Coloca la Raspberry Pi Pico en el centro de la protoboard, dejando espacio suficiente a ambos lados
2. Asegúrate de que los pines GND y VBUS sean fácilmente accesibles

### Conexión de LEDs

1. Coloca los LEDs en un lado de la protoboard:
   ```
   Columna A: LED Rojo
   Columna C: LED Verde
   Columna E: LED Azul
   Columna G: LED Amarillo
   ```
2. Conecta las resistencias de 220Ω a los ánodos (pata más larga) de cada LED
3. Conecta el otro extremo de cada resistencia al pin GPIO correspondiente
4. Conecta los cátodos (pata más corta) a la línea de GND

### Conexión de Botones

1. Coloca los botones en el otro lado de la protoboard:
   ```
   Fila 15-16: Botón Rojo
   Fila 20-21: Botón Verde
   Fila 25-26: Botón Azul
   Fila 30-31: Botón Amarillo
   Fila 35-36: Botón Reset
   ```
2. Conecta un pin de cada botón al GPIO correspondiente
3. Conecta el otro pin de cada botón a GND
4. Los otros dos pines del botón no se utilizan

### Conexión del Buzzer

1. Coloca el buzzer en la parte superior de la protoboard
2. Identifica el pin positivo (generalmente marcado con '+' o pin más largo)
3. Conecta el pin positivo al GP15
4. Conecta el pin negativo a GND

### Diagrama de Protoboard

```
                                   Raspberry Pi Pico
                                   ┌──────────────┐
                                   │              │
         LED Rojo (+ resistor) ────┤GP2           │
         LED Verde (+ resistor) ───┤GP3           │
         LED Azul (+ resistor) ────┤GP4           │
         LED Amarillo (+ resistor) ┤GP5           │
                                   │              │
         Botón Rojo ──────────────┤GP6    GND  ──┤
         Botón Verde ─────────────┤GP7           │
         Botón Azul ──────────────┤GP8           │
         Botón Amarillo ──────────┤GP9           │
         Botón Reset ─────────────┤GP10          │
                                   │              │
         Buzzer (+) ──────────────┤GP15          │
         Buzzer (-) ──────────────┤GND           │
                                   │              │
                                   └──────────────┘
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

## Modos de Operación

1. **Modo Hardware** (en Raspberry Pi Pico):

   - Utiliza componentes físicos (LEDs, botones, buzzer)
   - Es el modo por defecto al ejecutar en la Pico
   - Requiere el hardware conectado según el diagrama

2. **Modo CLI** (en computadora):
   - Interfaz por línea de comandos para pruebas
   - Solo funciona cuando ejecutas el código en tu computadora
   - No requiere hardware
   - Para ejecutar:
     ```bash
     python main.py
     ```

## Ejecución del Juego

### En tu Computadora (Modo CLI)

```bash
# El juego siempre correrá en modo CLI en la computadora
python main.py
```

### En la Raspberry Pi Pico (Modo Hardware)

1. Asegúrate de que todo el hardware está conectado según el diagrama
2. Conecta la Pico a tu computadora
3. Carga los archivos usando ampy (ver sección de Instalación)
4. La Pico ejecutará el programa automáticamente después de cargar los archivos

### Monitorear la Salida Serial

```bash
screen /dev/ttyACM0 115200
```

Para salir de screen: presiona Ctrl+A seguido de K y confirma con 'y'

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

## Contribuir

[Instrucciones para contribuir al proyecto]

## Licencia

[Tu licencia aquí]

---

**Nota**: Para agregar fotos del montaje, se recomienda:

1. Tomar fotos claras del montaje final
2. Incluir fotos del paso a paso del montaje
3. Agregar fotos de puntos críticos o conexiones importantes
4. Usar un fondo claro y buena iluminación
