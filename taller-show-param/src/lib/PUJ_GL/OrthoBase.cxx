// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/OrthoBase.h>
#include <OpenGL/gl.h>

// -------------------------------------------------------------------------
PUJ_GL::OrthoBase::
OrthoBase( const TReal& s )
  : Superclass( ),
    m_Scale( s )
{
  this->m_BoundingBox[ 0 ] = -0.1 * this->m_Scale;
  this->m_BoundingBox[ 1 ] = this->m_Scale;
  this->m_BoundingBox[ 2 ] = -0.1 * this->m_Scale;
  this->m_BoundingBox[ 3 ] = this->m_Scale;
  this->m_BoundingBox[ 4 ] = -0.1 * this->m_Scale;
  this->m_BoundingBox[ 5 ] = this->m_Scale;
}

// -------------------------------------------------------------------------
PUJ_GL::OrthoBase::
~OrthoBase( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::OrthoBase::
draw( )
{
  glBegin( GL_LINES );
  {
    glColor3f( 1, 0, 0 );
    glVertex3f( -0.1 * this->m_Scale, 0, 0 );
    glVertex3f( this->m_Scale, 0, 0 );

    glColor3f( 0, 1, 0 );
    glVertex3f( 0, -0.1 * this->m_Scale, 0 );
    glVertex3f( 0, this->m_Scale, 0 );

    glColor3f( 0, 0, 1 );
    glVertex3f( 0, 0, -0.1 * this->m_Scale );
    glVertex3f( 0, 0, this->m_Scale );
  }
  glEnd( );
}

// eof - OrthoBase.cxx
