#!/bin/bash
# Script de compilación para ShowOBJ

# Detectar el sistema operativo
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Compilando para macOS..."
    clang++ -std=c++17 \
        ShowOBJ.cxx \
        lib/PUJ_GL/BaseApp.cxx \
        lib/PUJ_GL/Mesh.cxx \
        lib/PUJ_GL/Trackball.cxx \
        -Ilib -Ilib/eigen3 \
        -DGL_SILENCE_DEPRECATION \
        -framework OpenGL -framework GLUT \
        -o ShowOBJ
else
    # Linux
    echo "Compilando para Linux..."
    g++ -std=c++11 \
        ShowOBJ.cxx \
        lib/PUJ_GL/BaseApp.cxx \
        lib/PUJ_GL/Mesh.cxx \
        lib/PUJ_GL/Trackball.cxx \
        -Ilib -I/usr/include/eigen3 \
        -lGL -lGLU -lglut \
        -o ShowOBJ
fi

if [ $? -eq 0 ]; then
    echo "Compilación exitosa!"
    echo "Ejecuta: ./run.sh meshes/bunny.obj"
else
    echo "Error en la compilación"
    exit 1
fi