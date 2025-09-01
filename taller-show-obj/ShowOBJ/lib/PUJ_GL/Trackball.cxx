// =========================================================================
// @author Abel Albuez Sanchez (aa-albuezs@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Trackball.h>
#include <cmath>
#include <algorithm>

// -------------------------------------------------------------------------
PUJ_GL::Trackball::
Trackball( )
  : m_Width( 500 ), m_Height( 500 ),
    m_MouseDown( false ), m_Zoom( 1.0 ),
    m_RotationSpeed( 1.0 ), m_ZoomSpeed( 0.01 )
{
  this->m_Rotation.setIdentity( );
}

// -------------------------------------------------------------------------
PUJ_GL::Trackball::
~Trackball( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
setWindowSize( int width, int height )
{
  this->m_Width = width;
  this->m_Height = height;
}

// -------------------------------------------------------------------------
const PUJ_GL::Trackball::TMatrix& PUJ_GL::Trackball::
getRotation( ) const
{
  return this->m_Rotation;
}

// -------------------------------------------------------------------------
PUJ_GL::Trackball::TReal PUJ_GL::Trackball::
getZoom( ) const
{
  return this->m_Zoom;
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
reset( )
{
  this->m_Rotation.setIdentity( );
  this->m_Zoom = 1.0;
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
mouseDown( int button, int x, int y )
{
  if( button == 0 ) // Botón izquierdo
  {
    this->m_MouseDown = true;
    this->m_LastX = x;
    this->m_LastY = y;
    this->m_LastPos = this->projectToSphere( x, y );
  }
  else if( button == 1 ) // Botón medio/rueda
  {
    this->m_ZoomStart = y;
  }
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
mouseUp( int button )
{
  if( button == 0 )
    this->m_MouseDown = false;
}

// -------------------------------------------------------------------------
bool PUJ_GL::Trackball::
mouseMove( int x, int y )
{
  if( !this->m_MouseDown )
    return false;

  // Calcular nueva posición en la esfera
  TVector currPos = this->projectToSphere( x, y );

  // Calcular eje de rotación (producto cruz manual)
  TVector axis;
  axis[0] = this->m_LastPos[1] * currPos[2] - this->m_LastPos[2] * currPos[1];
  axis[1] = this->m_LastPos[2] * currPos[0] - this->m_LastPos[0] * currPos[2];
  axis[2] = this->m_LastPos[0] * currPos[1] - this->m_LastPos[1] * currPos[0];

  // Calcular ángulo
  TReal angle = std::acos( 
    std::min( TReal(1.0), std::max( TReal(-1.0), 
      this->m_LastPos.dot( currPos ) 
    ))
  ) * this->m_RotationSpeed;

  // Si hay rotación significativa
  TReal axisLength = std::sqrt( axis[0]*axis[0] + axis[1]*axis[1] + axis[2]*axis[2] );
  if( axisLength > 1e-6 && std::abs(angle) > 1e-6 )
  {
    // Normalizar eje
    axis[0] /= axisLength;
    axis[1] /= axisLength;
    axis[2] /= axisLength;

    // Crear matriz de rotación usando Rodrigues
    TMatrix R;
    this->createRotationMatrix( R, axis, angle );

    // Acumular rotación
    this->m_Rotation = R * this->m_Rotation;

    // Actualizar última posición
    this->m_LastPos = currPos;
    this->m_LastX = x;
    this->m_LastY = y;

    return true; // Hubo cambio
  }
  return false;
}

// -------------------------------------------------------------------------
bool PUJ_GL::Trackball::
mouseWheel( int direction )
{
  TReal factor = 1.0 + direction * this->m_ZoomSpeed * 5.0;
  this->m_Zoom *= factor;
  this->m_Zoom = std::max( TReal(0.1), std::min( TReal(10.0), this->m_Zoom ) );
  return true;
}

// -------------------------------------------------------------------------
bool PUJ_GL::Trackball::
mouseDrag( int button, int x, int y )
{
  if( button == 1 ) // Botón medio
  {
    int dy = y - this->m_ZoomStart;
    TReal factor = 1.0 + dy * this->m_ZoomSpeed;
    this->m_Zoom *= factor;
    this->m_Zoom = std::max( TReal(0.1), std::min( TReal(10.0), this->m_Zoom ) );
    this->m_ZoomStart = y;
    return true;
  }
  return false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
setRotationSpeed( TReal speed )
{
  this->m_RotationSpeed = speed;
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
setZoomSpeed( TReal speed )
{
  this->m_ZoomSpeed = speed;
}

// -------------------------------------------------------------------------
PUJ_GL::Trackball::TVector PUJ_GL::Trackball::
projectToSphere( int x, int y )
{
  TVector v;
  v[0] = (2.0 * x - this->m_Width) / this->m_Width;
  v[1] = (this->m_Height - 2.0 * y) / this->m_Height;

  TReal d = v[0] * v[0] + v[1] * v[1];
  if( d <= 1.0 )
    v[2] = std::sqrt( 1.0 - d );
  else
  {
    v[0] /= std::sqrt( d );
    v[1] /= std::sqrt( d );
    v[2] = 0.0;
  }

  return v;
}

// -------------------------------------------------------------------------
void PUJ_GL::Trackball::
createRotationMatrix( TMatrix& R, const TVector& axis, TReal angle )
{
  TReal c = std::cos( angle );
  TReal s = std::sin( angle );
  TReal t = 1.0 - c;

  R.setIdentity( );
  R(0,0) = t*axis[0]*axis[0] + c;
  R(0,1) = t*axis[0]*axis[1] - s*axis[2];
  R(0,2) = t*axis[0]*axis[2] + s*axis[1];

  R(1,0) = t*axis[0]*axis[1] + s*axis[2];
  R(1,1) = t*axis[1]*axis[1] + c;
  R(1,2) = t*axis[1]*axis[2] - s*axis[0];

  R(2,0) = t*axis[0]*axis[2] - s*axis[1];
  R(2,1) = t*axis[1]*axis[2] + s*axis[0];
  R(2,2) = t*axis[2]*axis[2] + c;
}

// eof - Trackball.cxx
