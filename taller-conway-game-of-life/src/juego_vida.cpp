// =========================================================================
// @author Abel Albuez
// =========================================================================

#include "juego_vida.h"

// Evolucionar el tablero según las reglas de Conway
Tablero JuegoVida::evolucionar(const Tablero& tablero_actual) {
    int ancho = tablero_actual.obtenerAncho();
    int alto = tablero_actual.obtenerAlto();
    
    Tablero nueva_generacion(ancho, alto);
    
    for (int y = 0; y < alto; y++) {
        for (int x = 0; x < ancho; x++) {
            bool celula_viva = tablero_actual.obtener(x, y);
            
            int vecinos = contarVecinos(tablero_actual, x, y);
            
            bool nuevo_estado = aplicarReglas(celula_viva, vecinos);
            
            nueva_generacion.establecer(x, y, nuevo_estado);
        }
    }
    
    return nueva_generacion;
}

int JuegoVida::contarVecinos(const Tablero& tablero, int x, int y) {
    int contador = 0;
    
    // Revisar las 8 células vecinas
    // (-1,-1) (0,-1) (1,-1)
    // (-1, 0) [x,y]  (1, 0)
    // (-1, 1) (0, 1) (1, 1)
    
    for (int dy = -1; dy <= 1; dy++) {
        for (int dx = -1; dx <= 1; dx++) {
            if (dx == 0 && dy == 0) {
                continue;
            }
            
            int vecinoX = x + dx;
            int vecinoY = y + dy;
            
            if (tablero.obtener(vecinoX, vecinoY)) {
                contador++;
            }
        }
    }
    
    return contador;
}

bool JuegoVida::aplicarReglas(bool celula_viva, int num_vecinos) {
    if (celula_viva) {
        return (num_vecinos == 2 || num_vecinos == 3);
    } else {
        return (num_vecinos == 3);
    }
}