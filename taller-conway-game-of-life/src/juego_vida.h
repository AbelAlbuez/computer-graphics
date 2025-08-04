// juego_vida.h
#ifndef __JUEGO_VIDA_H__
#define __JUEGO_VIDA_H__

#include "tablero.h"

class JuegoVida {
public:
    static Tablero evolucionar(const Tablero& tablero_actual);
    
private:
    static int contarVecinos(const Tablero& tablero, int x, int y);
    
    static bool aplicarReglas(bool celula_viva, int num_vecinos);
};

#endif