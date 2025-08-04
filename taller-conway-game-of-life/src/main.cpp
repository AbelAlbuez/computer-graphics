// =========================================================================
// @author Abel Albuez
// =========================================================================

#include <iostream>
#include <string>
#include <cstdlib>
#include <exception>
#include "tablero.h"
#include "archivo_pbm.h"
#include "juego_vida.h"
#include "generador_frames.h"

// Mostrar mensaje de ayuda del programa
void mostrarAyuda(const std::string& nombre_programa) {
    std::cout << "\n";
    std::cout << "========================================\n";
    std::cout << "     JUEGO DE LA VIDA DE CONWAY\n";
    std::cout << "      Generador de Animaciones\n";
    std::cout << "========================================\n";
    std::cout << "\nUso: " << nombre_programa << " <archivo.pbm> <duracion> <fps>\n\n";
    std::cout << "Parámetros:\n";
    std::cout << "  archivo.pbm  : Archivo PBM con la configuración inicial\n";
    std::cout << "  duracion     : Duración de la animación en segundos (número real)\n";
    std::cout << "  fps          : Cuadros por segundo (número entero)\n\n";
    std::cout << "Ejemplo:\n";
    std::cout << "  " << nombre_programa << " glider.pbm 5.0 30\n";
    std::cout << "  Genera 150 frames (5 segundos a 30 fps) del patrón glider\n\n";
    std::cout << "Notas:\n";
    std::cout << "  - El archivo PBM debe estar en formato P1 (ASCII)\n";
    std::cout << "  - Los frames se guardan como frame_00000.ppm, frame_00001.ppm, etc.\n";
    std::cout << "  - Para crear un video: ffmpeg -framerate 30 -i frame_%05d.ppm video.mp4\n\n";
}

// Programa principal
int main(int argc, char* argv[]) {
    if (argc == 2) {
        std::string arg = argv[1];
        if (arg == "-h" || arg == "--help") {
            mostrarAyuda(argv[0]);
            return EXIT_SUCCESS;
        }
    }
    
    if (argc != 4) {
        std::cerr << "Error: Número incorrecto de argumentos" << std::endl;
        std::cerr << "Use -h o --help para ver la ayuda" << std::endl;
        return EXIT_FAILURE;
    }
    
    std::string archivo_entrada;
    float duracion;
    int fps;
    
    archivo_entrada = argv[1];
    
    try {
        duracion = std::stof(argv[2]);
        fps = std::stoi(argv[3]);
    } catch (const std::exception& e) {
        std::cerr << "Error: Los argumentos numéricos no son válidos" << std::endl;
        std::cerr << "Duración debe ser un número real y FPS un entero" << std::endl;
        return EXIT_FAILURE;
    }
    
    if (duracion <= 0) {
        std::cerr << "Error: La duración debe ser mayor que 0" << std::endl;
        return EXIT_FAILURE;
    }
    
    if (fps <= 0) {
        std::cerr << "Error: Los FPS deben ser mayor que 0" << std::endl;
        return EXIT_FAILURE;
    }
    
    int total_frames = static_cast<int>(duracion * fps);
    
    std::cout << "\n=== Parámetros ===" << std::endl;
    std::cout << "Archivo: " << archivo_entrada << std::endl;
    std::cout << "Duración: " << duracion << " segundos" << std::endl;
    std::cout << "FPS: " << fps << std::endl;
    std::cout << "Total frames a generar: " << total_frames << std::endl;
    
    if (total_frames > 1000) {
        std::cout << "\nADVERTENCIA: Se generarán " << total_frames 
                  << " frames. Esto puede tomar tiempo y espacio en disco." << std::endl;
        std::cout << "¿Desea continuar? (s/n): ";
        char respuesta;
        std::cin >> respuesta;
        if (respuesta != 's' && respuesta != 'S') {
            std::cout << "Operación cancelada." << std::endl;
            return EXIT_SUCCESS;
        }
    }
    
    try {
        std::cout << "\n=== Leyendo archivo PBM ===" << std::endl;
        Tablero tablero_inicial = ArchivoPBM::leer(archivo_entrada);
        
        if (tablero_inicial.obtenerAncho() == 0 || tablero_inicial.obtenerAlto() == 0) {
            std::cerr << "Error: No se pudo leer el archivo PBM o está vacío" << std::endl;
            return EXIT_FAILURE;
        }
        
        std::cout << "Tablero cargado: " 
                  << tablero_inicial.obtenerAncho() << "x" 
                  << tablero_inicial.obtenerAlto() << std::endl;
        
        int celulas_vivas = 0;
        for (int y = 0; y < tablero_inicial.obtenerAlto(); y++) {
            for (int x = 0; x < tablero_inicial.obtenerAncho(); x++) {
                if (tablero_inicial.obtener(x, y)) {
                    celulas_vivas++;
                }
            }
        }
        std::cout << "Células vivas iniciales: " << celulas_vivas << std::endl;
        
        if (tablero_inicial.obtenerAncho() <= 20 && tablero_inicial.obtenerAlto() <= 20) {
            std::cout << "\nEstado inicial:" << std::endl;
            tablero_inicial.mostrar();
        }
        
        std::cout << "\n=== Generando animación ===" << std::endl;
        
        GeneradorFrames generador("frame_");
        generador.generar(tablero_inicial, duracion, fps);
        
        std::cout << "\n=== Proceso Completado ===" << std::endl;
        std::cout << "\nPara crear un video con los frames generados:" << std::endl;
        std::cout << "\n1. Con ffmpeg (recomendado):" << std::endl;
        std::cout << "   ffmpeg -framerate " << fps 
                  << " -i frame_%05d.ppm -c:v libx264 -pix_fmt yuv420p output.mp4" 
                  << std::endl;
        
        std::cout << "\n2. Para un GIF animado (con ImageMagick):" << std::endl;
        std::cout << "   convert -delay " << (100/fps) 
                  << " frame_*.ppm animation.gif" << std::endl;
        
        std::cout << "\n3. Para reproducir directamente (con ffplay):" << std::endl;
        std::cout << "   ffplay -framerate " << fps 
                  << " -i frame_%05d.ppm" << std::endl;
        
    } catch (const std::exception& e) {
        std::cerr << "\nError durante la ejecución: " << e.what() << std::endl;
        return EXIT_FAILURE;
    } catch (...) {
        std::cerr << "\nError desconocido durante la ejecución" << std::endl;
        return EXIT_FAILURE;
    }
    
    return EXIT_SUCCESS;
}