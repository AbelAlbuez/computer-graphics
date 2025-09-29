// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include "App.h"
#include <PUJ_GL/Image.h>
#include <cmath>
#include <iostream>
// -------------------------------------------------------------------------

// Función helper para mapear rangos
PUJ_GL::Traits::TReal remap_to_2pi(PUJ_GL::Traits::TReal t) {
  return (t + 0.5) * 2.0 * M_PI;
}

void parametric_model(
  PUJ_GL::Traits::TReal* point, 
  PUJ_GL::Traits::TReal* normal,
  const PUJ_GL::Traits::TReal& u, 
  const PUJ_GL::Traits::TReal& v
)
{
  // Plano simple
  point[0] = u * 2.0;
  point[1] = v * 2.0;
  point[2] = 0;

  // Normal hacia arriba
  normal[0] = 0;
  normal[1] = 0;
  normal[2] = 1;
}

// -------------------------------------------------------------------------
App::
App(
  int* argc, char** argv,
  int w, int h,
  int x, int y
  )
  : Superclass(
    argc, argv, GLUT_DOUBLE | GLUT_RGB, w, h, x, y, "Show a parametric model"
    )
{
  PUJ_GL::Image* image = nullptr;
  if( *argc > 1 )
  {
    image = new PUJ_GL::Image( );
    if( !( image->read_from_Netpbm( argv[ 1 ] ) ) )
    {
      delete image;
      image = nullptr;
    } // end if
    else
    {
      this->m_Image = image;
    }
  } // end if

  this->m_Scene.load_parametric_model(
    parametric_model,
    0.5, -0.5, 170, false, 0.5, -0.5, 170, false,
    image
    );

  this->m_Camera.configure( this->m_Scene.bounding_box( ) );
  this->m_Scene.load_orthobase( 0.1 );
}

// -------------------------------------------------------------------------
App::
~App( )
{
}

// -------------------------------------------------------------------------
void App::
init( )
{
  this->Superclass::init( );
  const TReal* c = this->m_Scene.clear_color( );
  glClearColor( c[ 0 ], c[ 1 ], c[ 2 ], c[ 3 ] );

  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  
   // Posición del bombillo
   GLfloat light_pos[] = {0.0f, 0.0f, 2.0f, 1.0f};  // Sobre el centro
   GLfloat light_ambient[] = {0.2f, 0.2f, 0.2f, 1.0f};  
   GLfloat light_diffuse[] = {1.0f, 1.0f, 0.9f, 1.0f};  // Ligeramente cálida
   GLfloat light_specular[] = {1.0f, 1.0f, 1.0f, 1.0f}; // Brillos
   
   glLightfv(GL_LIGHT0, GL_POSITION, light_pos);
   glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
   glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
   glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
   
   // Atenuación (cómo se desvanece con distancia)
   glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0f);
   glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.5f);
   glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.2f);
   
   // Material con brillo
   GLfloat mat_specular[] = {0.3f, 0.3f, 0.3f, 1.0f};
   GLfloat mat_shininess[] = {30.0f};
   
   glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular);
   glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);
}

// -------------------------------------------------------------------------
void App::
_cb_reshape( int width, int height )
{
  TReal a = 1.0;

  if( height != 0 )
    a = TReal( width ) / TReal( height );

  glViewport( 0, 0, width, height );

  glMatrixMode( GL_PROJECTION );
  glLoadIdentity( );

  this->m_Camera.load_perspective( a );

  glutPostRedisplay( );
}

// -------------------------------------------------------------------------
void App::
_cb_display( )
{
  glClear( GL_COLOR_BUFFER_BIT );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  this->m_Camera.look( );
  
  glEnable(GL_LIGHTING);
  glEnable(GL_LIGHT0);
  glEnable(GL_DEPTH_TEST);
  
  // Dibujar plano con bump mapping
  drawBumpMappedPlane(100, 2.0f, 3.0f);
  
  glutSwapBuffers();
}

