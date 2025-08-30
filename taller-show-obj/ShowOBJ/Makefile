## ========================================================================
## @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
## ========================================================================

all: PUJ_GL_ShowOBJ

SRCS=lib/PUJ_GL/BaseApp.cxx lib/PUJ_GL/Mesh.cxx ShowOBJ.cxx
OBJS=$(SRCS:.cxx=.o)

CXX=g++
CFLAGS=-std=c++23 -Ilib -I/usr/include/eigen3
LDFLAGS=-lGL -lGLU -lglut

PUJ_GL_ShowOBJ: $(OBJS)
	$(CXX) $^ -o $@ $(LDFLAGS)

%.o: %.cxx
	$(CXX) $(CFLAGS) -c $^ -o $@

clean:
	rm -rf PUJ_GL_ShowOBJ *.o lib/PUJ_GL/*.o

## eof - Makefile