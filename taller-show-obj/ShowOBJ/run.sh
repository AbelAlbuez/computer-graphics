#!/bin/bash
# Script para correr ShowOBJ con un modelo .obj

if [ $# -eq 0 ]; then
  echo "Uso: ./run.sh <archivo.obj>"
  echo "Ejemplos:"
  echo "  ./run.sh meshes/bunny.obj"
  echo "  ./run.sh meshes/cube.obj"
  echo "  ./run.sh meshes/ship.obj"
  exit 1
fi

cd "$(dirname "$0")"

./ShowOBJ "$1"
