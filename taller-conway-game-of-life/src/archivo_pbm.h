#ifndef __ARCHIVO_PBM_H__
#define __ARCHIVO_PBM_H__

#include <string>
#include "tablero.h"

class ArchivoPBM {
public:
    static Tablero leer(const std::string& nombre_archivo);
    
    static void escribir(const std::string& nombre_archivo, const Tablero& tablero);
};

#endif