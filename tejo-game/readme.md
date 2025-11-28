# 🎯 Juego de Tejo - Simulador 3D

## Proyecto Final de Computación Gráfica

**Pontificia Universidad Javeriana**  
**Maestría en Inteligencia Artificial**  
**Profesor:** Leonardo Florez-Valencia (florez-l@javeriana.edu.co)  
**Fecha de entrega:** 24 de noviembre de 2025

---

## 👥 Integrantes del Equipo

| Integrante | Rol Principal |
|------------|---------------|
| **Abel Albuez** | Física (PyBullet), colisiones, sistema de puntuación, lógica de turnos |
| **Alejandro Caicedo Caicedo** | Visuales avanzados, UI/HUD, geometrías 3D con VTK |
| **Ricardo Cruz Solano** | Documentación, testing, QA |

---

## 📋 Descripción del Proyecto

Simulador 3D del **Tejo**, deporte nacional de Colombia. El proyecto recrea la experiencia auténtica del juego tradicional colombiano con:

- **Vista lateral** estilo Angry Birds para una perspectiva intuitiva
- **Control manual** con teclado para lanzamiento preciso
- **Física realista** usando PyBullet (mayor fuerza = mayor distancia y rotación)
- **Sistema de puntuación oficial** con mechas, embocinadas, moñonas y mano
- **Efectos de sonido** para mayor inmersión

---

## ✨ Características Principales

### Sistema de Puntuación Oficial del Tejo

| Figura | Puntos | Descripción |
|--------|--------|-------------|
| **Mecha** | 3 | El tejo golpea el bocín y la mecha explota (20% probabilidad) |
| **Embocinada** | 6 | El tejo queda parado dentro del bocín |
| **Moñona** | 9 | Embocinada + Mecha en el mismo lanzamiento |
| **Mano** | 1 | Tejo más cercano al bocín al final del turno |

### Mecánica de Juego

- **Partidas a 27 puntos** - El primer equipo en alcanzar 27 puntos gana
- **Rondas de 6 turnos** - Cada equipo lanza 6 tejos por ronda
- **Turnos alternados** - Los equipos se alternan en cada lanzamiento
- **Suspensión por figura** - Si se logra una figura, se suspende la ronda

### Física Realista

- Trayectorias parabólicas calculadas con PyBullet
- Detección de colisiones con el bocín
- Análisis de orientación del tejo (parado/acostado) usando quaterniones
- Fricción y rebotes realistas en el tablero de arcilla

### Visualización 3D

- Tablero inclinado a 45° con textura de arcilla
- Bocín (disco blanco) en el centro del tablero
- Tejos de colores por equipo (rojo para A, verde para B)
- Mechas amarillas distribuidas alrededor del bocín
- Interfaz con barras de fuerza y ángulo

---

## 🎮 Manual de Usuario

### Controles del Juego

| Tecla | Acción |
|-------|--------|
| **W** | Aumentar fuerza (+5%) |
| **S** | Disminuir fuerza (-5%) |
| **↑ (Flecha Arriba)** | Aumentar ángulo (+5°) |
| **↓ (Flecha Abajo)** | Disminuir ángulo (-5°) |
| **ESPACIO** | Lanzar el tejo |
| **R** | Reiniciar juego |
| **ESC** | Salir del juego |

### Cómo Jugar

1. **Inicio del juego**
   - El juego comienza automáticamente con el Equipo A (rojo)
   - Cada equipo tiene 6 tejos por ronda

2. **Ajustar el lanzamiento**
   - Usa **W/S** para ajustar la fuerza (50% - 100%)
   - Usa las **flechas ↑/↓** para ajustar el ángulo (20° - 70°)
   - Mayor fuerza = mayor distancia y rotación del tejo

3. **Lanzar**
   - Presiona **ESPACIO** para lanzar el tejo
   - Observa la trayectoria y espera a que el tejo se detenga

4. **Puntuación**
   - El sistema calcula automáticamente los puntos según:
     - Si golpeó el bocín (posibilidad de mecha)
     - Si quedó parado (embocinada)
     - Combinación de ambos (moñona)
   - Al final de cada par de lanzamientos, el tejo más cercano al bocín gana 1 punto (mano)

5. **Cambio de turno**
   - Después de cada lanzamiento, el turno pasa al otro equipo
   - Si se logra una figura, la ronda termina y el equipo que la logró comienza la siguiente

6. **Victoria**
   - El primer equipo en alcanzar **27 puntos** gana la partida

### Indicadores en Pantalla

- **Panel Superior:** Muestra los puntajes de ambos equipos y el turno actual
- **Panel Inferior:** Muestra la fuerza y el ángulo actuales
- **Consola:** Información detallada de cada lanzamiento y puntuación

