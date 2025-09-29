# 🖼️ Taller 3 – Bump Mapping en Superficies Paramétricas

## 📌 Descripción del Proyecto

Este proyecto implementa un sistema interactivo en **C++ con OpenGL** para experimentar con **bump mapping**.
El objetivo es simular relieve sobre un **plano paramétrico** usando una imagen en formato `.ppm`, sin alterar la geometría de la superficie.

### 🎯 Características principales

* Generación de superficies paramétricas (plano, con experimentos en cilindro, esfera, elipsoide y toroide).
* Implementación de bump mapping: perturbación de las normales a partir de gradientes de la imagen.
* Iluminación dinámica con componentes ambiente, difusa y especular.
* Sistema interactivo con controles por teclado.

---

## ⚙️ Requisitos

Antes de compilar el proyecto, asegúrate de tener instaladas las siguientes dependencias:

* [CMake](https://cmake.org/)
* [Make](https://www.gnu.org/software/make/)
* [Eigen3](https://eigen.tuxfamily.org/)
* OpenGL (incluido en macOS y disponible en la mayoría de sistemas Linux)

En macOS se pueden instalar con:

```bash
brew install cmake make eigen
```

---

## 🛠️ Compilación y ejecución

El proyecto incluye un script de ayuda: `build_and_run.sh`.

### 🔹 Paso 1 – Dar permisos de ejecución

```bash
chmod +x build_and_run.sh
```

### 🔹 Paso 2 – Compilar y ejecutar

Ejecuta el script desde la raíz del proyecto:

```bash
./build_and_run.sh
```

El script:

1. Verifica dependencias.
2. Elimina builds anteriores.
3. Configura el proyecto con CMake.
4. Compila el código.
5. Genera el ejecutable `PUJ_GL_ShowParametricModel`.
6. Pregunta si quieres ejecutar la aplicación automáticamente.

---

## ▶️ Opciones de ejecución

* Ejecutar sin textura:

```bash
./PUJ_GL_ShowParametricModel
```

* Ejecutar con textura (`.ppm`):

```bash
./PUJ_GL_ShowParametricModel ../meshes/texture.ppm
```

* Ejecutar con modelos OBJ:

```bash
./PUJ_GL_ShowParametricModel ../meshes/bunny.obj
./PUJ_GL_ShowParametricModel ../meshes/cube.obj
./PUJ_GL_ShowParametricModel ../meshes/ship.obj
```

---

## 🎮 Controles de la aplicación

* `+ / -` → Aumentar/disminuir fuerza del relieve.
* `S` → Activar/desactivar suavizado.
* `L` → Rotar la luz alrededor de la superficie.
* `R` → Resetear la cámara.
* Flechas → Rotar la vista.
* Scroll / rueda del mouse → Zoom in/out.

---

## 📖 Aprendizajes clave

* Las **superficies paramétricas** muestran cómo los rangos y ángulos influyen en la geometría.
* El **bump mapping depende de la iluminación**: sin luz, las normales no tienen efecto visual.
* El **gradiente entre píxeles vecinos** genera bordes y volumen más realistas que la altura directa.
* El **suavizado** reduce ruido y mejora la calidad visual.
* La **topología** de la superficie (plano, esfera, toroide) afecta la estabilidad del efecto.
