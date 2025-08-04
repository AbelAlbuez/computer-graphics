// =========================================================================
// @author Ricardo Cruz
// =========================================================================

#ifndef __GENERADOR_FRAMES_H__
#define __GENERADOR_FRAMES_H__

#include <string>
#include "tablero.h"
#include "FrameBuffer.h"

class GeneradorFrames {
public:
    static void generarAnimacion(const Tablero& inicial, int total_frames, int fps, const std::string& carpeta_salida);

private:
    static void guardarFrame(const Tablero& tablero, int numero_frame, const std::string& carpeta_salida);
};

#endif