---

## 🚀 Manual de Instalación

### Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, Linux o macOS
- **Python:** 3.10, 3.11 o 3.12
- **RAM:** 4 GB mínimo
- **GPU:** Tarjeta gráfica con soporte OpenGL 3.3+
- **Windows:** Microsoft Visual C++ Build Tools (para PyBullet)

### Paso 1: Clonar el Repositorio

```bash
git clone https://github.com/AbelAlbuez/computer-graphics.git
cd computer-graphics/tejo-game
```

### Paso 2: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate

# En Linux/macOS:
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el Juego

```bash
python TejoGame.py
```

### Dependencias Principales

| Biblioteca | Versión | Propósito |
|------------|---------|-----------|
| ogre-python | 14.4.1 | Motor de renderizado 3D |
| pybullet | 3.x | Simulación de física |
| vtk | ≥9.0.0 | Generación de geometrías |
| pygame | ≥2.6.0 | Sistema de audio |
| imgui | ≥2.0.0 | Interfaz de usuario |
| PyOpenGL | ≥3.1.0 | Renderizado OpenGL |
| numpy | - | Cálculos numéricos |

---

## 📁 Estructura del Proyecto

```
tejo-game/
│
├── TejoGame.py                # Código principal del juego
├── requirements.txt           # Dependencias del proyecto
├── resources.cfg              # Configuración de recursos Ogre3D
├── README.md                  # Este archivo
│
├── game/
│   ├── __init__.py           # Inicialización del módulo
│   ├── constants.py          # Constantes del juego (física, puntuación)
│   ├── game_state.py         # Estado del juego, rondas, turnos
│   ├── physics_engine.py     # Motor de física con PyBullet
│   ├── scoring_system.py     # Sistema de puntuación del tejo
│   ├── ui_imgui.py           # Sistema de UI con Dear ImGui
│   ├── ui_trays.py           # Sistema de UI alternativo (TrayManager)
│   ├── ui_system.py          # Sistema de UI con billboards
│   ├── renderer.py           # Renderizado de objetos 3D
│   ├── game_objects.py       # Geometrías 3D (placeholder)
│   └── input_system.py       # Sistema de input (placeholder)
│
├── lib/
│   └── PUJ_Ogre/             # Biblioteca base Ogre3D del profesor
│       ├── __init__.py
│       ├── BaseApplication.py
│       ├── BaseApplicationWithVTK.py
│       └── BaseListener.py
│
└── resources/
    ├── all.material          # Definición de materiales (colores)
    ├── ground.jpg            # Textura del suelo
    ├── terreno.jpg           # Textura de arcilla (opcional)
    ├── tablero.png           # Textura del tablero (opcional)
    ├── explosion-fx.mp3      # Sonido de explosión de mecha
    ├── win.mp3               # Sonido de victoria
    ├── Embocinada.mp3        # Sonido de embocinada
    ├── Moñona.mp3            # Sonido de moñona
    └── splat.mp3             # Sonido de impacto con tablero
```

---

## ⚙️ Configuración y Personalización

### Constantes de Física (`game/constants.py`)

```python
# Propiedades del Tejo
TEJO_MASS = 0.68              # Masa en kg
TEJO_RADIUS = 0.03            # Radio en metros
TEJO_HEIGHT = 0.01            # Altura en metros
TEJO_FRICTION = 0.7           # Coeficiente de fricción
TEJO_RESTITUTION = 0.3        # Coeficiente de rebote
TEJO_SPIN_FACTOR = 12.0       # Factor de rotación

# Propiedades del Tablero
BOARD_LENGTH = 2.5            # Longitud en metros
BOARD_WIDTH = 1.0             # Ancho en metros
BOARD_ANGLE = 45              # Inclinación en grados
BOARD_FRICTION = 10.0         # Fricción alta para frenar tejos

# Configuración del Juego
TEJOS_PER_TEAM = 6            # Tejos por ronda por equipo
NUM_TEAMS = 2                 # Número de equipos
WINNING_SCORE = 27            # Puntos para ganar

# Física General
GRAVITY = -9.8                # Gravedad (m/s²)
```

### Ajustar Dificultad

Para modificar la dificultad del juego, puedes ajustar:

- **TEJO_SPIN_FACTOR:** Mayor valor = más rotación del tejo
- **BOARD_FRICTION:** Mayor valor = el tejo se detiene más rápido
- **Probabilidad de mecha:** En `scoring_system.py`, método `roll_explosion()` (actualmente 20%)

---

## 🐛 Solución de Problemas

### Error: "Microsoft Visual C++ required" (Windows)

