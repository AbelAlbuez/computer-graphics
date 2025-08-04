// =========================================================================
// @author Ricardo Cruz
// =========================================================================

#ifndef __ARCHIVO_PBM_H__
#define __ARCHIVO_PBM_H__

#include <string>
#include "tablero.h"

class ArchivoPBM {
public:
    static Tablero leer(const std::string& ruta);
    static void escribir(const std::string& ruta, const Tablero& tablero);

    static const float PIXEL_VIVO;
    static const float PIXEL_MUERTO;

private:
    static bool esComentario(const std::string& linea);
    static std::string limpiarLinea(const std::string& linea);
};

#endif
