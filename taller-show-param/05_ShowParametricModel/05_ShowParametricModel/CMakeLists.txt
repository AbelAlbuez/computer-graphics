## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================
cmake_minimum_required(VERSION 3.11)
project(ShowParametricModel)

# Find necessary packages
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLUT REQUIRED)
include(CMakeBaseDefs.cmake)

# Local include directories
include_directories(
  ${OPENGL_INCLUDE_DIR} ${GLUT_INCLUDE_DIR}
  ${PROJECT_BINARY_DIR}/lib ${PROJECT_SOURCE_DIR}/lib
  )

# Build library
add_library(
  PUJ_GL
  STATIC
  lib/PUJ_GL/BaseApp.cxx
  lib/PUJ_GL/Image.cxx
  lib/PUJ_GL/Mesh.cxx
  lib/PUJ_GL/MeshObject.cxx
  lib/PUJ_GL/Object.cxx
  lib/PUJ_GL/OrthoBase.cxx
  lib/PUJ_GL/ParametricModel.cxx
  lib/PUJ_GL/Scene.cxx
  lib/PUJ_GL/TrackballCamera.cxx
  )
generate_export_header(
  PUJ_GL
  EXPORT_MACRO_NAME PUJ_GL_EXPORT
  EXPORT_FILE_NAME lib/PUJ_GL/Export.h
  )
target_link_libraries(
  PUJ_GL
  Eigen3::Eigen
  ${OPENGL_LIBRARY} ${GLUT_glut_LIBRARY}
  )

# Build app
add_executable(PUJ_GL_ShowParametricModel main.cxx App.cxx)
target_link_libraries(PUJ_GL_ShowParametricModel PUJ_GL)

## eof - CMakeLists.txt
