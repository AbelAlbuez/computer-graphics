#ifndef __TABLERO_H__
#define __TABLERO_H__

#include <vector>

class Tablero {
private:
    int m_ancho;
    int m_alto;
    std::vector<std::vector<bool>> m_celulas;
    
public:
    Tablero(int ancho, int alto);

    int obtenerAncho() const { return m_ancho; }
    int obtenerAlto() const { return m_alto; }

    bool obtener(int x, int y) const;
    void establecer(int x, int y, bool valor);
    void mostrar() const;
    Tablero clonar() const;
};

#endif