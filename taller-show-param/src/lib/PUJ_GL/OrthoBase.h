// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__OrthoBase__h__
#define __PUJ_GL__OrthoBase__h__

#include <PUJ_GL/Object.h>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT OrthoBase
    : public PUJ_GL::Object
  {
    PUJ_GL_Traits;

  public:
    using Self       = OrthoBase;
    using Superclass = PUJ_GL::Object;

  public:
    OrthoBase( const TReal& s );
    virtual ~OrthoBase( ) override;

    virtual void draw( ) override;

  protected:
    TReal m_Scale { 1 };
  };
} // end namespace

#endif // __PUJ_GL__OrthoBase__h__

// eof - OrthoBase.h
