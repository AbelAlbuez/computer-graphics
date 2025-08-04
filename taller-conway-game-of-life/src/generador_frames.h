#ifndef GENERADOR_FRAMES_H
#define GENERADOR_FRAMES_H

#include <string>
#include "Tablero.h"
#include "FrameBuffer.h"

class GeneradorFrames {
public:
    // Constructor: recibe ancho y alto (opcional)
    GeneradorFrames();

    // Guarda un frame a partir del estado actual del tablero
    void guardarFrame(const Tablero& tablero, int numeroFrame);

    // Calcula cuántos frames deben generarse según duración y FPS
    static int calcularNumeroFrames(float duracion, int fps);

    // Muestra barra de progreso en consola
    static void mostrarProgreso(int actual, int total);
};

#endif // GENERADOR_FRAMES_H
