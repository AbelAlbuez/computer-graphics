# Taller 5 - Simulador de Caída Libre
## Gráficos por Computador

**Integrantes:**
- Abel Albuez
- Ricardo Rivas

**Profesor:** Leonardo Florez-Valencia  
**Institución:** Pontificia Universidad Javeriana

---

## 📋 Descripción

Simulador de física en tiempo real que genera esferas de manera aleatoria e infinita que caen sobre un plano configurable. El proyecto integra Ogre3D para renderizado 3D y PyBullet para simulación física realista.

---

## ✨ Características

- 🎲 Generación aleatoria de esferas
- ♾️ Caída infinita de esferas
- 🌈 Cuatro materiales diferentes (rojo, verde, amarillo, blanco)
- ⚡ Física realista con PyBullet (gravedad, colisiones, rebotes)
- 🎮 Plano configurable por el usuario
- 📊 Sincronización frame-a-frame entre física y gráficos

---

## 🎯 Requisitos del Taller

| Requisito | Estado |
|-----------|--------|
| Generar esferas aleatoriamente | ✅ |
| Caída libre sobre un plano | ✅ |
| Plano definido por usuario | ✅ |

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
cd computer-graphics/moving-sphere-sample
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

> **Nota para Windows:** Si PyBullet falla, instalar [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/) y seleccionar "Desarrollo para el escritorio con C++"

5. **Ejecutar**
```bash
python MovingSpheres.py
```

---

## ⚙️ Configuración

Edita los parámetros en `MovingSpheres.py`:

```python
altura_caida = 3.0                           # Altura desde donde caen (metros)
tiempo_entre_esferas = 0.5                   # Intervalo entre esferas (segundos)
limites_plano = [ -3.00, 3.00, -3.00, 3.00 ] # Tamaño del plano [x_min, x_max, z_min, z_max]
```

---

## 🎮 Controles

| Acción | Control |
|--------|---------|
| Rotar cámara | Click izquierdo + Arrastrar |
| Zoom | Rueda del ratón |
| Pan (mover) | Click medio + Arrastrar |
| Salir | ESC |

---

## 📁 Estructura del Proyecto

```
moving-sphere-sample/
│
├── MovingSpheres.py          # Código principal del simulador
├── requirements.txt          # Dependencias del proyecto
├── resources.cfg             # Configuración de recursos Ogre3D
├── BITACORA_SIMPLE.md        # Bitácora de desarrollo
├── CAMBIOS_MINIMOS.md        # Documentación de cambios
├── README.md                 # Este archivo
│
├── lib/
│   └── PUJ_Ogre/             # Biblioteca base Ogre3D
│       ├── __init__.py
│       ├── BaseApplication.py
│       ├── BaseApplicationWithVTK.py
│       └── BaseListener.py
│
└── resources/
    ├── all.material          # Definiciones de materiales
    └── ground.jpg            # Textura del plano
```

---

## 🔧 Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.10+ | Lenguaje principal |
| Ogre3D | 14.4.1 | Renderizado 3D |
| PyBullet | 3.x | Motor de física |
| VTK | 9.0+ | Generación de geometría |

---

## 🐛 Solución de Problemas

### Error: "Microsoft Visual C++ required" (Windows)
**Solución:**
1. Descargar [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Instalar "Desarrollo para el escritorio con C++"
3. Reiniciar terminal
4. Ejecutar: `pip install pybullet`

### Error: "Cannot locate resource OgreUnifiedShader.h"
**Solución:** El archivo `resources.cfg` ya incluye la configuración correcta. Verificar que existe la carpeta `venv/Media/`.

### Las esferas caen fuera del plano
**Solución:** Verificar que el parámetro `limites_plano` se usa correctamente en la línea que crea el plano visual.

---

## 📚 Documentación

- **[BITACORA_SIMPLE.md](BITACORA_SIMPLE.md)** - Proceso completo de desarrollo, problemas encontrados y aprendizajes
- **[CAMBIOS_MINIMOS.md](CAMBIOS_MINIMOS.md)** - Explicación detallada de los cambios realizados al código base

---

## 🎓 Aprendizajes Clave

Durante el desarrollo de este taller identificamos la progresión en la abstracción de tecnologías:

- **VTK:** Control total del pipeline gráfico (geometría, normales, renderizado)
- **Ogre3D:** Abstracción del renderizado, enfoque en escena y objetos
- **PyBullet:** Abstracción completa de física, solo definimos propiedades

Esta separación permite que cada sistema haga lo que mejor sabe hacer: PyBullet calcula física precisa con formas simplificadas, mientras Ogre renderiza geometría detallada.

---

## 📝 Cambios Principales

1. ✅ Agregados parámetros configurables
2. ✅ Plano ahora usa `self.limites_plano`
3. ✅ Método `_generarEsfera()` con posiciones aleatorias
4. ✅ Generación infinita (eliminado límite de esferas)
5. ✅ Eliminada esfera predefinida
6. ✅ Ajustes de cámara y física

**Total:** ~30 líneas modificadas/agregadas al código base

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

---

**Fecha de entrega:** Noviembre 2025  
**Versión:** 1.0