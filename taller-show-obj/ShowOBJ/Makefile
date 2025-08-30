## ========================================================================
## @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
## ========================================================================

CXX = clang++
SRC = ShowOBJ.cxx lib/PUJ_GL/BaseApp.cxx lib/PUJ_GL/Mesh.cxx
CFLAGS = -std=c++17 -Wall -Wextra -Ilib -Ilib/eigen3 -DGL_SILENCE_DEPRECATION
LDFLAGS = -framework OpenGL -framework GLUT

TARGET = ShowOBJ

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)

SHELL := /bin/bash

clean:
	@rm -f $(TARGET)
	@find . -name '*.o' -type f -delete


## eof - Makefile