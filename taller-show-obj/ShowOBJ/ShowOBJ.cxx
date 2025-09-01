// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// @author Abel Albuez Sanchez (aa-albuezs@javeriana.edu.co) - Trackball implementation
// @author Ricardo Crus (nombre.apellido@javeriana.edu.co) - Trackball implementation
// ========================================================================

#include <iostream>
#include <cmath>
#include <algorithm>
#include <Eigen/Core>
#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/Mesh.h>
#include <PUJ_GL/Trackball.h>

/**
 */
class MyApp
  : public PUJ_GL::BaseApp
{
public:
  using Self       = MyApp;
  using Superclass = PUJ_GL::BaseApp;

  using TReal = PUJ_GL::Mesh::TReal;
  using TMatrix = Eigen::Matrix< TReal, 4, 4 >;
  using TVector = Eigen::Matrix< TReal, 3, 1 >;

public:
  MyApp(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10, int y = 10
    )
    : Superclass(
      argc, argv,
      GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH,
      w, h, x, y, "Show OBJ models - Trackball + Zoom"
      )
    {
      this->m_Mesh.read_from_OBJ( argv[ 1 ] );
      
      // Calcular el centro y radio del modelo para mejor visualización
      const TReal* bb = this->m_Mesh.bounding_box();
      this->m_ModelCenter[0] = (bb[0] + bb[1]) * TReal(0.5);
      this->m_ModelCenter[1] = (bb[2] + bb[3]) * TReal(0.5);
      this->m_ModelCenter[2] = (bb[4] + bb[5]) * TReal(0.5);
      
      TReal dx = bb[1] - bb[0];
      TReal dy = bb[3] - bb[2];
      TReal dz = bb[5] - bb[4];
      this->m_ModelRadius = std::sqrt(dx*dx + dy*dy + dz*dz) * TReal(0.5);
      
      // Configurar trackball
      this->m_Trackball.setWindowSize( w, h );
    }

  virtual ~MyApp( ) override
    {
      // No hacer nada aquí - BaseApp maneja su propia limpieza
    }

  virtual void init( ) override
    {
      this->Superclass::init( );

      glClearColor( 0.2, 0.2, 0.2, 1.0 );
      glEnable( GL_DEPTH_TEST );
    }

protected:
  virtual void _cb_reshape( int width, int height ) override
    {
      // Actualizar trackball
      this->m_Trackball.setWindowSize( width, height );
      
      TReal a = 1.0;
      if( height != 0 )
        a = TReal( width ) / TReal( height );

      glViewport( 0, 0, width, height );

      glMatrixMode( GL_PROJECTION );
      glLoadIdentity( );
      
      // Usar perspectiva
      TReal fovy = 45.0;
      TReal near = this->m_ModelRadius * 0.1;
      TReal far = this->m_ModelRadius * 10.0;
      gluPerspective( fovy, a, near, far );

      glutPostRedisplay( );
    }
    
  virtual void _cb_display( ) override
    {
      glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );

      glMatrixMode( GL_MODELVIEW );
      glLoadIdentity( );
      
      // Aplicar zoom desde el trackball
      TReal zoom = this->m_Trackball.getZoom();
      glTranslatef( 0, 0, -this->m_ModelRadius * 3.0 * zoom );
      
      // Aplicar rotación desde el trackball
      glMultMatrixf( this->m_Trackball.getRotation().data() );
      
      // Centrar el modelo
      glTranslatef( -this->m_ModelCenter[0], 
                    -this->m_ModelCenter[1], 
                    -this->m_ModelCenter[2] );

      // Show the global orthogonal base
      glBegin( GL_LINES );
      {
        glColor3f( 1, 0, 0 );
        glVertex3f( 0, 0, 0 );
        glVertex3f( this->m_ModelRadius * 0.5, 0, 0 );

        glColor3f( 0, 1, 0 );
        glVertex3f( 0, 0, 0 );
        glVertex3f( 0, this->m_ModelRadius * 0.5, 0 );

        glColor3f( 0, 0, 1 );
        glVertex3f( 0, 0, 0 );
        glVertex3f( 0, 0, this->m_ModelRadius * 0.5 );
      }
      glEnd( );

      // Show mesh
      this->m_Mesh.draw( );

      // Mostrar información en pantalla
      this->drawInfo( );

      glutSwapBuffers( );
    }

  virtual void _cb_keyboard( unsigned char key, int x, int y ) override
    {
      bool needsRedisplay = false;
      
      if( key == 'r' || key == 'R' )
      {
        this->m_Trackball.reset( );
        needsRedisplay = true;
      }
      else if( key == '+' || key == '=' )
      {
        // Zoom in con teclado
        this->m_Trackball.mouseWheel( 1 );
        needsRedisplay = true;
      }
      else if( key == '-' || key == '_' )
      {
        // Zoom out con teclado
        this->m_Trackball.mouseWheel( -1 );
        needsRedisplay = true;
      }
      else if( key == 27 || key == 'q' || key == 'Q' ) // ESC o Q para salir
      {
        this->close( );
        exit( 0 );
      }
      
      if( needsRedisplay )
        glutPostRedisplay( );
    }
    
  virtual void _cb_mouse( int button, int state, int x, int y ) override
    {
      if( state == GLUT_DOWN )
      {
        // Manejar rueda del mouse para zoom
        if( button == 3 ) // Rueda arriba
        {
          this->m_Trackball.mouseWheel( 1 );
          glutPostRedisplay( );
        }
        else if( button == 4 ) // Rueda abajo
        {
          this->m_Trackball.mouseWheel( -1 );
          glutPostRedisplay( );
        }
        else
        {
          // Botones normales
          this->m_Trackball.mouseDown( button, x, y );
        }
      }
      else if( state == GLUT_UP )
      {
        this->m_Trackball.mouseUp( button );
      }
    }
    
  virtual void _cb_motion( int x, int y ) override
    {
      bool changed = false;
      
      // Intentar rotación (botón izquierdo)
      changed |= this->m_Trackball.mouseMove( x, y );
      
      // Intentar zoom (botón medio)
      changed |= this->m_Trackball.mouseDrag( 1, x, y );
      
      if( changed )
        glutPostRedisplay( );
    }

  void drawInfo( )
    {
      // Guardar estado de OpenGL
      glPushAttrib( GL_ALL_ATTRIB_BITS );
      
      // Configurar para texto 2D
      glMatrixMode( GL_PROJECTION );
      glPushMatrix( );
      glLoadIdentity( );
      glOrtho( 0, glutGet( GLUT_WINDOW_WIDTH ), 0, glutGet( GLUT_WINDOW_HEIGHT ), -1, 1 );
      
      glMatrixMode( GL_MODELVIEW );
      glPushMatrix( );
      glLoadIdentity( );
      
      glDisable( GL_DEPTH_TEST );
      glColor3f( 1, 1, 1 );
      
      // Mostrar controles
      int y = glutGet( GLUT_WINDOW_HEIGHT ) - 20;
      const char* info[] = {
        "Controles:",
        " Mouse: Click izq + arrastrar = Rotar",
        " Mouse: Rueda = Zoom",
        " Teclado: R = Reset | +/- = Zoom | ESC/Q = Salir",
        nullptr
      };
      
      for( int i = 0; info[i] != nullptr; i++ )
      {
        glRasterPos2i( 10, y - i * 15 );
        for( const char* c = info[i]; *c != '\0'; c++ )
          glutBitmapCharacter( GLUT_BITMAP_8_BY_13, *c );
      }
      
      // Mostrar zoom actual
      char zoomStr[50];
      sprintf( zoomStr, "Zoom: %.2fx", this->m_Trackball.getZoom() );
      glRasterPos2i( 10, 20 );
      for( const char* c = zoomStr; *c != '\0'; c++ )
        glutBitmapCharacter( GLUT_BITMAP_8_BY_13, *c );
      
      // Restaurar estado
      glPopMatrix( );
      glMatrixMode( GL_PROJECTION );
      glPopMatrix( );
      glPopAttrib( );
    }

protected:
  PUJ_GL::Mesh m_Mesh;
  PUJ_GL::Trackball m_Trackball;
  TVector m_ModelCenter;
  TReal m_ModelRadius;
};

int main( int argc, char** argv )
{
  if( argc < 2 )
  {
    std::cerr << "Uso: " << argv[0] << " <archivo.obj>" << std::endl;
    return EXIT_FAILURE;
  }
  
  MyApp* app = new MyApp( &argc, argv );
  app->init( );
  app->go( );
  // No hacer delete - BaseApp maneja su propia memoria con el singleton

  return( EXIT_SUCCESS );
}

// eof - ShowOBJ.cxx