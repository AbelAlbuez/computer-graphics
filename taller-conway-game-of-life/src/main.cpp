// =========================================================================
// @author Abel Albuez
// =========================================================================

#include <iostream>
#include <string>
#include <cstdlib>


// TODO: Incluir nuestros módulos cuando estén listos
// #include "tablero.h"
// #include "archivo_pbm.h"
// #include "juego_vida.h"
// #include "generador_frames.h"
// #include "utilidades.h"

void mostrarAyuda(const std::string &nombre_programa)
{
    std::cout << "\n";
    std::cout << "========================================\n";
    std::cout << "     JUEGO DE LA VIDA DE CONWAY\n";
    std::cout << "      Generador de Animaciones\n";
    std::cout << "========================================\n";
    std::cout << "\nUso: " << nombre_programa << " <archivo.pbm> <duracion> <fps>\n\n";
    std::cout << "Parámetros:\n";
    std::cout << "  archivo.pbm  : Archivo PBM con la configuración inicial\n";
    std::cout << "  duracion     : Duración de la animación en segundos\n";
    std::cout << "  fps          : Cuadros por segundo\n\n";
    std::cout << "Ejemplo:\n";
    std::cout << "  " << nombre_programa << " glider.pbm 5.0 30\n\n";
}

int main(int argc, char *argv[])
{
    if (argc == 2)
    {
        std::string arg = argv[1];
        if (arg == "--help" || arg == "-h")
        {
            mostrarAyuda(argv[0]);
            return EXIT_SUCCESS;
        }
    }

    if (argc != 4)
    {
        std::cerr << "Error: Número incorrecto de argumentos" << std::endl;
        std::cerr << "Use '" << argv[0] << " --help' para más información." << std::endl;
        return EXIT_FAILURE;
    }

    std::string archivo_entrada;
    float duracion;
    int fps;

    archivo_entrada = argv[1];

    try
    {
        duracion = std::stof(argv[2]);
    }
    catch (...)
    {
        std::cerr << "Error: La duración debe ser un número válido" << std::endl;
        return EXIT_FAILURE;
    }

    try
    {
        fps = std::stoi(argv[3]);
    }
    catch (...)
    {
        std::cerr << "Error: Los FPS deben ser un número entero válido" << std::endl;
        return EXIT_FAILURE;
    }

    if (duracion <= 0 || fps <= 0)
    {
        std::cerr << "Error: La duración y los FPS deben ser mayores que cero" << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "=== Parámetros ===" << std::endl;
    std::cout << "Archivo: " << archivo_entrada << std::endl;
    std::cout << "Duración: " << duracion << " segundos" << std::endl;
    std::cout << "FPS: " << fps << std::endl;
    std::cout << "Total frames a generar: " << (int)(duracion * fps) << std::endl;

    try
    {
        // TODO: Paso 1 - Leer archivo PBM inicial
        std::cout << "\n1. Leyendo archivo: " << archivo_entrada << "..." << std::endl;
        // Tablero tablero_inicial = ArchivoPBM::leer(archivo_entrada);

        // TODO: Paso 2 - Mostrar información del tablero
        std::cout << "2. Tablero cargado (simulado)" << std::endl;
        // std::cout << "Dimensiones: " << tablero.obtenerAncho() << "x" << tablero.obtenerAlto() << std::endl;

        // TODO: Paso 3 - Generar frames
        std::cout << "3. Generando frames..." << std::endl;
        // GeneradorFrames generador;
        // generador.generar(tablero_inicial, duracion, fps);

        // Mensaje final
        std::cout << "\n=== Proceso Completado ===" << std::endl;
        std::cout << "Para crear un video, ejecute:" << std::endl;
        std::cout << "ffmpeg -framerate " << fps << " -i frame_%05d.pbm output.mp4" << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}