#include <iostream>
#include <random>
#include <GL/glut.h>
#include <GL/gl.h>

float* Points = nullptr;
float* Colors = nullptr;
unsigned short* Indices = nullptr;
size_t NumberOfPoints = 0;
size_t NumberOfFaces = 0;

// -------------------------------------------------------------------------
void display( )
{
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  // Setup camera
  gluLookAt(
    0.0, 0.0, 5.0, // Camera is at ( 0, 0, 5 )
    0.0, 0.0, 0.0, // Looks at the origin ( 0, 0, 0 )
    0.0, 1.0, 0.0  // Up vector is ( 0, 1, 0 )
    );

  // Draw the model
  glBegin( GL_TRIANGLES );
  {
    for( size_t f = 0; f < NumberOfFaces * 3; f += 3 )
    {
      glColor3fv( Colors + ( 3 * Indices[ f ] ) );
      glVertex3fv( Points + ( 3 * Indices[ f ] ) );

      glColor3fv( Colors + ( 3 * Indices[ f + 1 ] ) );
      glVertex3fv( Points + ( 3 * Indices[ f + 1 ] ) );

      glColor3fv( Colors + ( 3 * Indices[ f + 2 ] ) );
      glVertex3fv( Points + ( 3 * Indices[ f + 2 ] ) );
    } // end for
  }
  glEnd( );

  glutSwapBuffers( );
}

// -------------------------------------------------------------------------
void reshape( int w, int h )
{
  glViewport( 0, 0, w, h );

  glMatrixMode( GL_PROJECTION );
  glLoadIdentity( );
  gluPerspective( 45.0, float( w ) / float( h ), 1e-1, 100.0 );
}

void parametric( float& x, float& y, float& z, float u, float v )
{
  float r = 0.7;
  x = r * std::cos( u );
  y = r * std::sin( u );
  z = v;

  float dxu = -r * std::sin( u );
  float dyu = r * std::cos( u );
  float dzu = 0;

  float dxv = 0;
  float dyv = 0;
  float dzv = 1;
}

// -------------------------------------------------------------------------
void create_model( )
{
  size_t usamples = 100;
  size_t vsamples = 217;
  size_t nsamples = ( usamples  ) * ( vsamples  );
  float urange[ 2 ] = { 0, 6.28 };
  float vrange[ 2 ] = { 0, 5 };

  Points = reinterpret_cast< float* >( std::calloc( nsamples * 3, sizeof( float ) ) );
  size_t i = 0;
  for( size_t sv = 0; sv < vsamples; ++sv )
  {
    float v = vrange[ 0 ] + ( ( vrange[ 1 ] - vrange[ 0 ] ) * float( sv ) / float( vsamples - 1 ) );
    for( size_t su = 0; su < usamples; ++su )
    {
      float u = urange[ 0 ] + ( ( urange[ 1 ] - urange[ 0 ] ) * float( su ) / float( usamples - 1 ) );
      float x, y, z;
      parametric( x, y, z, u, v );
      Points[ i++ ] = x;
      Points[ i++ ] = y;
      Points[ i++ ] = z;
    } // end for
  } // end for
  NumberOfPoints = nsamples;

  Colors
    =
    reinterpret_cast< float* >(
      std::calloc( NumberOfPoints * 3, sizeof( float ) )
      );
  std::random_device rd;
  std::mt19937 gen( rd( ) );
  std::uniform_int_distribution< unsigned short > dis( 0, 100 );
  for( size_t c = 0; c < NumberOfPoints * 3; ++c )
    Colors[ c ] = float( dis( gen ) ) / float( 100 );

  Indices
    =
    reinterpret_cast< unsigned short* >(
      std::calloc( ( vsamples - 1 ) * ( usamples - 1 ) * 6, sizeof( unsigned short ) )
      );
  i = 0;
  for( size_t v = 0; v < vsamples - 1; ++v )
  {
    for( size_t u = 0; u < usamples - 1; ++u )
    {
      size_t w = u + ( usamples * v );
      Indices[ i++ ] = w;
      Indices[ i++ ] = w + 1;
      Indices[ i++ ] = ( w + 1 ) + usamples;
      Indices[ i++ ] = w;
      Indices[ i++ ] = ( w + 1 ) + usamples;
      Indices[ i++ ] = w + usamples;
    }
  }
  NumberOfFaces = ( vsamples - 1 ) * ( usamples - 1 ) * 2;
}

// -------------------------------------------------------------------------
int main( int argc, char** argv )
{
  glutInit( &argc, argv );
  glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH );
  glutInitWindowSize( 800, 600 );
  glutCreateWindow( "Parametric model with GLUT" );

  // Register callback functions
  glutDisplayFunc( display );
  glutReshapeFunc( reshape );

  glEnable( GL_DEPTH_TEST );
  glClearColor( 0.2f, 0.3f, 0.3f, 1.0f );
  create_model( );
  glutMainLoop( );

  std::free( Points );
  std::free( Indices );

  return( EXIT_SUCCESS );
}
