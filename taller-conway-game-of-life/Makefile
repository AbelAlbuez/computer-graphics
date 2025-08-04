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

# ACTUALIZADO: Incluir archivo_pbm.cpp
SOURCES = $(SRC_DIR)/main.cpp \
          $(SRC_DIR)/tablero.cpp \
          $(SRC_DIR)/archivo_pbm.cpp \
          $(SRC_DIR)/FrameBuffer.cxx

# ACTUALIZADO: Incluir archivo_pbm.o
OBJECTS = $(OBJ_DIR)/main.o \
          $(OBJ_DIR)/tablero.o \
          $(OBJ_DIR)/archivo_pbm.o \
          $(OBJ_DIR)/FrameBuffer.o

# Headers disponibles
HEADERS = $(SRC_DIR)/tablero.h \
          $(SRC_DIR)/archivo_pbm.h \
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

# Reglas específicas para cada archivo
$(OBJ_DIR)/main.o: $(SRC_DIR)/main.cpp $(HEADERS)
	@echo "Compilando main.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/tablero.o: $(SRC_DIR)/tablero.cpp $(SRC_DIR)/tablero.h
	@echo "Compilando tablero.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# NUEVO: Regla para archivo_pbm
$(OBJ_DIR)/archivo_pbm.o: $(SRC_DIR)/archivo_pbm.cpp $(SRC_DIR)/archivo_pbm.h
	@echo "Compilando archivo_pbm.cpp..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(OBJ_DIR)/FrameBuffer.o: $(SRC_DIR)/FrameBuffer.cxx $(SRC_DIR)/FrameBuffer.h
	@echo "Compilando FrameBuffer.cxx..."
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Limpiar archivos compilados
clean:
	@echo "Limpiando archivos compilados..."
	@rm -rf $(OBJ_DIR)/*.o $(TARGET)
	@echo "¡Limpieza completada!"

# Ejecutar
run: all
	$(TARGET) src/ejemplo.pbm 3.0 10

.PHONY: all clean run directories