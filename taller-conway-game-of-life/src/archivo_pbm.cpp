#include "archivo_pbm.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <cctype>

// Inicialización de valores constantes para píxeles
const float ArchivoPBM::PIXEL_VIVO = 0.0f;   // negro
const float ArchivoPBM::PIXEL_MUERTO = 1.0f; // blanco

// Determino si la línea es un comentario (inicia con # ignorando espacios)
bool ArchivoPBM::esComentario(const std::string& linea) {
    for (char c : linea) {
        if (std::isspace(c)) continue;
        return c == '#';
    }
    return false;
}

// Elimino espacios y tabulaciones del inicio y final de la línea
std::string ArchivoPBM::limpiarLinea(const std::string& linea) {
    size_t inicio = linea.find_first_not_of(" \t");
    size_t fin = linea.find_last_not_of(" \t");
    if (inicio == std::string::npos) return "";
    return linea.substr(inicio, fin - inicio + 1);
}

// Leo un archivo PBM en formato P1 (texto) y cargo el tablero
bool ArchivoPBM::leer(const std::string& nombreArchivo, Tablero& tablero) {
    std::ifstream archivo(nombreArchivo);
    if (!archivo.is_open()) {
        std::cerr << "Error: No se pudo abrir " << nombreArchivo << std::endl;
        return false;
    }

    std::string linea;
    int filas = 0, columnas = 0;

    // Validar encabezado P1
    while (std::getline(archivo, linea)) {
        linea = limpiarLinea(linea);
        if (linea.empty() || esComentario(linea)) continue;

        if (linea != "P1") {
            std::cerr << "Error: Formato PBM inválido. Se esperaba P1" << std::endl;
            return false;
        }
        break;
    }

    // Leer dimensiones
    while (std::getline(archivo, linea)) {
        linea = limpiarLinea(linea);
        if (linea.empty() || esComentario(linea)) continue;

        std::stringstream ss(linea);
        ss >> columnas >> filas;
        break;
    }

    if (filas <= 0 || columnas <= 0) {
        std::cerr << "Error: Dimensiones inválidas en PBM" << std::endl;
        return false;
    }

    tablero.redimensionar(filas, columnas);

    // Leer datos de la imagen
    int i = 0, j = 0;
    while (std::getline(archivo, linea) && i < filas) {
        linea = limpiarLinea(linea);
        if (linea.empty() || esComentario(linea)) continue;

        std::stringstream ss(linea);
        int bit;
        while (ss >> bit) {
            tablero.setCelda(i, j, bit == 0); // 0 = vivo, 1 = muerto
            j++;
            if (j == columnas) {
                j = 0;
                i++;
            }
        }
    }

    return true;
}

// Escribo el tablero como imagen PBM usando FrameBuffer (escala de grises)
bool ArchivoPBM::escribir(const std::string& nombreArchivo, const Tablero& tablero) {
    int filas = tablero.getFilas();
    int columnas = tablero.getColumnas();

    FrameBuffer imagen(FrameBuffer::RGB);
    imagen.allocate(columnas, filas);

    // Pinto cada píxel en gris según si la celda está viva o muerta
    for (int i = 0; i < filas; ++i) {
        for (int j = 0; j < columnas; ++j) {
            bool viva = tablero.getCelda(i, j);
            float color = viva ? PIXEL_VIVO : PIXEL_MUERTO;
            imagen(i, j, 0) = color;
            imagen(i, j, 1) = color;
            imagen(i, j, 2) = color;
        }
    }

    std::ofstream salida(nombreArchivo);
    if (!salida.is_open()) {
        std::cerr << "Error al escribir en " << nombreArchivo << std::endl;
        return false;
    }

    imagen._to_stream(salida);  // Este método debe estar público en FrameBuffer
    salida.close();
    return true;
}