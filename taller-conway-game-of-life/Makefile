# =========================================================================
# Makefile para el Juego de la Vida
# =========================================================================

# Compilador y flags
CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -O2
LDFLAGS = 

# Directorios
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Nombre del ejecutable
TARGET = $(BIN_DIR)/juego_vida

# Archivos fuente
SOURCES = $(SRC_DIR)/main.cpp \
          $(SRC_DIR)/tablero.cpp \
          $(SRC_DIR)/archivo_pbm.cpp \
          $(SRC_DIR)/juego_vida.cpp \
          $(SRC_DIR)/generador_frames.cpp \
          $(SRC_DIR)/FrameBuffer.cxx

# Archivos objeto
OBJECTS = $(OBJ_DIR)/main.o \
          $(OBJ_DIR)/tablero.o \
          $(OBJ_DIR)/archivo_pbm.o \
          $(OBJ_DIR)/juego_vida.o \
          $(OBJ_DIR)/generador_frames.o \
          $(OBJ_DIR)/FrameBuffer.o

# Headers
HEADERS = $(SRC_DIR)/tablero.h \
          $(SRC_DIR)/archivo_pbm.h \
          $(SRC_DIR)/juego_vida.h \
          $(SRC_DIR)/generador_frames.h \
          $(SRC_DIR)/FrameBuffer.h

# Regla principal
all: directories $(TARGET)

# Crear directorios necesarios
directories:
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(BIN_DIR)

# Compilar el ejecutable
$(TARGET): $(OBJECTS)
	@echo "Enlazando $@..."
	$(CXX) $(OBJECTS) -o $@ $(LDFLAGS)
	@echo "¡Compilación exitosa!"

# Reglas de compilación para cada módulo
$(OBJ_DIR)/main.o: $(SRC_DIR)/main.cpp $(HEADERS)
	@echo "Compilando main.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/tablero.o: $(SRC_DIR)/tablero.cpp $(SRC_DIR)/tablero.h
	@echo "Compilando tablero.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/archivo_pbm.o: $(SRC_DIR)/archivo_pbm.cpp $(SRC_DIR)/archivo_pbm.h $(SRC_DIR)/tablero.h
	@echo "Compilando archivo_pbm.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/juego_vida.o: $(SRC_DIR)/juego_vida.cpp $(SRC_DIR)/juego_vida.h $(SRC_DIR)/tablero.h
	@echo "Compilando juego_vida.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/generador_frames.o: $(SRC_DIR)/generador_frames.cpp $(SRC_DIR)/generador_frames.h \
                                $(SRC_DIR)/tablero.h $(SRC_DIR)/FrameBuffer.h \
                                $(SRC_DIR)/archivo_pbm.h $(SRC_DIR)/juego_vida.h
	@echo "Compilando generador_frames.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/FrameBuffer.o: $(SRC_DIR)/FrameBuffer.cxx $(SRC_DIR)/FrameBuffer.h
	@echo "Compilando FrameBuffer.cxx..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpiar archivos compilados
clean:
	@echo "Limpiando archivos compilados..."
	@rm -rf $(OBJ_DIR)/*.o $(TARGET)
	@echo "¡Limpieza completada!"

# Limpiar todo (incluyendo directorios)
clean-all:
	@echo "Limpiando todo..."
	@rm -rf $(OBJ_DIR) $(BIN_DIR)
	@echo "¡Limpieza completa!"

# Limpiar solo los frames y videos generados
clean-output:
	@echo "Limpiando archivos generados..."
	@rm -rf frames/ gifs/ videos/
	@rm -f *.ppm *.pbm *.gif *.mp4
	@echo "¡Archivos de salida eliminados!"

# Compilar en modo debug
debug: CXXFLAGS += -g -DDEBUG
debug: clean all

# Ejecutar con ejemplo
run: all
	$(TARGET) src/glider.pbm 3.0 10

# Ejecutar prueba rápida
test: all
	@echo "=== Prueba rápida con blinker ==="
	$(TARGET) src/blinker.pbm 0.5 10
	@echo -e "\nFrames generados:"
	@ls -la frames/ | head -10

# Crear video de los frames generados
video:
	@if [ -d "frames" ]; then \
		echo "Creando video..."; \
		mkdir -p videos; \
		ffmpeg -framerate 10 -i frames/frame_%05d.ppm -c:v libx264 -pix_fmt yuv420p videos/output.mp4; \
		echo "Video guardado en videos/output.mp4"; \
	else \
		echo "Error: No hay frames en la carpeta frames/"; \
	fi

# Crear GIF de los frames generados
gif:
	@if [ -d "frames" ]; then \
		echo "Creando GIF animado..."; \
		mkdir -p gifs; \
		convert -delay 10 frames/frame_*.ppm gifs/animation.gif; \
		echo "GIF guardado en gifs/animation.gif"; \
	else \
		echo "Error: No hay frames en la carpeta frames/"; \
	fi

# Instalar (opcional)
install: all
	@echo "Instalando en /usr/local/bin..."
	@sudo cp $(TARGET) /usr/local/bin/
	@echo "¡Instalación completada!"

# Desinstalar (opcional)
uninstall:
	@echo "Desinstalando..."
	@sudo rm -f /usr/local/bin/juego_vida
	@echo "¡Desinstalación completada!"

# Mostrar ayuda
help:
	@echo "Makefile para el Juego de la Vida"
	@echo ""
	@echo "Objetivos disponibles:"
	@echo "  make              - Compilar el proyecto"
	@echo "  make clean        - Limpiar archivos objeto"
	@echo "  make clean-all    - Limpiar todo"
	@echo "  make clean-output - Limpiar frames y videos generados"
	@echo "  make debug        - Compilar en modo debug"
	@echo "  make run          - Compilar y ejecutar ejemplo"
	@echo "  make test         - Ejecutar prueba rápida"
	@echo "  make video        - Crear video MP4 de los frames"
	@echo "  make gif          - Crear GIF animado de los frames"
	@echo "  make help         - Mostrar esta ayuda"
	@echo ""
	@echo "Uso del programa:"
	@echo "  $(TARGET) <archivo.pbm> <duracion> <fps>"

.PHONY: all clean clean-all clean-output debug run test video gif install uninstall help directories