// =========================================================================
// @author Abel Albuez
// =========================================================================

#include "tablero.h"
#include <iostream>

Tablero::Tablero(int ancho, int alto)
    : m_ancho(ancho), m_alto(alto)
{

    m_celulas.resize(alto);

    for (int i = 0; i < alto; i++)
    {
        m_celulas[i].resize(ancho, false);
    }
}

// Obtener el estado de una célula
bool Tablero::obtener(int x, int y) const
{
    if (x >= 0 && x < m_ancho && y >= 0 && y < m_alto)
    {
        return m_celulas[y][x];
    }
    return false;
}

// Establecer el estado de una célula
void Tablero::establecer(int x, int y, bool valor)
{
    if (x >= 0 && x < m_ancho && y >= 0 && y < m_alto)
    {
        m_celulas[y][x] = valor;
    }
}

// Mostrar el tablero en consola
void Tablero::mostrar() const
{
    std::cout << "Tablero " << m_ancho << "x" << m_alto << ":\n";

    std::cout << "+";
    for (int x = 0; x < m_ancho; ++x)
    {
        std::cout << "-";
    }
    std::cout << "+\n";

    for (int y = 0; y < m_alto; ++y)
    {
        std::cout << "|";
        for (int x = 0; x < m_ancho; ++x)
        {
            std::cout << (m_celulas[y][x] ? "*" : " ");
        }
        std::cout << "|\n";
    }

    std::cout << "+";
    for (int x = 0; x < m_ancho; ++x)
    {
        std::cout << "-";
    }
    std::cout << "+\n";
}

Tablero Tablero::clonar() const
{
    Tablero copia(m_ancho, m_alto);

    for (int y = 0; y < m_alto; y++)
    {
        for (int x = 0; x < m_ancho; x++)
        {
            copia.m_celulas[y][x] = m_celulas[y][x];
        }
    }

    return copia;
}
