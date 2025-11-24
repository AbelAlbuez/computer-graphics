# Juego de Tejo - Simulador 3D
## Gráficos por Computador

**Integrantes:**
- Abel Albuez
- Ricardo Rivas

**Profesor:** Leonardo Florez-Valencia  
**Institución:** Pontificia Universidad Javeriana

---

## 📋 Descripción

Simulador 3D del **Tejo**, deporte nacional de Colombia. El proyecto integra Ogre3D para renderizado 3D, PyBullet para física realista y pygame para efectos de sonido. El juego implementa las reglas oficiales del tejo incluyendo mechas, embocinadas, moñonas y el sistema de puntos de mano.

---

## ✨ Características

- 🎯 **Sistema de puntuación oficial del tejo:**
  - **Mecha:** 3 puntos (explosión al golpear el bocín, 20% probabilidad)
  - **Embocinada:** 6 puntos (tejo parado dentro del bocín)
  - **Moñona:** 9 puntos (embocinada + mecha)
  - **Mano:** 1 punto (tejo más cercano al bocín por turno)

- 🎮 **Sistema de rondas:**
  - Partidas a 27 puntos
  - Rondas de 6 turnos (12 lanzamientos totales)
  - Rondas ilimitadas hasta alcanzar 27 puntos
  - Suspensión automática de ronda al lograr figura

- ⚡ **Física realista:**
  - Trayectorias parabólicas con PyBullet
  - Detección de colisiones con el bocín
  - Análisis de orientación del tejo (parado/acostado)
  - Fricción y rebotes realistas

- 🎨 **Visualización 3D:**
  - Tablero inclinado a 45°
  - Bocín (disco blanco) en el centro
  - Tejos de colores por equipo (rojo/verde)
  - UI con barras verticales para fuerza y ángulo

- 🔊 **Efectos de sonido:**
  - Explosión cuando estalla una mecha
  - Indicadores visuales (disco rojo al explotar)

---

## 🎯 Reglas del Juego

### Objetivo
Ser el primer equipo en alcanzar **27 puntos**.

### Estructura
- **2 equipos:** Equipo A (rojo) y Equipo B (verde)
- **6 tejos por equipo** por ronda
- Turnos alternados entre equipos

### Puntuación
1. **Mecha (3 puntos):** El tejo golpea el bocín y la mecha explota (20% probabilidad)
2. **Embocinada (6 puntos):** El tejo queda parado dentro del bocín
3. **Moñona (9 puntos):** Embocinada + Mecha en el mismo lanzamiento
4. **Mano (1 punto):** Al final de cada turno, el equipo con el tejo más cercano al bocín

### Dinámica de rondas
- Si se logra una **figura** (mecha/embocinada/moñona):
  - Se suspenden los lanzamientos restantes
  - El equipo que logró la figura lanza primero en la siguiente ronda
  - Los jugadores que no lanzaron van primero en su siguiente turno
- Si no hay figuras, la ronda completa sus 6 turnos

---

## 🚀 Instalación

### Requisitos previos

- Python 3.10, 3.11 o 3.12
- **Windows:** Microsoft Visual C++ Build Tools
- 4 GB RAM mínimo

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/AbelAlbuez/computer-graphics.git
cd computer-graphics/tejo-game
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar**
```bash
python TejoGame.py
```

---

## 🎮 Controles

| Acción | Control |
|--------|---------|
| Aumentar fuerza | W |
| Disminuir fuerza | S |
| Aumentar ángulo | Flecha Arriba ↑ |
| Disminuir ángulo | Flecha Abajo ↓ |
| Lanzar tejo | ESPACIO |
| Reiniciar juego | R |
| Salir | ESC |

### Indicadores UI
- **Barra amarilla (Z=1.5):** Fuerza del lanzamiento (50-100)
- **Barra cian (Z=2.5):** Ángulo del lanzamiento (20-70°)
- **Consola:** Información detallada de puntuación y eventos

---

## 📁 Estructura del Proyecto

