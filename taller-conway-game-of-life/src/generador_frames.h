// =========================================================================
// @author Abel Albuez
// =========================================================================
#ifndef __GENERADOR_FRAMES_H__
#define __GENERADOR_FRAMES_H__

#include <string>
#include "tablero.h"
#include "FrameBuffer.h"

class GeneradorFrames {
private:
    std::string m_prefijo_salida;
    bool m_usar_ppm;
    
    std::string generarNombreArchivo(int numero_frame) const;
    
    void guardarFrame(const Tablero& tablero, int numero_frame);
    
    FrameBuffer tableroAFrameBuffer(const Tablero& tablero) const;
    
    void mostrarProgreso(int actual, int total) const;
    
    bool crearDirectorio(const std::string& nombre) const;
    
    std::string obtenerRutaFrame(int numero_frame) const;
    
public:
    GeneradorFrames(const std::string& prefijo = "frame_", bool usar_ppm = true);
    
    void generar(Tablero& tablero_inicial, float duracion, int fps);

    void generarVisualizadorHTML(int total_frames, int fps, 
                                int ancho_tablero, int alto_tablero) const;
};

#endif // __GENERADOR_FRAMES_H__