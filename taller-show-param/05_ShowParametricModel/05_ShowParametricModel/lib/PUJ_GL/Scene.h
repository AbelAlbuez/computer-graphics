// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Scene__h__
#define __PUJ_GL__Scene__h__

#include <PUJ_GL/Object.h>
#include <functional>

namespace PUJ_GL
{
  // Forward declaration
  class Image;

  /**
   */
  class PUJ_GL_EXPORT Scene
  {
    PUJ_GL_Traits;

  public:
    using Self = Scene;

    using TParametricFunction
      =
      std::function< void( TReal*, TReal*, const TReal&, const TReal& ) >;

  public:
    Scene( );
    virtual ~Scene( );

    virtual void draw( );

    const TReal* clear_color( ) const;
    const TReal* bounding_box( ) const;

    void load_mesh( const std::string& fname );
    void load_orthobase( const TReal& s = 1 );
    void load_parametric_model(
      TParametricFunction function,
      const TReal& minU, const TReal& maxU,
      const TNatural& samplesU, bool closedU,
      const TReal& minV, const TReal& maxV,
      const TNatural& samplesV, bool closedV,
      PUJ_GL::Image* image = nullptr
      );

  protected:
    void _reset( );

  protected:
    TReal m_Color[ 4 ] { 0, 0, 0, 1 };

    mutable bool m_BoudingBoxUpdated { false };
    mutable TReal m_BoundingBox[ 6 ] { 0 };

    std::vector< PUJ_GL::Object* > m_Objects;
  };
} // end namespace

#endif // __PUJ_GL__Scene__h__

// eof - Scene.h
