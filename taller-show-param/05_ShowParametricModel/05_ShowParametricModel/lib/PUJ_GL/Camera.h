// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Camera__h__
#define __PUJ_GL__Camera__h__

#include <PUJ_GL/Traits.h>

namespace PUJ_GL
{
  /**
   */
  class Camera
  {
    PUJ_GL_Traits;

  public:
    using Self = Camera;

  public:
    Camera( )
    {
      this->reset( );
    }
    virtual ~Camera( )
    {
    }
    
    void set_eye( const TReal& x, const TReal& y, const TReal& z )
    {
    }

    void set_position( const TReal& x, const TReal& y, const TReal& z )
    {
    }

    void set_up( const TReal& x, const TReal& y, const TReal& z )
    {
      TReal n = std::sqrt( ( x * x ) + ( y * y ) + ( z * z ) );
      if( n == TReal( 0 ) ) n = TReal( 1 );
      
      this->m_Transform( 1, 0 ) = x / n;
      this->m_Transform( 1, 1 ) = y / n;
      this->m_Transform( 1, 2 ) = z / n;
      this->_rebuild_base( );
    }
    
    void reset( )
    {
    }
    
  protected:
    void _rebuild_base( )
    {
    }

  protected:
    TRow m_Eye;
    TRow m_Position;
    
    TMatrix m_Transform;
  };
} // end namespace

#endif // __PUJ_GL__Camera__h__

// eof - Camera.h
