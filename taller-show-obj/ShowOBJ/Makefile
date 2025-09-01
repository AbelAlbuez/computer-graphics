## ========================================================================
## @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
## ========================================================================

# Detectar el sistema operativo
UNAME_S := $(shell uname -s)

# Configuración del compilador según el sistema
ifeq ($(UNAME_S),Darwin)
    # macOS
    CXX = clang++
    CFLAGS = -std=c++17 -Wall -Wextra -Ilib -Ilib/eigen3 -DGL_SILENCE_DEPRECATION
    LDFLAGS = -framework OpenGL -framework GLUT
else
    # Linux
    CXX = g++
    CFLAGS = -std=c++11 -Wall -Wextra -Ilib -Ilib/eigen3
    LDFLAGS = -lGL -lGLU -lglut
endif

# Archivos fuente
SRC = ShowOBJ.cxx lib/PUJ_GL/BaseApp.cxx lib/PUJ_GL/Mesh.cxx lib/PUJ_GL/Trackball.cxx

# Nombre del ejecutable
TARGET = ShowOBJ

# Regla principal
all: $(TARGET)

# Compilar el ejecutable
$(TARGET): $(SRC)
	$(CXX) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

# Shell para el comando clean
SHELL := /bin/bash

# Limpiar archivos compilados
clean:
	@rm -f $(TARGET)
	@find . -name '*.o' -type f -delete
	@echo "Archivos limpiados"

# Ejecutar con modelo de prueba
run: $(TARGET)
	./$(TARGET) meshes/bunny.obj

# Ayuda
help:
	@echo "Uso del Makefile:"
	@echo "  make        - Compilar el proyecto"
	@echo "  make clean  - Limpiar archivos compilados"
	@echo "  make run    - Compilar y ejecutar con bunny.obj"
	@echo "  make help   - Mostrar esta ayuda"

.PHONY: all clean run help

## eof - Makefile