## ========================================================================
## @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
## ========================================================================

APP=PUJ_GL_ShowOBJ

SRCS=lib/PUJ_GL/BaseApp.cxx lib/PUJ_GL/Mesh.cxx ShowOBJ.cxx
OBJS=$(SRCS:.cxx=.o)

CXX=g++
# Usar flags de C++
CXXSTD=-std=c++23

# Detección simple de plataforma
# - En MSYS2/MinGW64, $(OS) es Windows_NT
# - En Linux, usamos uname
UNAME_S := $(shell uname -s)

ifeq ($(OS),Windows_NT)
  # ---- Windows (MSYS2 / MinGW64) ----
  INC_EIGEN = -I/mingw64/include/eigen3
  LDFLAGS   = -lfreeglut -lopengl32 -lglu32
  BIN       = $(APP).exe
else
  # ---- Linux ----
  INC_EIGEN = -I/usr/include/eigen3
  LDFLAGS   = -lGL -lGLU -lglut
  BIN       = $(APP)
endif

# Includes propios
CXXFLAGS=$(CXXSTD) -Ilib $(INC_EIGEN)

# Regla principal
all: $(BIN)

$(BIN): $(OBJS)
	$(CXX) $(OBJS) -o $@ $(LDFLAGS)

%.o: %.cxx
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -rf $(APP) $(APP).exe *.o lib/PUJ_GL/*.o

## eof - Makefile
