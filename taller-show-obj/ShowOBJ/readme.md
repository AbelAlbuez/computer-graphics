# Visualizador OBJ con Trackball

## Autores
- **Leonardo Florez-Valencia** (florez-l@javeriana.edu.co) - Framework base
- **Abel Albuez Sanchez** (aa-albuezs@javeriana.edu.co) - Implementación del Trackball y Zoom
- **Ricardo Crus** (r.cruzs@javeriana.edu.co) - Implementación del Trackball y Zoom

## Descripción
Programa para inspeccionar modelos 3D en formato Wavefront OBJ usando control tipo trackball con el ratón. Implementado en C++ con OpenGL/GLUT.

## Características Principales
- ✅ Control de trackball para rotación intuitiva con el mouse
- ✅ Zoom con rueda del mouse y teclado
- ✅ Pan (desplazamiento) con botón medio del mouse
- ✅ Toggle entre modo wireframe y sólido
- ✅ Normalización y centrado automático de modelos
- ✅ Información en pantalla
- ✅ Arquitectura modular con clase Trackball separada

## Compilación Rápida

### macOS
```bash
make
```

### Linux
```bash
# Instalar dependencias si es necesario
sudo apt-get install freeglut3-dev libeigen3-dev

# Compilar
make
```

## Uso
```bash
./run.sh meshes/bunny.obj
```

## Controles
- **Mouse**: Click izquierdo + arrastrar para rotar
- **Rueda**: Zoom in/out
- **R**: Reset vista
- **+/-**: Zoom alternativo
- **ESC/Q**: Salir

## Archivos Importantes
- `ShowOBJ.cxx` - Aplicación principal
- `lib/PUJ_GL/Trackball.h/cxx` - Implementación del trackball
- `MANUAL_DE_USO.md` - Manual detallado

---
*Proyecto para el curso de Computación Gráfica - Universidad Javeriana*