**Problema:** PyBullet requiere compilación en Windows.

**Solución:**
1. Descargar [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instalar "Desarrollo para el escritorio con C++"
3. Reiniciar la terminal
4. Ejecutar: `pip install pybullet`

### No se escuchan los efectos de sonido

**Problema:** Archivos de audio no encontrados.

**Solución:** 
- Verificar que existen los archivos `.mp3` en la carpeta `resources/`
- El juego funciona sin audio si no se encuentran los archivos

### Los tejos no se detienen

**Problema:** El sistema no detecta cuando el tejo está quieto.

**Solución:**
- Verificar que PyBullet está instalado correctamente
- El umbral de velocidad es 0.1 m/s (configurable en `physics_engine.py`)

### Pantalla negra al iniciar

**Problema:** Los recursos de Ogre3D no se cargan.

**Solución:**
- Verificar que `resources.cfg` apunta correctamente a la carpeta `resources/`
- Asegurar que los materiales en `all.material` están correctos

### ImGui no se muestra

**Problema:** La interfaz de usuario no aparece.

**Solución:**
- Verificar que `imgui` y `PyOpenGL` están instalados
- El juego imprime información en la consola como respaldo

---

## 🎓 Aspectos Técnicos Destacados

### Detección de Embocinada

El sistema usa análisis de quaterniones para determinar si el tejo quedó "parado":

```python
def _check_tejo_standing(self, orientation):
    x, y, z, w = orientation
    up_y = 1 - 2 * (x*x + z*z)
    return up_y > 0.7  # Tolerancia de verticalidad
```

### Sistema de Rondas

- Contador independiente `current_round_throws` para cada ronda
- Sistema `players_pending` para gestionar el orden de jugadores
- Suspensión automática al detectar una figura
- Partidas sin límite de rondas hasta alcanzar 27 puntos

### Sincronización Física-Gráficos

- PyBullet calcula la física en cada frame
- Las transformaciones (posición, rotación) se aplican a los nodos de Ogre3D
- Detección de tejos detenidos usando umbral de velocidad

---

## 📊 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| Ogre3D | 14.4.1 | Motor de renderizado 3D |
| PyBullet | 3.x | Simulación de física |
| VTK | 9.0+ | Generación de geometrías 3D |
| pygame | 2.6+ | Sistema de audio |
| Dear ImGui | 2.0+ | Interfaz de usuario |
| OpenGL | 3.3+ | API gráfica |

---

## ✅ Características Implementadas

- [x] Sistema de puntuación completo (mecha, embocinada, moñona, mano)
- [x] Rondas con suspensión automática por figuras
- [x] Partidas a 27 puntos sin límite de rondas
- [x] Turnos alternados entre equipos
- [x] Física realista con PyBullet
- [x] Interfaz de usuario con Dear ImGui
- [x] Efectos de sonido (explosión, victoria, embocinada, moñona)
- [x] Sistema de reinicio (tecla R)
- [x] Detección de orientación del tejo
- [x] Punto de mano por proximidad al bocín
- [x] Tablero inclinado a 45 grados
- [x] Geometrías 3D para tejos, bocín y mechas

---

## 📝 Reglas Oficiales del Tejo

El tejo es un deporte tradicional colombiano declarado patrimonio cultural de la nación. Las reglas implementadas en este simulador siguen los lineamientos oficiales:

1. **Objetivo:** Lanzar el tejo (disco metálico) para hacerlo caer lo más cerca posible del bocín o hacer explotar las mechas.

2. **Cancha:** Tablero de arcilla inclinado con un bocín metálico en el centro rodeado de mechas explosivas.

3. **Puntuación:**
   - Mecha (3 pts): El tejo golpea el bocín y una mecha explota
   - Embocinada (6 pts): El tejo queda parado dentro del bocín
   - Moñona (9 pts): Embocinada con mecha
   - Mano (1 pt): Tejo más cercano al bocín sin figura

4. **Victoria:** Primer equipo en alcanzar 27 puntos.

---

## 🔗 Enlaces

- **Repositorio:** [GitHub - computer-graphics](https://github.com/AbelAlbuez/computer-graphics)
- **Documentación Ogre3D:** [ogre3d.org](https://www.ogre3d.org/documentation/)
- **Documentación PyBullet:** [pybullet.org](https://pybullet.org/)
- **Historia del Tejo:** [Wikipedia](https://es.wikipedia.org/wiki/Tejo_(deporte))

---

## 📄 Licencia

Este proyecto se desarrolla con fines educativos para el curso de Computación Gráfica de la Pontificia Universidad Javeriana.

---

**Versión:** 2.0  
**Última actualización:** Noviembre 2025