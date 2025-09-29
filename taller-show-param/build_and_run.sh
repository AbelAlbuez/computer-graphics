#!/bin/bash

# =============================================================================
# Script para build y ejecución del proyecto ShowParametricModel
# Autor: Generado automáticamente
# =============================================================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Función para verificar dependencias
check_dependencies() {
    print_info "Verificando dependencias..."
    
    local missing_deps=()
    
    if ! command_exists cmake; then
        missing_deps+=("cmake")
    fi
    
    if ! command_exists make; then
        missing_deps+=("make")
    fi
    
    # Verificar si Eigen3 está disponible
    if ! pkg-config --exists eigen3 2>/dev/null; then
        if ! brew list eigen >/dev/null 2>&1; then
            missing_deps+=("eigen")
        fi
    fi
    
    # Verificar OpenGL (generalmente disponible en macOS)
    if ! command_exists glxinfo 2>/dev/null && ! command_exists glinfo 2>/dev/null; then
        print_warning "OpenGL no detectado, pero debería estar disponible en macOS"
    fi
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        print_error "Dependencias faltantes: ${missing_deps[*]}"
        print_info "Instalar con: brew install ${missing_deps[*]}"
        return 1
    fi
    
    print_success "Todas las dependencias están disponibles"
    return 0
}

# Función para limpiar build anterior
clean_build() {
    print_info "Limpiando build anterior..."
    if [ -d "src/build" ]; then
        rm -rf src/build
        print_success "Build anterior eliminado"
    else
        print_info "No hay build anterior que limpiar"
    fi
}

# Función para crear directorio de build
create_build_dir() {
    print_info "Creando directorio de build..."
    mkdir -p src/build
    cd src/build
    print_success "Directorio de build creado"
}

# Función para configurar con CMake
configure_cmake() {
    print_info "Configurando proyecto con CMake..."
    if cmake ..; then
        print_success "Configuración de CMake completada"
        return 0
    else
        print_error "Error en la configuración de CMake"
        return 1
    fi
}

# Función para compilar el proyecto
compile_project() {
    print_info "Compilando proyecto..."
    if make -j$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo 4); then
        print_success "Compilación completada exitosamente"
        return 0
    else
        print_error "Error en la compilación"
        return 1
    fi
}

# Función para verificar el ejecutable
verify_executable() {
    if [ -f "PUJ_GL_ShowParametricModel" ]; then
        print_success "Ejecutable creado: PUJ_GL_ShowParametricModel"
        chmod +x PUJ_GL_ShowParametricModel
        return 0
    else
        print_error "Ejecutable no encontrado"
        return 1
    fi
}

# Función para mostrar opciones de ejecución
show_run_options() {
    echo ""
    print_info "Opciones de ejecución:"
    echo "  1. Ejecutar sin textura:"
    echo "     ./PUJ_GL_ShowParametricModel"
    echo ""
    echo "  2. Ejecutar con textura:"
    echo "     ./PUJ_GL_ShowParametricModel ../meshes/texture.ppm"
    echo ""
    echo "  3. Ejecutar con otros archivos OBJ:"
    echo "     ./PUJ_GL_ShowParametricModel ../meshes/bunny.obj"
    echo "     ./PUJ_GL_ShowParametricModel ../meshes/cube.obj"
    echo "     ./PUJ_GL_ShowParametricModel ../meshes/ship.obj"
    echo ""
    print_info "Controles de la aplicación:"
    echo "  - Rueda del mouse: Zoom in/out"
    echo "  - Flechas del teclado: Rotar cámara"
    echo "  - Tecla 'R': Resetear cámara"
    echo ""
}

# Función principal
main() {
    echo "============================================================================="
    echo "                    SHOW PARAMETRIC MODEL - BUILD SCRIPT"
    echo "============================================================================="
    echo ""
    
    # Verificar que estamos en el directorio correcto
    if [ ! -f "src/CMakeLists.txt" ]; then
        print_error "No se encontró CMakeLists.txt en src/. Asegúrate de ejecutar desde el directorio correcto."
        exit 1
    fi
    
    # Verificar dependencias
    if ! check_dependencies; then
        print_error "Instala las dependencias faltantes y vuelve a intentar"
        exit 1
    fi
    
    # Limpiar build anterior
    clean_build
    
    # Crear directorio de build
    create_build_dir
    
    # Configurar con CMake
    if ! configure_cmake; then
        print_error "Falló la configuración de CMake"
        exit 1
    fi
    
    # Compilar el proyecto
    if ! compile_project; then
        print_error "Falló la compilación"
        exit 1
    fi
    
    # Verificar ejecutable
    if ! verify_executable; then
        print_error "No se pudo crear el ejecutable"
        exit 1
    fi
    
    # Mostrar opciones de ejecución
    show_run_options
    
    # Preguntar si quiere ejecutar automáticamente
    echo -n "¿Quieres ejecutar la aplicación ahora? (y/n): "
    read -r response
    case $response in
        [yY]|[yY][eE][sS])
            print_info "Ejecutando aplicación con textura..."
            ./PUJ_GL_ShowParametricModel ../meshes/texture.ppm
            ;;
        *)
            print_info "Ejecuta manualmente cuando estés listo"
            ;;
    esac
    
    print_success "Script completado exitosamente!"
}

# Ejecutar función principal
main "$@"
