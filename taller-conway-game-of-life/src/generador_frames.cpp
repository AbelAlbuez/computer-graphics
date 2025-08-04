// =========================================================================
// @author Abel Albuez
// =========================================================================

#include "generador_frames.h"
#include "archivo_pbm.h"
#include "juego_vida.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <iomanip>
#include <sys/stat.h>
#include <sys/types.h>
#include <cstring>
#include <cerrno>

// Constructor
GeneradorFrames::GeneradorFrames(const std::string &prefijo, bool usar_ppm)
    : m_prefijo_salida(prefijo), m_usar_ppm(usar_ppm)
{
}

// Crear directorio si no existe
bool GeneradorFrames::crearDirectorio(const std::string &nombre) const
{
#ifdef _WIN32
    return mkdir(nombre.c_str()) == 0 || errno == EEXIST;
#else
    return mkdir(nombre.c_str(), 0755) == 0 || errno == EEXIST;
#endif
}

// Obtener ruta completa del frame
std::string GeneradorFrames::obtenerRutaFrame(int numero_frame) const
{
    return "frames/" + generarNombreArchivo(numero_frame);
}

// Generar todos los frames
void GeneradorFrames::generar(Tablero &tablero_inicial, float duracion, int fps)
{
    // Calcular número total de frames
    int total_frames = static_cast<int>(duracion * fps);

    if (total_frames <= 0)
    {
        std::cerr << "Error: Número de frames inválido" << std::endl;
        return;
    }

    std::cout << "\n=== Generación de Frames ===" << std::endl;
    std::cout << "Duración: " << duracion << " segundos" << std::endl;
    std::cout << "FPS: " << fps << std::endl;
    std::cout << "Total de frames a generar: " << total_frames << std::endl;
    std::cout << "Formato de salida: " << (m_usar_ppm ? "PPM (color)" : "PBM (blanco y negro)") << std::endl;

    std::cout << "\nCreando directorio 'frames/'..." << std::endl;
    if (!crearDirectorio("frames"))
    {
        std::cerr << "Error: No se pudo crear el directorio 'frames'" << std::endl;
        return;
    }

    std::cout << "Generando frames..." << std::endl;

    Tablero tablero_actual = tablero_inicial.clonar();

    for (int frame = 0; frame < total_frames; frame++)
    {
        mostrarProgreso(frame + 1, total_frames);

        guardarFrame(tablero_actual, frame);

        if (frame < total_frames - 1)
        {
            tablero_actual = JuegoVida::evolucionar(tablero_actual);
        }
    }

    std::cout << "\n\n¡Generación completada!" << std::endl;
    std::cout << "Archivos generados en carpeta 'frames/': " 
              << m_prefijo_salida << "00000" 
              << (m_usar_ppm ? ".ppm" : ".pbm") << " hasta " 
              << m_prefijo_salida << std::setfill('0') << std::setw(5) 
              << (total_frames - 1) << (m_usar_ppm ? ".ppm" : ".pbm") << std::endl;
    
    generarVisualizadorHTML(total_frames, fps, 
                           tablero_inicial.obtenerAncho(), 
                           tablero_inicial.obtenerAlto());
}

// Generar nombre de archivo con formato frame_00000.ppm o .pbm
std::string GeneradorFrames::generarNombreArchivo(int numero_frame) const
{
    std::stringstream ss;
    ss << m_prefijo_salida
       << std::setfill('0') << std::setw(5) << numero_frame
       << (m_usar_ppm ? ".ppm" : ".pbm");
    return ss.str();
}

// Guardar un frame
void GeneradorFrames::guardarFrame(const Tablero &tablero, int numero_frame)
{
    std::string nombre_archivo = obtenerRutaFrame(numero_frame);

    if (m_usar_ppm)
    {
        FrameBuffer fb = tableroAFrameBuffer(tablero);

        std::ofstream archivo(nombre_archivo);
        if (archivo.is_open())
        {
            archivo << fb;
            archivo.close();
        }
        else
        {
            std::cerr << "Error al crear archivo: " << nombre_archivo << std::endl;
        }
    }
    else
    {
        ArchivoPBM::escribir(nombre_archivo, tablero);
    }
}

// Convertir un tablero a FrameBuffer para visualización
FrameBuffer GeneradorFrames::tableroAFrameBuffer(const Tablero &tablero) const
{
    FrameBuffer fb;
    fb.allocate(tablero.obtenerAncho(), tablero.obtenerAlto());

    for (int y = 0; y < tablero.obtenerAlto(); y++)
    {
        for (int x = 0; x < tablero.obtenerAncho(); x++)
        {
            float valor = tablero.obtener(x, y) ? 0.0f : 1.0f;

            fb(y, x, 0) = valor;
            fb(y, x, 1) = valor;
            fb(y, x, 2) = valor;
        }
    }

    return fb;
}

