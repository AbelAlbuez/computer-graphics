#include "generador_frames.h"
#include "archivo_pbm.h"  // Para usar PIXEL_VIVO y MUERTO

#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
#include <cmath>

GeneradorFrames::GeneradorFrames() {
    // No se requiere inicialización específica por ahora
}

void GeneradorFrames::guardarFrame(const Tablero& tablero, int numeroFrame) {
    int filas = tablero.getFilas();
    int columnas = tablero.getColumnas();

    FrameBuffer imagen(FrameBuffer::RGB);
    imagen.allocate(columnas, filas);

    for (int i = 0; i < filas; ++i) {
        for (int j = 0; j < columnas; ++j) {
            bool viva = tablero.getCelda(i, j);
            float valor = viva ? ArchivoPBM::PIXEL_VIVO : ArchivoPBM::PIXEL_MUERTO;

            imagen(i, j, 0) = valor;
            imagen(i, j, 1) = valor;
            imagen(i, j, 2) = valor;
        }
    }

    // Generar nombre tipo frame_00000.pbm
    std::ostringstream nombre;
    nombre << "frame_" << std::setfill('0') << std::setw(5) << numeroFrame << ".pbm";

    std::ofstream archivo(nombre.str());
    if (!archivo.is_open()) {
        std::cerr << "Error al guardar " << nombre.str() << std::endl;
        return;
    }

    imagen._to_stream(archivo);  // FrameBuffer::_to_stream debe ser público
    archivo.close();
}

int GeneradorFrames::calcularNumeroFrames(float duracion, int fps) {
    return static_cast<int>(std::round(duracion * fps));
}

void GeneradorFrames::mostrarProgreso(int actual, int total) {
    int porcentaje = static_cast<int>((float(actual) / total) * 100.0f);
    std::cout << "\rGenerando frames: [" << std::setw(3) << porcentaje << "%] "
              << "(" << actual << "/" << total << ")" << std::flush;
    if (actual == total) std::cout << std::endl;
}