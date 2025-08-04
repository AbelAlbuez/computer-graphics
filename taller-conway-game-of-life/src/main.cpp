// =========================================================================
// @author Abel Albuez
// =========================================================================

#include <iostream>
#include <string>
#include <cstdlib>
#include <exception>

// Incluir nuestros módulos
#include "tablero.h"
#include "archivo_pbm.h"
// TODO: #include "juego_vida.h"
// TODO: #include "generador_frames.h"
// TODO: #include "utilidades.h"

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
        // ACTUALIZADO: Ahora podemos leer archivos PBM reales!
        std::cout << "\n=== Leyendo archivo PBM ===" << std::endl;

        // Leer el archivo PBM
        Tablero tablero_inicial = ArchivoPBM::leer(archivo_entrada);

        // Verificar si se leyó correctamente
        if (tablero_inicial.obtenerAncho() == 0 || tablero_inicial.obtenerAlto() == 0)
        {
            std::cerr << "Error: No se pudo leer el archivo PBM" << std::endl;
            return EXIT_FAILURE;
        }

        // Mostrar información del tablero
        std::cout << "Tablero cargado: "
                  << tablero_inicial.obtenerAncho() << "x"
                  << tablero_inicial.obtenerAlto() << std::endl;

        // Contar células vivas
        int celulas_vivas = 0;
        for (int y = 0; y < tablero_inicial.obtenerAlto(); y++)
        {
            for (int x = 0; x < tablero_inicial.obtenerAncho(); x++)
            {
                if (tablero_inicial.obtener(x, y))
                {
                    celulas_vivas++;
                }
            }
        }
        std::cout << "Células vivas: " << celulas_vivas << std::endl;

        // Si el tablero es pequeño, mostrarlo
        if (tablero_inicial.obtenerAncho() <= 20 && tablero_inicial.obtenerAlto() <= 20)
        {
            std::cout << "\nVisualizando tablero inicial:" << std::endl;
            tablero_inicial.mostrar();
        }

        // Probar escritura
        std::cout << "\n=== Prueba de escritura ===" << std::endl;
        ArchivoPBM::escribir("test_output.pbm", tablero_inicial);

        // TODO: Cuando tengamos los otros módulos
        std::cout << "\n[NOTA] Juego de Vida y Generador de Frames pendientes" << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cerr << "Error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }
    return EXIT_SUCCESS;
}