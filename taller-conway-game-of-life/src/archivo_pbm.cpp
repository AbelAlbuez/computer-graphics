// =========================================================================
// @author Ricardo Cruz
// =========================================================================

#include "archivo_pbm.h"
#include "tablero.h"

#include <fstream>
#include <sstream>
#include <iostream>
#include <stdexcept>

// Constantes útiles si se desea representar visualmente
const float ArchivoPBM::PIXEL_VIVO = 0.0f;
const float ArchivoPBM::PIXEL_MUERTO = 1.0f;

// Verifica si una línea es vacía o un comentario
bool ArchivoPBM::esComentario(const std::string& linea) {
    return linea.empty() || linea[0] == '#';
}

// Elimina comentarios de una línea
std::string ArchivoPBM::limpiarLinea(const std::string& linea) {
    size_t pos = linea.find('#');
    if (pos != std::string::npos) {
        return linea.substr(0, pos);
    }
    return linea;
}

// Lee un archivo PBM en formato P1 y retorna un objeto Tablero
Tablero ArchivoPBM::leer(const std::string& ruta) {
    std::ifstream archivo(ruta);
    if (!archivo.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo: " + ruta);
    }

    std::string linea;
    int ancho = 0, alto = 0;
    bool dimensiones_leidas = false;
    std::vector<bool> datos;

    while (std::getline(archivo, linea)) {
        linea = limpiarLinea(linea);
        if (esComentario(linea)) continue;

        std::istringstream ss(linea);
        if (linea == "P1") {
            continue; // Encabezado válido
        } else if (!dimensiones_leidas) {
            ss >> ancho >> alto;
            if (ancho <= 0 || alto <= 0) {
                throw std::runtime_error("Dimensiones inválidas en el archivo PBM.");
            }
            dimensiones_leidas = true;
        } else {
            int bit;
            while (ss >> bit) {
                datos.push_back(bit == 1); // 1 = vivo, 0 = muerto
            }
        }
    }

    // Validación: cantidad de datos debe coincidir con ancho * alto
    if ((int)datos.size() != ancho * alto) {
        throw std::runtime_error("El número de bits no coincide con el tamaño declarado del archivo PBM.");
    }

    Tablero tablero(ancho, alto);

    // Llenamos el tablero con los valores leídos
    for (int y = 0; y < alto; ++y) {
        for (int x = 0; x < ancho; ++x) {
            tablero.establecer(x, y, datos[y * ancho + x]);
        }
    }

    return tablero;
}

// Escribe un objeto Tablero en un archivo PBM formato P1
void ArchivoPBM::escribir(const std::string& ruta, const Tablero& tablero) {
    std::ofstream archivo(ruta);
    if (!archivo.is_open()) {
        throw std::runtime_error("No se pudo abrir el archivo para escribir: " + ruta);
    }

    archivo << "P1\n";
    archivo << "# Archivo generado automáticamente por archivo_pbm.cpp\n";
    archivo << tablero.obtenerAncho() << " " << tablero.obtenerAlto() << "\n";

    for (int y = 0; y < tablero.obtenerAlto(); ++y) {
        for (int x = 0; x < tablero.obtenerAncho(); ++x) {
            archivo << (tablero.obtener(x, y) ? "1" : "0") << " ";
        }
        archivo << "\n";
    }
}