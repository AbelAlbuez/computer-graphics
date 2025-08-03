# Juego de la Vida de Conway - Generador de Animaciones

## Descripción

Este proyecto implementa un generador de animaciones para el Juego de la Vida de Conway. El programa lee una configuración inicial desde un archivo PBM y genera una secuencia de imágenes que muestran la evolución del autómata celular.

## Instalación Rápida

```bash
# Navegar al proyecto
cd computer-graphics/taller-conway-game-of-life

# Compilar
make

# Ejecutar ejemplo
./bin/juego_vida src/ejemplo.pbm 3.0 10
```

## Características

- Lectura de archivos PBM (Portable Bitmap) formato P1
- Generación de secuencias de frames en formato PBM o PPM
- Detección de patrones estáticos
- Barra de progreso con estadísticas en tiempo real
- Arquitectura modular y extensible

## Compilación

### Requisitos
- Compilador C++ con soporte para C++11 (g++, clang++)
- Make
- Sistema operativo Linux/Unix o Windows con MinGW

### Archivos Necesarios
Asegúrate de tener todos los archivos header (`.h`) en la carpeta `src/`:
- `tablero.h`
- `archivo_pbm.h`
- `juego_vida.h`
- `generador_frames.h`
- `utilidades.h`

### Instrucciones de compilación

```bash
# Navegar al directorio del proyecto
cd computer-graphics/taller-conway-game-of-life

# Compilar
make

# O compilar en modo debug
make debug

# Limpiar archivos compilados y frames generados
make clean

# Limpiar solo los frames generados
make clean-frames
```

## Uso

### Sintaxis básica

```bash
./bin/juego_vida <archivo.pbm> <duracion> <fps>
```

### Parámetros

- `archivo.pbm`: Archivo PBM con la configuración inicial (formato P1)
- `duracion`: Duración de la animación en segundos (número decimal)
- `fps`: Cuadros por segundo (número entero)

### Ejemplos

```bash
# Generar 30 frames (3 segundos a 10 fps) del archivo ejemplo
./bin/juego_vida src/ejemplo.pbm 3.0 10

# Generar 150 frames (5 segundos a 30 fps) de un glider
./bin/juego_vida src/glider.pbm 5.0 30

# Generar 60 frames (2 segundos a 30 fps) de un blinker
./bin/juego_vida src/blinker.pbm 2.0 30

# Ver ayuda
./bin/juego_vida --help
```

## Archivos de Ejemplo

Los archivos PBM de ejemplo deben guardarse en la carpeta `src/`. A continuación se muestran algunos patrones clásicos:

### 1. Glider (src/glider.pbm)
```
P1
# Glider pattern
10 10
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

### 2. Blinker (src/blinker.pbm)
```
P1
# Blinker oscillator
5 5
0 0 0 0 0
0 0 1 0 0
0 0 1 0 0
0 0 1 0 0
0 0 0 0 0
```

### 3. Toad (src/toad.pbm)
```
P1
# Toad oscillator
6 6
0 0 0 0 0 0
0 0 0 0 0 0
0 0 1 1 1 0
0 1 1 1 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

### 4. Beacon (src/beacon.pbm)
```
P1
# Beacon oscillator
6 6
0 0 0 0 0 0
0 1 1 0 0 0
0 1 0 0 0 0
0 0 0 0 1 0
0 0 0 1 1 0
0 0 0 0 0 0
```

## Creación de Videos

Los frames se generan en el directorio actual como `frame_00000.pbm`, `frame_00001.pbm`, etc.

Una vez generados los frames, puedes crear un video usando FFmpeg:

```bash
# Crear video MP4
ffmpeg -framerate 30 -i frame_%05d.pbm -c:v libx264 -pix_fmt yuv420p output.mp4

# Crear GIF animado (usando ImageMagick)
convert -delay 3 frame_*.pbm animation.gif

# Crear video con mejor calidad
ffmpeg -framerate 30 -i frame_%05d.pbm -c:v libx264 -crf 20 -pix_fmt yuv420p output_hq.mp4
```

**Nota**: Los frames se guardan en el directorio desde donde ejecutas el programa.

## Estructura del Proyecto

```
computer-graphics/
└── taller-conway-game-of-life/
    ├── src/
    │   ├── main.cpp               # Programa principal
    │   ├── tablero.h              # Gestión del tablero
    │   ├── tablero.cpp         
    │   ├── archivo_pbm.h          # Lectura/escritura PBM
    │   ├── archivo_pbm.cpp     
    │   ├── juego_vida.h           # Lógica del juego
    │   ├── juego_vida.cpp      
    │   ├── generador_frames.h     # Generación de frames
    │   ├── generador_frames.cpp
    │   ├── utilidades.h           # Funciones auxiliares
    │   ├── utilidades.cpp      
    │   ├── FrameBuffer.h          # Buffer de imagen (reutilizado)
    │   ├── FrameBuffer.cxx        # Implementación (reutilizado)
    │   └── ejemplo.pbm            # Archivo PBM de ejemplo
    ├── obj/                       # Archivos objeto (generado)
    ├── bin/                       # Ejecutable (generado)
    ├── Makefile                   # Sistema de compilación
    └── README.md                  # Este archivo
```

## Formato PBM

El formato PBM (Portable Bitmap) es un formato de imagen simple:

```
P1                    # Número mágico (P1 = ASCII)
# Comentario opcional
ancho alto           # Dimensiones
0 1 0 1 ...         # Datos (0=blanco, 1=negro)
```

## Reglas del Juego de la Vida

1. **Supervivencia**: Una célula viva con 2 o 3 vecinos vivos sobrevive
2. **Muerte por soledad**: Una célula viva con menos de 2 vecinos muere
3. **Muerte por sobrepoblación**: Una célula viva con más de 3 vecinos muere
4. **Nacimiento**: Una célula muerta con exactamente 3 vecinos vivos nace

## Características Técnicas

- **Detección de patrones estáticos**: El programa detecta cuando el tablero deja de evolucionar
- **Estadísticas en tiempo real**: Muestra el número de células vivas en cada frame
- **Barra de progreso**: Indica el avance de la generación
- **Manejo de errores**: Validación robusta de entrada y manejo de excepciones
- **Código modular**: Fácil de extender y mantener

## Problemas Comunes

### Error: "No se puede abrir el archivo"
- Verifica que el archivo PBM existe y tiene el formato correcto
- Asegúrate de que el archivo comience con "P1"

### Error: "Dimensiones inválidas"
- Verifica que el archivo PBM tenga dimensiones válidas (números positivos)

### Se generan demasiados frames
- Reduce la duración o los FPS
- Considera que duracion × fps = número total de frames

## Extensiones Futuras

- Soporte para otros formatos de imagen
- Detección de osciladores y períodos
- Interfaz gráfica
- Soporte para reglas personalizadas
- Optimización con paralelización

## Licencia

Este proyecto es software libre para uso educativo.

## Entregable del Taller

Para entregar el taller, crea un archivo ZIP que contenga:

```
taller-conway-game-of-life.zip
├── src/                    # Todo el código fuente
├── Makefile               # Sistema de compilación
├── README.md              # Este manual
└── ejemplos/              # (Opcional) Archivos PBM de prueba
```

**Fecha límite**: Antes de la tercera sesión del curso

## Autores

- Abel Albuez
- Ricardo Cruz

## Agradecimientos

- John Conway por crear el Juego de la Vida
- Comunidad de autómatas celulares