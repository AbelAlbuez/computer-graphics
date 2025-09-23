// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/TrackballCamera.h>

#include <OpenGL/gl.h>
#include <OpenGL/glu.h>

// -------------------------------------------------------------------------
PUJ_GL::TrackballCamera::
TrackballCamera( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::TrackballCamera::
~TrackballCamera( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
configure( const TReal* bb )
{
  this->m_Center[ 0 ] = ( bb[ 1 ] + bb[ 0 ] ) * 0.5;
  this->m_Center[ 1 ] = ( bb[ 3 ] + bb[ 2 ] ) * 0.5;
  this->m_Center[ 2 ] = ( bb[ 5 ] + bb[ 4 ] ) * 0.5;

  TReal x = bb[ 1 ] - bb[ 0 ];
  TReal y = bb[ 3 ] - bb[ 2 ];
  TReal z = bb[ 5 ] - bb[ 4 ];
  this->m_Radius = std::sqrt( ( x * x ) + ( y * y ) + ( z * z ) ) * 1.5;

  this->m_Rotation.setIdentity( );
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
load_perspective( const TReal& aspect )
{
  gluPerspective(
    this->m_Fovy,
    aspect,
    1e-3 * this->m_Radius,
    4e0 * this->m_Radius
    );
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
look( )
{
  glTranslatef( 0, 0, -this->m_Radius );
  glMultMatrixf( this->m_Rotation.data( ) );
  glTranslatef(
    -this->m_Center[ 0 ], -this->m_Center[ 1 ], -this->m_Center[ 2 ]
    );
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
zoom( const TReal& d )
{
  this->m_Radius += d;
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
yaw( const TReal& a )
{
  TMatrix R = TMatrix::Identity( );
  R( 0, 0 ) = R( 2, 2 ) = std::cos( a );
  R( 0, 2 ) = R( 2, 0 ) = std::sin( a );
  R( 0, 2 ) *= TReal( -1 );
  this->m_Rotation.transpose( ) *= R;
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
pitch( const TReal& a )
{
  TMatrix R = TMatrix::Identity( );
  R( 1, 1 ) = R( 2, 2 ) = std::cos( a );
  R( 1, 2 ) = R( 2, 1 ) = std::sin( a );
  R( 2, 1 ) *= TReal( -1 );
  this->m_Rotation.transpose( ) *= R;
}

// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
roll( const TReal& a )
{
  TMatrix R = TMatrix::Identity( );
  R( 0, 0 ) = R( 1, 1 ) = std::cos( a );
  R( 0, 1 ) = R( 1, 0 ) = std::sin( a );
  R( 1, 0 ) *= TReal( -1 );
  this->m_Rotation.transpose( ) *= R;
}
 
// -------------------------------------------------------------------------
void PUJ_GL::TrackballCamera::
reset( )
{
  this->m_Rotation.setIdentity( );
}

// eof - TrackballCamera.cxx
