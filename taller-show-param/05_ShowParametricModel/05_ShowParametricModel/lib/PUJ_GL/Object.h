// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Object__h__
#define __PUJ_GL__Object__h__

#include <PUJ_GL/Traits.h>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT Object
  {
    PUJ_GL_Traits;

  public:
    using Self = Object;

  public:
    Object( );
    virtual ~Object( );

    const TReal* bounding_box( ) const;

    virtual void draw( ) = 0;

  protected:
    TReal m_BoundingBox[ 6 ] { 0 };
  };
} // end namespace

#endif // __PUJ_GL__Object__h__

// eof - Object.h
