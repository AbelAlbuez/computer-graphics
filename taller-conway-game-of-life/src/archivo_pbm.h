#ifndef ARCHIVO_PBM_H
#define ARCHIVO_PBM_H

#include <string>
#include "Tablero.h"
#include "FrameBuffer.h"

class ArchivoPBM {
public:
    // Valores de píxel en escala de grises (negro = vivo, blanco = muerto)
    static const float PIXEL_VIVO;   // 0.0f
    static const float PIXEL_MUERTO; // 1.0f

    // Lee un archivo PBM (P1) y carga los datos en un tablero
    static bool leer(const std::string& nombreArchivo, Tablero& tablero);

    // Escribe una imagen PBM basada en un tablero usando FrameBuffer
    static bool escribir(const std::string& nombreArchivo, const Tablero& tablero);

private:
    // Verifica si una línea es comentario en formato PBM
    static bool esComentario(const std::string& linea);

    // Elimina espacios y tabulaciones sobrantes
    static std::string limpiarLinea(const std::string& linea);
};

#endif // ARCHIVO_PBM_H