// Mostrar barra de progreso visual
void GeneradorFrames::mostrarProgreso(int actual, int total) const
{
    int porcentaje = (actual * 100) / total;
    int ancho_barra = 50;
    int completado = (ancho_barra * actual) / total;

    std::cout << "\r[";
    for (int i = 0; i < ancho_barra; i++)
    {
        if (i < completado)
        {
            std::cout << "=";
        }
        else if (i == completado)
        {
            std::cout << ">";
        }
        else
        {
            std::cout << " ";
        }
    }
    std::cout << "] " << porcentaje << "% (" << actual << "/" << total << ")";
    std::cout.flush();
}

// Agregar este método a la clase GeneradorFrames
void GeneradorFrames::generarVisualizadorHTML(int total_frames, int fps, 
                                              int ancho_tablero, int alto_tablero) const {
    std::ofstream html("visualizador.html");
    
    html << "<!DOCTYPE html>\n<html>\n<head>\n";
    html << "<title>Juego de la Vida - Animación</title>\n";
    html << "<style>\n";
    html << "body { background: #1a1a1a; color: white; font-family: monospace; ";
    html << "display: flex; flex-direction: column; align-items: center; padding: 20px; }\n";
    html << "#canvas { border: 2px solid #444; background: white; ";
    html << "image-rendering: pixelated; image-rendering: crisp-edges; }\n";
    html << "#controls { margin: 20px; }\n";
    html << "button { padding: 10px 20px; margin: 5px; font-size: 16px; }\n";
    html << "</style>\n</head>\n<body>\n";
    html << "<h1>Juego de la Vida - Animación</h1>\n";
    html << "<canvas id='canvas'></canvas>\n";
    html << "<div id='controls'>\n";
    html << "<button onclick='togglePlay()'>Play/Pausa</button>\n";
    html << "<button onclick='reset()'>Reiniciar</button>\n";
    html << "<span id='info'>Frame: 0/" << total_frames << "</span>\n";
    html << "</div>\n";
    html << "<script>\n";
    
    html << "const totalFrames = " << total_frames << ";\n";
    html << "const fps = " << fps << ";\n";
    html << "const cellSize = 10;\n";
    html << "let currentFrame = 0;\n";
    html << "let playing = true;\n";
    html << "let frames = [];\n\n";
    
    html << "// Datos de los frames\n";
    html << "function loadFrames() {\n";
    html << "  const canvas = document.getElementById('canvas');\n";
    html << "  canvas.width = " << ancho_tablero << " * cellSize;\n";
    html << "  canvas.height = " << alto_tablero << " * cellSize;\n";
    html << "  \n";
    
    for (int i = 0; i < total_frames; i++) {
        std::string nombre_frame = obtenerRutaFrame(i);
        std::ifstream frame_file(nombre_frame);
        
        if (frame_file.is_open()) {
            std::string linea;
            std::vector<std::vector<int>> datos;
            
            for (int skip = 0; skip < 4; skip++) {
                std::getline(frame_file, linea);
            }
            
            html << "  frames[" << i << "] = [";
            for (int y = 0; y < alto_tablero; y++) {
                html << "[";
                for (int x = 0; x < ancho_tablero; x++) {
                    int r, g, b;
                    frame_file >> r >> g >> b;
                    html << (r == 0 ? "1" : "0");
                    if (x < ancho_tablero - 1) html << ",";
                }
                html << "]";
                if (y < alto_tablero - 1) html << ",";
            }
            html << "];\n";
            
            frame_file.close();
        }
    }
    
    html << "}\n\n";
    
    html << "function drawFrame() {\n";
    html << "  const canvas = document.getElementById('canvas');\n";
    html << "  const ctx = canvas.getContext('2d');\n";
    html << "  const frame = frames[currentFrame];\n";
    html << "  \n";
    html << "  ctx.clearRect(0, 0, canvas.width, canvas.height);\n";
    html << "  \n";
    html << "  for (let y = 0; y < frame.length; y++) {\n";
    html << "    for (let x = 0; x < frame[y].length; x++) {\n";
    html << "      if (frame[y][x] === 1) {\n";
    html << "        ctx.fillStyle = 'black';\n";
    html << "        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);\n";
    html << "      }\n";
    html << "    }\n";
    html << "  }\n";
    html << "  \n";
    html << "  document.getElementById('info').textContent = ";
    html << "'Frame: ' + currentFrame + '/' + totalFrames;\n";
    html << "}\n\n";
    
    html << "function animate() {\n";
    html << "  if (playing) {\n";
    html << "    drawFrame();\n";
    html << "    currentFrame = (currentFrame + 1) % totalFrames;\n";
    html << "  }\n";
    html << "}\n\n";
    
    html << "function togglePlay() {\n";
    html << "  playing = !playing;\n";
    html << "}\n\n";
    
    html << "function reset() {\n";
    html << "  currentFrame = 0;\n";
    html << "  drawFrame();\n";
    html << "}\n\n";
    
    html << "// Inicializar\n";
    html << "loadFrames();\n";
    html << "drawFrame();\n";
    html << "setInterval(animate, " << (1000/fps) << ");\n";
    
    html << "</script>\n</body>\n</html>\n";
    html.close();
    
    std::cout << "\n¡Visualizador HTML creado!" << std::endl;
    std::cout << "Abre 'visualizador.html' en tu navegador para ver la animación" << std::endl;
}