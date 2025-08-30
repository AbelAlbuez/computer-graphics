// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include <iostream>
#include <Eigen/Core>
#include <PUJ_GL/BaseApp.h>
#include <PUJ_GL/Mesh.h>

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

public:
  MyApp(
    int* argc, char** argv,
    int w = 500, int h = 500,
    int x = 10, int y = 10
    )
    : Superclass(
      argc, argv,
      GLUT_DOUBLE | GLUT_RGB,
      w, h, x, y, "Show OBJ models"
      )
    {
      this->m_Camera.setIdentity( );
      this->m_Mesh.read_from_OBJ( argv[ 1 ] );
    }

  virtual ~MyApp( ) override
    {
    }

  virtual void init( ) override
    {
      this->Superclass::init( );

      glClearColor( 0.0, 0.0, 0.0, 1.0 );
    }

protected:
  virtual void _cb_reshape( int width, int height ) override
    {
      TReal a = 1.0;

      if( height != 0 )
        a = TReal( width ) / TReal( height );

      glViewport( 0, 0, width, height );

      glMatrixMode( GL_PROJECTION );
      glLoadIdentity( );

      // glOrtho( left, right, bottom, up, near, far );
      // glFrustum( left, right, bottom, up, near, far );
      // gluPerspective( fovy, aspect, near, far );

      glutPostRedisplay( );
    }
  virtual void _cb_display( ) override
    {
      glClear( GL_COLOR_BUFFER_BIT );

      glMatrixMode( GL_MODELVIEW );
      glLoadIdentity( );

      glMultMatrixf( this->m_Camera.data( ) );

      // Show the global orthogonal base
      glBegin( GL_LINES );
      {
        glColor3f( 1, 0, 0 );
        glVertex3f( -0.1, 0, 0 );
        glVertex3f( 1, 0, 0 );

        glColor3f( 0, 1, 0 );
        glVertex3f( 0, -0.1, 0 );
        glVertex3f( 0, 1, 0 );

        glColor3f( 0, 0, 1 );
        glVertex3f( 0, 0, -0.1 );
        glVertex3f( 0, 0, 1 );
      }
      glEnd( );

      // Show mesh
      this->m_Mesh.draw( );

      glutSwapBuffers( );
    }

  virtual void _cb_keyboard( unsigned char key, int x, int y ) override
    {
      if( key == 'x' || key == 'X' )
      {
        this->m_Axis = 'x';
      }
      else if( key == 'y' || key == 'Y' )
      {
        this->m_Axis = 'y';
      }
      else if( key == 'z' || key == 'Z' )
      {
        this->m_Axis = 'z';
      }
      else if( key == '+' || key == '-' )
      {
        static const TReal a = std::atan( TReal( 1 ) ) / TReal( 45 );
        static const TReal ca = std::cos( a );
        static const TReal sa = std::sin( a );

        TMatrix R = TMatrix::Identity( );
        if( this->m_Axis == 'x' )
        {
          R( 1, 1 ) = R( 2, 2 ) = ca;
          R( 1, 2 ) = R( 2, 1 ) = sa;
          if     ( key == '+' ) R( 1, 2 ) *= TReal( -1 );
          else if( key == '-' ) R( 2, 1 ) *= TReal( -1 );
        }
        else if( this->m_Axis == 'y' )
        {
          R( 0, 0 ) = R( 2, 2 ) = ca;
          R( 0, 2 ) = R( 2, 0 ) = sa;
          if     ( key == '+' ) R( 2, 0 ) *= TReal( -1 );
          else if( key == '-' ) R( 0, 2 ) *= TReal( -1 );
        }
        else if( this->m_Axis == 'z' )
        {
          R( 0, 0 ) = R( 1, 1 ) = ca;
          R( 0, 1 ) = R( 1, 0 ) = sa;
          if     ( key == '+' ) R( 0, 1 ) *= TReal( -1 );
          else if( key == '-' ) R( 1, 0 ) *= TReal( -1 );
        } // end if
        this->m_Camera.transpose( ) *= R.transpose( );

        glutPostRedisplay( );
      }
      else if( key == 'r' || key == 'R' )
      {
        this->m_Camera.setIdentity( );
        glutPostRedisplay( );
      } // end if
    }

protected:
  TMatrix m_Camera;
  unsigned char m_Axis { 'y' };
  PUJ_GL::Mesh m_Mesh;
};

int main( int argc, char** argv )
{
  MyApp app( &argc, argv );
  app.init( );
  app.go( );

  return( EXIT_SUCCESS );
}

// eof - ShowOBJ.cxx