```
tejo-game/
│
├── TejoGame.py                # Código principal del juego
├── requirements.txt           # Dependencias del proyecto
├── resources.cfg              # Configuración de recursos Ogre3D
├── readme.md                  # Este archivo
│
├── game/
│   ├── __init__.py
│   ├── constants.py           # Constantes del juego (física, puntuación)
│   ├── game_state.py          # Estado del juego, rondas, turnos
│   ├── physics_engine.py      # Motor de física con PyBullet
│   ├── scoring_system.py      # Sistema de puntuación del tejo
│   ├── ui_system.py           # Sistema de UI (barras, textos)
│   └── renderer.py            # Renderizado de objetos
│
├── lib/
│   └── PUJ_Ogre/              # Biblioteca base Ogre3D
│       ├── __init__.py
│       ├── BaseApplication.py
│       ├── BaseApplicationWithVTK.py
│       └── BaseListener.py
│
└── resources/
    ├── all.material           # Materiales (colores tejos, bocín)
    └── explosion-fx.mp3       # Sonido de explosión (opcional)
```

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| Ogre3D | 14.4.1 | Renderizado 3D |
| PyBullet | 3.x | Motor de física |
| pygame | 2.6+ | Sistema de audio |
| VTK | 9.0+ | Generación de geometría |

---

## ⚙️ Configuración

Los parámetros del juego se pueden ajustar en `game/constants.py`:

```python
# Física del tejo
TEJO_MASS = 0.68              # Masa en kg
TEJO_RADIUS = 0.03            # Radio en metros
TEJO_FRICTION = 0.7           # Fricción

# Tablero
BOARD_LENGTH = 2.5            # Longitud en metros
BOARD_WIDTH = 1.0             # Ancho en metros
BOARD_ANGLE = 45              # Inclinación en grados

# Juego
TEJOS_PER_TEAM = 6            # Tejos por ronda
WINNING_SCORE = 27            # Puntos para ganar
```

---

## 🐛 Solución de Problemas

### Error: "Microsoft Visual C++ required" (Windows)
**Solución:**
1. Descargar [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instalar "Desarrollo para el escritorio con C++"
3. Reiniciar terminal
4. Ejecutar: `pip install pybullet`

### No se escucha el sonido de explosión
**Solución:** Verificar que existe el archivo `explosion-fx.mp3` en la carpeta `resources/`. El juego funciona sin audio si no se encuentra.

### Los tejos no se detienen
**Solución:** Verificar que PyBullet está instalado correctamente. El sistema detecta automáticamente cuando un tejo se detiene basándose en velocidad lineal y angular.

---

## 🎓 Aspectos Técnicos Destacados

### Sistema de detección de figuras
- **Embocinada:** Usa análisis de quaterniones para determinar si el tejo está vertical (up_y > 0.7)
- **Mecha:** Sistema probabilístico (20%) con detección de colisión por distancia
- **Moñona:** Validación combinada de ambas condiciones

### Gestión de rondas
- Contador independiente `current_round_throws` para cada ronda
- Sistema `players_pending` para orden de jugadores
- Suspensión automática al detectar figura
- Victoria solo al alcanzar 27 puntos (rondas ilimitadas)

### Sincronización física-gráficos
- PyBullet calcula física en cada frame
- Transformaciones aplicadas a nodos Ogre3D
- Detección de tejos detenidos con contador de frames

---

## 📝 Características Implementadas

- ✅ Sistema de puntuación completo (mecha, embocinada, moñona, mano)
- ✅ Rondas con suspensión por figuras
- ✅ Partidas a 27 puntos sin límite de rondas
- ✅ Turnos alternados entre equipos
- ✅ Física realista con PyBullet
- ✅ UI con indicadores visuales
- ✅ Efectos de sonido
- ✅ Sistema de reinicio (tecla R)
- ✅ Detección de orientación del tejo
- ✅ Punto de mano por proximidad al bocín

---

## 📄 Licencia

Este proyecto se desarrolla con fines educativos para el curso de Gráficos por Computador.

---

## 👥 Autores

**Abel Albuez** - [GitHub](https://github.com/AbelAlbuez)  
**Ricardo Rivas**

**Código base:** Leonardo Florez-Valencia (florez-l@javeriana.edu.co)

---

## 🔗 Enlaces

- [Repositorio del curso](https://github.com/AbelAlbuez/computer-graphics)
- [Documentación Ogre3D](https://www.ogre3d.org/documentation/)
- [Documentación PyBullet](https://pybullet.org/)
- [Reglas oficiales del Tejo](https://es.wikipedia.org/wiki/Tejo_(deporte))

---

**Fecha:** Noviembre 2025  
**Versión:** 2.0