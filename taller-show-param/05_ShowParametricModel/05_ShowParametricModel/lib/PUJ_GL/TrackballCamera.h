// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__TrackballCamera__h__
#define __PUJ_GL__TrackballCamera__h__

#include <PUJ_GL/Traits.h>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT TrackballCamera
  {
    PUJ_GL_Traits;

  public:
    using Self = TrackballCamera;

  public:
    TrackballCamera( );
    virtual ~TrackballCamera( );

    void configure( const TReal* bb );

    void load_perspective( const TReal& aspect );
    void look( );

    void zoom( const TReal& d );
    void yaw( const TReal& a );
    void pitch( const TReal& a );
    void roll( const TReal& a );

    void reset( );

  protected:
    TReal m_Fovy { 45 };

    TReal m_Center[ 3 ] { 0 };
    TReal m_Radius { 0 };
    TMatrix m_Rotation;
  };
} // end namespace

#endif // __PUJ_GL__TrackballCamera__h__

// eof - TrackballCamera.h