// -------------------------------------------------------------------------
void App::drawBumpMappedPlane(int gridSize, float planeSize, float bumpStrength)
{
  if(this->m_Image == nullptr) return;
  
  // Usar las variables miembro
  gridSize = m_gridSize;
  bumpStrength = m_bumpStrength;
  
  float tileSize = planeSize / gridSize;
  float halfSize = planeSize / 2.0f;
  
  for(int i = 0; i < gridSize-1; i++) {
    for(int j = 0; j < gridSize-1; j++) {
      float x = -halfSize + i * tileSize;
      float y = -halfSize + j * tileSize;
      
      float u = float(i) / float(gridSize);
      float v = float(j) / float(gridSize);
      
      // Declarar variables para alturas
      float h, hRight, hUp;
      
      if(m_useSmoothing) {
        h = sampleImageSmooth(u, v);
        hRight = sampleImageSmooth(u + 1.0f/gridSize, v);
        hUp = sampleImageSmooth(u, v + 1.0f/gridSize);
      } else {
        const unsigned char* pixel = (*this->m_Image)(1.0f - v, u);
        const unsigned char* pixelRight = (*this->m_Image)(1.0f - v, u + 1.0f/gridSize);
        const unsigned char* pixelUp = (*this->m_Image)(1.0f - (v + 1.0f/gridSize), u);
        
        if(!pixel || !pixelRight || !pixelUp) continue;
        
        h = float(pixel[0]) / 255.0f;
        hRight = float(pixelRight[0]) / 255.0f;
        hUp = float(pixelUp[0]) / 255.0f;
      }
      
      // Calcular gradientes para bump mapping
      float dx = (hRight - h) * bumpStrength;
      float dy = (hUp - h) * bumpStrength;
      
      // Normal perturbada
      float nx = -dx;
      float ny = -dy;
      float nz = 1.0f;
      
      float len = sqrt(nx*nx + ny*ny + nz*nz);
      nx /= len; ny /= len; nz /= len;
      
      // Aplicar color de la imagen
      const unsigned char* colorPixel = (*this->m_Image)(1.0f - v, u);
      if(colorPixel) {
        GLfloat color[4];
        // Asumiendo imagen en escala de grises (para Homero)
        float gray = float(colorPixel[0]) / 255.0f;
        // Para imágenes a color (si m_Channels >= 3)
        color[0] = float(colorPixel[0]) / 255.0f;  // R
        color[1] = float(colorPixel[1]) / 255.0f;  // G  
        color[2] = float(colorPixel[2]) / 255.0f;  // B
        color[3] = 1.0f;
        
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, color);
      }
      
      glBegin(GL_QUADS);
        glNormal3f(nx, ny, nz);
        glVertex3f(x, y, 0);
        glVertex3f(x + tileSize, y, 0);
        glVertex3f(x + tileSize, y + tileSize, 0);
        glVertex3f(x, y + tileSize, 0);
      glEnd();
    }
  }
}
// -------------------------------------------------------------------------

// -------------------------------------------------------------------------
float App::sampleImageSmooth(float u, float v)
{
  if(this->m_Image == nullptr) return 0.5f;
  
  // Promedio de 3x3 píxeles
  float sum = 0.0f;
  int count = 0;
  float step = 1.0f / 500.0f; // Tamaño del muestreo
  
  for(int i = -1; i <= 1; i++) {
    for(int j = -1; j <= 1; j++) {
      float su = u + i * step;
      float sv = v + j * step;
      
      // Clamp a [0,1]
      su = std::max(0.0f, std::min(1.0f, su));
      sv = std::max(0.0f, std::min(1.0f, sv));
      
      const unsigned char* pixel = (*this->m_Image)(1.0f - sv, su);
      if(pixel) {
        sum += float(pixel[0]) / 255.0f;
        count++;
      }
    }
  }
  
  return count > 0 ? sum / count : 0.5f;
}
// -------------------------------------------------------------------------

// -------------------------------------------------------------------------
void App::
_cb_mouse( int button, int state, int x, int y )
{
  if( state == 1 && ( button == 3 || button == 4 ) )
  {
    this->m_Camera.zoom( 1e-1 * TReal( ( button == 3 )? -1: 1 ) );
    glutPostRedisplay( );
  } // end if
}

// -------------------------------------------------------------------------
void App::
_cb_special( int key, int x, int y )
{
  static const TReal a = std::atan( TReal( 1 ) ) / TReal( 45 );

  if( key == 100 ) // Left
  {
    this->m_Camera.yaw( -a );
    glutPostRedisplay( );
  }
  else if( key == 102 ) // Right
  {
    this->m_Camera.yaw( a );
    glutPostRedisplay( );
  }
  else if( key == 101 ) // Up
  {
    this->m_Camera.pitch( -a );
    glutPostRedisplay( );
  }
  else if( key == 103 ) // Down
  {
    this->m_Camera.pitch( a );
    glutPostRedisplay( );
  } // end if
}



// -------------------------------------------------------------------------
void App::
_cb_keyboard( unsigned char key, int x, int y )
{
  if(key == 'r' || key == 'R') {
    this->m_Camera.reset();
    glutPostRedisplay();
  }
  else if(key == '+' || key == '=') {
    m_bumpStrength += 0.5f;
    std::cout << "Bump strength: " << m_bumpStrength << std::endl;
    glutPostRedisplay();
  }
  else if(key == '-' || key == '_') {
    m_bumpStrength = std::max(0.0f, m_bumpStrength - 0.5f);
    std::cout << "Bump strength: " << m_bumpStrength << std::endl;
    glutPostRedisplay();
  }
  else if(key == 's' || key == 'S') {
    m_useSmoothing = !m_useSmoothing;
    std::cout << "Smoothing: " << (m_useSmoothing ? "ON" : "OFF") << std::endl;
    glutPostRedisplay();
  }
  else if(key == 'l' || key == 'L') {
    m_lightAngle += 0.2f;
  
  // Mover bombillo en círculo sobre el plano
  GLfloat light_pos[] = {
    2.0f * cos(m_lightAngle),  // Radio 2
    2.0f * sin(m_lightAngle),
    2.0f,                      // Altura fija
    1.0f                       // Luz puntual
  };
  
  glLightfv(GL_LIGHT0, GL_POSITION, light_pos);
  glutPostRedisplay();
  }
}

// eof - App.cxx
