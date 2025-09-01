#!/bin/bash
# Script para crear los modelos OBJ de ejemplo

echo "Creando modelos OBJ de ejemplo..."

# Crear directorio si no existe
mkdir -p meshes

# Crear pirámide.obj
cat > meshes/piramide.obj << 'EOF'
# Pirámide de base cuadrada
# Vértices
v 0.0 1.0 0.0      # Vértice superior (punta)
v -1.0 -1.0 1.0    # Base frontal izquierda
v 1.0 -1.0 1.0     # Base frontal derecha
v 1.0 -1.0 -1.0    # Base trasera derecha
v -1.0 -1.0 -1.0   # Base trasera izquierda

# Caras triangulares
# Caras laterales
f 1 2 3
f 1 3 4
f 1 4 5
f 1 5 2

# Base (dos triángulos)
f 2 3 4
f 2 4 5
EOF

# Crear dodecaedro.obj
cat > meshes/dodecaedro.obj << 'EOF'
# Dodecaedro simplificado (12 caras pentagonales)
# Vértices
v 0.0 1.618 0.618
v 0.0 1.618 -0.618
v 0.0 -1.618 0.618
v 0.0 -1.618 -0.618
v 1.618 0.618 0.0
v 1.618 -0.618 0.0
v -1.618 0.618 0.0
v -1.618 -0.618 0.0
v 0.618 0.0 1.618
v -0.618 0.0 1.618
v 0.618 0.0 -1.618
v -0.618 0.0 -1.618
v 1.0 1.0 1.0
v 1.0 1.0 -1.0
v 1.0 -1.0 1.0
v 1.0 -1.0 -1.0
v -1.0 1.0 1.0
v -1.0 1.0 -1.0
v -1.0 -1.0 1.0
v -1.0 -1.0 -1.0

# Caras (pentágonos divididos en triángulos)
# Cara superior
f 1 2 14
f 1 14 13
f 1 13 17

# Cara inferior
f 3 4 16
f 3 16 15
f 3 15 19

# Caras laterales
f 5 6 15
f 5 15 13
f 5 13 14

f 7 8 19
f 7 19 17
f 7 17 18

f 9 10 17
f 9 17 13
f 9 13 15

f 11 12 18
f 11 18 14
f 11 14 16

# Conectar más caras
f 2 11 14
f 2 18 11
f 4 12 16
f 4 20 12

f 6 9 15
f 6 16 9
f 8 10 19
f 8 20 10
EOF

# Crear estrella.obj (simplificada)
cat > meshes/estrella.obj << 'EOF'
# Estrella 3D simple de 4 puntas
# Vértices
v 0.0 0.0 0.0      # Centro

# Puntas principales
v 2.0 0.0 0.0      # Este
v -2.0 0.0 0.0     # Oeste
v 0.0 2.0 0.0      # Arriba
v 0.0 -2.0 0.0     # Abajo
v 0.0 0.0 2.0      # Adelante
v 0.0 0.0 -2.0     # Atrás

# Vértices intermedios
v 0.5 0.5 0.5
v -0.5 0.5 0.5
v 0.5 -0.5 0.5
v -0.5 -0.5 0.5
v 0.5 0.5 -0.5
v -0.5 0.5 -0.5
v 0.5 -0.5 -0.5
v -0.5 -0.5 -0.5

# Caras triangulares
# Conectar centro con puntas a través de intermedios
f 1 8 2
f 1 2 10
f 1 10 5
f 1 5 8

f 1 9 3
f 1 3 11
f 1 11 5
f 1 5 9

f 1 8 4
f 1 4 12
f 1 12 6
f 1 6 8

f 1 10 5
f 1 5 14
f 1 14 7
f 1 7 10

# Caras externas
f 2 8 10
f 3 9 11
f 4 8 12
f 5 10 14
f 6 12 8
f 7 14 10

# Conectar puntas
f 8 9 10
f 10 11 14
f 12 13 14
f 8 12 13
EOF

# Crear torus.obj (simplificado)
cat > meshes/torus.obj << 'EOF'
# Torus (Dona) muy simplificado
# 8 vértices en círculo exterior, 8 en interior

# Círculo exterior
v 3.0 0.0 0.0
v 2.12 0.0 2.12
v 0.0 0.0 3.0
v -2.12 0.0 2.12
v -3.0 0.0 0.0
v -2.12 0.0 -2.12
v 0.0 0.0 -3.0
v 2.12 0.0 -2.12

# Círculo interior
v 1.5 0.5 0.0
v 1.06 0.5 1.06
v 0.0 0.5 1.5
v -1.06 0.5 1.06
v -1.5 0.5 0.0
v -1.06 0.5 -1.06
v 0.0 0.5 -1.5
v 1.06 0.5 -1.06

# Círculo interior inferior
v 1.5 -0.5 0.0
v 1.06 -0.5 1.06
v 0.0 -0.5 1.5
v -1.06 -0.5 1.06
v -1.5 -0.5 0.0
v -1.06 -0.5 -1.06
v 0.0 -0.5 -1.5
v 1.06 -0.5 -1.06

# Conectar los círculos
# Cara superior
f 1 2 10 9
f 2 3 11 10
f 3 4 12 11
f 4 5 13 12
f 5 6 14 13
f 6 7 15 14
f 7 8 16 15
f 8 1 9 16

# Cara inferior
f 17 18 10 9
f 18 19 11 10
f 19 20 12 11
f 20 21 13 12
f 21 22 14 13
f 22 23 15 14
f 23 24 16 15
f 24 17 9 16

# Conectar superior con inferior
f 1 2 18 17
f 2 3 19 18
f 3 4 20 19
f 4 5 21 20
f 5 6 22 21
f 6 7 23 22
f 7 8 24 23
f 8 1 17 24
EOF

echo "✓ Creados 4 modelos OBJ en la carpeta meshes/"
echo ""
echo "Modelos disponibles:"
echo "  - meshes/piramide.obj    (Pirámide simple)"
echo "  - meshes/dodecaedro.obj  (Poliedro de 12 caras)"
echo "  - meshes/estrella.obj    (Estrella 3D)"
echo "  - meshes/torus.obj       (Dona/Toroide)"
echo ""
echo "Para probarlos:"
echo "  ./ShowOBJ meshes/piramide.obj"
echo "  ./ShowOBJ meshes/dodecaedro.obj"
echo "  ./ShowOBJ meshes/estrella.obj"
echo "  ./ShowOBJ meshes/torus.obj"