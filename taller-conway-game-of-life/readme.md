# Juego de la Vida de Conway - Generador de Animaciones

Implementación del autómata celular de Conway con generación de animaciones en C++. Este proyecto permite cargar patrones desde archivos PBM y generar secuencias de frames que pueden convertirse en videos o visualizarse en un navegador web.

## Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Compilación](#compilación)
- [Manual de Uso](#manual-de-uso)
- [Ejemplos](#ejemplos)
- [Visualización](#visualización)
- [Conceptos Aprendidos](#conceptos-aprendidos)

## Descripción

El Juego de la Vida es un autómata celular diseñado por John Conway en 1970. Este proyecto implementa:

- **Carga de patrones**: Lee configuraciones iniciales desde archivos PBM
- **Simulación**: Aplica las reglas de Conway para evolucionar el tablero
- **Generación de frames**: Crea secuencias de imágenes PPM para animaciones
- **Visualización web**: Genera un visualizador HTML interactivo

### Reglas de Conway
1. **Supervivencia**: Una célula viva con 2-3 vecinos sobrevive
2. **Muerte por soledad**: Una célula viva con <2 vecinos muere
3. **Muerte por sobrepoblación**: Una célula viva con >3 vecinos muere
4. **Nacimiento**: Una célula muerta con exactamente 3 vecinos nace

## Características

- Lectura/escritura de archivos PBM (Portable Bitmap)
- Generación de frames en formato PPM (color) o PBM (blanco y negro)
- Barra de progreso visual durante la generación
- Visualizador HTML5 interactivo con controles play/pausa
- Integración con FrameBuffer para renderizado eficiente
- Soporte para patrones clásicos (glider, blinker, toad, pulsar)

## Estructura del Proyecto

```
taller-conway-game-of-life/
├── bin/                      # Ejecutables compilados
│   └── juego_vida           # Ejecutable principal
├── ejemplos/                # Patrones de ejemplo en formato PBM
│   ├── blinker.pbm         # Oscilador simple (período 2)
│   ├── block.pbm           # Patrón estático 2x2
│   ├── ejemplo.pbm         # Patrón de ejemplo
│   ├── glider.pbm          # Nave espacial clásica
│   ├── pulsar.pbm          # Oscilador complejo (período 3)
│   └── toad.pbm            # Oscilador (período 2)
├── frames/                  # Directorio de salida para frames
├── obj/                     # Archivos objeto compilados
├── src/                     # Código fuente
│   ├── archivo_pbm.h/.cpp      # Manejo de archivos PBM
│   ├── FrameBuffer.h/.cxx      # Renderizado de imágenes
│   ├── generador_frames.h/.cpp # Generación de animaciones
│   ├── juego_vida.h/.cpp       # Lógica del autómata celular
│   ├── main.cpp                # Programa principal
│   ├── tablero.h/.cpp          # Estructura del tablero
│   └── utilidades.h/.cpp       # Funciones auxiliares
├── videos/                  # Videos generados (opcional)
├── Makefile                # Script de compilación
├── visualizador.html       # Visualizador web generado
├── Observaciones.docx      # Documentación del aprendizaje
└── README.md               # Este archivo
```

## Requisitos

### Software Necesario
- **Compilador C++**: g++ con soporte para C++11 o superior
- **Make**: Para compilación automatizada
- **Navegador web moderno**: Para el visualizador HTML

### Herramientas Opcionales
- **FFmpeg**: Para convertir frames a video
- **ImageMagick**: Para crear GIFs animados

## Compilación

### Clonar el Repositorio
```bash
git clone https://github.com/AbelAlbuez/computer-graphics.git
cd computer-graphics/taller-conway-game-of-life
```

### Compilación Básica
```bash
make
```

### Compilación Limpia
```bash
make clean  # Elimina archivos objeto
make        # Recompila todo
```

### Compilación Manual (sin Make)
```bash
g++ -std=c++11 -o bin/juego_vida src/*.cpp src/*.cxx
```

## Manual de Uso

### Sintaxis Básica
```bash
./bin/juego_vida <archivo.pbm> <duracion> <fps>
```

### Parámetros
- **archivo.pbm**: Archivo con el patrón inicial (formato PBM P1)
- **duracion**: Duración de la animación en segundos (decimal)
- **fps**: Frames por segundo (entero)

### Ejemplos de Uso

#### 1. Generar animación del Glider (5 segundos a 30 fps)
```bash
./bin/juego_vida ejemplos/glider.pbm 5.0 30
```
Genera 150 frames del patrón glider

#### 2. Animación corta del Blinker (2 segundos a 10 fps)
```bash
./bin/juego_vida ejemplos/blinker.pbm 2.0 10
```
Genera 20 frames mostrando la oscilación

#### 3. Ver ayuda
```bash
./bin/juego_vida -h
```

### Salida
- Los frames se guardan en `frames/` como `frame_00000.ppm`, `frame_00001.ppm`, etc.
- Se genera automáticamente `visualizador.html` para ver la animación

## Ejemplos

### Patrones Incluidos

| Patrón | Tipo | Descripción |
|--------|------|-------------|
| **block.pbm** | Estático | Cuadrado 2x2 que no cambia |
| **blinker.pbm** | Oscilador | Línea de 3 células que alterna vertical/horizontal |
| **toad.pbm** | Oscilador | Forma de 6 células con período 2 |
| **glider.pbm** | Nave | Se desplaza diagonalmente por el tablero |
| **pulsar.pbm** | Oscilador | Patrón simétrico complejo con período 3 |

### Formato PBM
Los archivos PBM deben estar en formato P1 (ASCII):
```
P1
# Comentario opcional
6 6
0 0 0 0 0 0
0 0 1 0 0 0
0 0 0 1 0 0
0 1 1 1 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

## Visualización

### Visualizador Web
Abre `visualizador.html` en tu navegador después de generar frames:
- **Play/Pausa**: Controla la animación
- **Reiniciar**: Vuelve al frame 0
- **Indicador**: Muestra frame actual/total

### Crear Video con FFmpeg
```bash
# MP4 con códec H.264
ffmpeg -framerate 30 -i frames/frame_%05d.ppm -c:v libx264 -pix_fmt yuv420p output.mp4

# AVI sin compresión
ffmpeg -framerate 30 -i frames/frame_%05d.ppm -c:v rawvideo output.avi
```

### Crear GIF con ImageMagick
```bash
# GIF animado
convert -delay 10 frames/frame_*.ppm -loop 0 animation.gif

# GIF optimizado (más pequeño)
convert -delay 10 frames/frame_*.ppm -loop 0 -layers Optimize animation.gif
```

### Reproducir con FFplay
```bash
ffplay -framerate 30 -i frames/frame_%05d.ppm
```

## Conceptos Aprendidos

### 1. **Autómatas Celulares**
- Reglas locales generan comportamiento global
- Evolución determinista pero compleja
- Paralelismo implícito en la actualización

### 2. **Patrones y Comportamientos**
- **Estáticos**: Configuraciones estables (block)
- **Osciladores**: Ciclos periódicos (blinker, toad, pulsar)
- **Naves espaciales**: Movimiento sin propulsión (glider)

### 3. **Implementación Técnica**
- **Doble buffer**: Cálculo de nuevo estado sin modificar el actual
- **Conteo de vecinos**: Algoritmo de las 8 direcciones
- **Condiciones de borde**: Células fuera del tablero = muertas

### 4. **Diseño Modular**
- Separación lógica (JuegoVida) de visualización (FrameBuffer)
- Reutilización de código existente
- Interfaces claras entre componentes

### 5. **Procesamiento de Imágenes**
- Conversión entre representaciones (bool → RGB → PPM)
- Generación de secuencias numeradas
- Creación de visualizadores interactivos

## Mejoras Futuras

- Soporte para más formatos de imagen (PNG, JPEG)
- Patrones aleatorios y semillas
- Zoom y desplazamiento en el visualizador
- Detección automática de ciclos
- Estadísticas de población por frame
- Reglas personalizables (variantes del juego)
- Tableros toroidales (bordes conectados)

## Autores

**Abel Albuez**  
**Ricardo Cruz**

## Repositorio

Este proyecto está disponible en GitHub:  
[https://github.com/AbelAlbuez/computer-graphics](https://github.com/AbelAlbuez/computer-graphics)

### Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

### Reportar Problemas

Si encuentras algún bug o tienes sugerencias, por favor abre un issue en:  
[https://github.com/AbelAlbuez/computer-graphics/issues](https://github.com/AbelAlbuez/computer-graphics/issues)

## Referencias

- [Wikipedia - Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)
- [LifeWiki - Catálogo de patrones](https://conwaylife.com/wiki/Main_Page)
- [Formato PBM](http://netpbm.sourceforge.net/doc/pbm.html)

---

*"El Juego de la Vida demuestra que la complejidad puede emerger de reglas simples"* - John Conway