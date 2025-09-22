// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include "App.h"
#include <PUJ_GL/Image.h>

// -------------------------------------------------------------------------
void parametric_model(
  PUJ_GL::Traits::TReal* point, PUJ_GL::Traits::TReal* normal,
  const PUJ_GL::Traits::TReal& u, const PUJ_GL::Traits::TReal& v
  )
{
  point[ 0 ] = u;
  point[ 1 ] = v;
  point[ 2 ] = 0;

  normal[ 0 ] = 0;
  normal[ 1 ] = 0;
  normal[ 2 ] = 1;
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
  } // end if

  this->m_Scene.load_parametric_model(
    parametric_model,
    -0.5, 0.5, 10, false, -0.5, 0.5, 10, false,
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
  this->m_Scene.draw( );
  glutSwapBuffers( );
}

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
  if( key == 'r' || key == 'R' )
  {
    this->m_Camera.reset( );
    glutPostRedisplay( );
  } // end if
}

// eof - App.cxx
