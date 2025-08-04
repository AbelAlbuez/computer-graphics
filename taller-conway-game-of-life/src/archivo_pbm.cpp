// =========================================================================
// @author Abel Albuez
// =========================================================================

#include "archivo_pbm.h"
#include <fstream>
#include <iostream>
#include <sstream>

// Función auxiliar para saltar comentarios
static void saltarComentarios(std::ifstream &archivo)
{
    char c;
    while (archivo >> std::ws)
    {
        c = archivo.peek();
        if (c == '#')
        {
            std::string linea;
            std::getline(archivo, linea);
        }
        else
        {
            break;
        }
    }
}

// Leer un archivo PBM y convertirlo a Tablero
Tablero ArchivoPBM::leer(const std::string &nombre_archivo)
{
    std::ifstream archivo(nombre_archivo);

    if (!archivo.is_open())
    {
        std::cerr << "Error: No se puede abrir el archivo " << nombre_archivo << std::endl;
        return Tablero(0, 0);
    }

    // Leer el "número mágico" (debe ser P1)
    std::string magic;
    archivo >> magic;

    if (magic != "P1")
    {
        std::cerr << "Error: El archivo no es formato PBM P1" << std::endl;
        archivo.close();
        return Tablero(0, 0);
    }

    saltarComentarios(archivo);

    int ancho, alto;
    archivo >> ancho >> alto;

    if (ancho <= 0 || alto <= 0)
    {
        std::cerr << "Error: Dimensiones inválidas" << std::endl;
        archivo.close();
        return Tablero(0, 0);
    }

    Tablero tablero(ancho, alto);

    for (int y = 0; y < alto; y++)
    {
        for (int x = 0; x < ancho; x++)
        {
            int valor;
            archivo >> valor;

            if (archivo.fail())
            {
                std::cerr << "Error: Datos incompletos en el archivo" << std::endl;
                return Tablero(0, 0);
            }

            tablero.establecer(x, y, valor == 1);
        }
    }

    archivo.close();
    std::cout << "Archivo leído: " << nombre_archivo
              << " (" << ancho << "x" << alto << ")" << std::endl;
    return tablero;
}

// Escribir un Tablero como archivo PBM
void ArchivoPBM::escribir(const std::string &nombre_archivo, const Tablero &tablero)
{
    std::ofstream archivo(nombre_archivo);

    if (!archivo.is_open())
    {
        std::cerr << "Error: No se puede crear el archivo " << nombre_archivo << std::endl;
        return;
    }

    archivo << "P1" << std::endl;
    archivo << "# Generado por Juego de la Vida" << std::endl;
    archivo << tablero.obtenerAncho() << " " << tablero.obtenerAlto() << std::endl;

    for (int y = 0; y < tablero.obtenerAlto(); y++)
    {
        for (int x = 0; x < tablero.obtenerAncho(); x++)
        {
            archivo << (tablero.obtener(x, y) ? "1" : "0");

            if (x < tablero.obtenerAncho() - 1)
            {
                archivo << " ";
            }
        }
        archivo << std::endl;
    }

    archivo.close();
    std::cout << "Archivo guardado: " << nombre_archivo << std::endl;
}