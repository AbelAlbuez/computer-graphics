// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__ParametricModel__h__
#define __PUJ_GL__ParametricModel__h__

#include <PUJ_GL/Mesh.h>
#include <functional>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT ParametricModel
    : public PUJ_GL::Mesh
  {
    PUJ_GL_Traits;

  public:
    using Self       = ParametricModel;
    using Superclass = PUJ_GL::Mesh;

    using TParametricFunction
      =
      std::function< void( TReal*, TReal*, const TReal&, const TReal& ) >;

  public:
    ParametricModel( );
    virtual ~ParametricModel( ) override;

    void set_parameters_ranges(
      const TReal& minU, const TReal& maxU,
      const TReal& minV, const TReal& maxV
      );
    void set_parameters_closeness( const bool& u, const bool& v );
    void set_number_of_samples( const TNatural& u, const TNatural& v );

    void build( TParametricFunction f );

  protected:
    TReal m_MinU { 0 };
    TReal m_MaxU { 0 };
    TReal m_MinV { 0 };
    TReal m_MaxV { 0 };
    bool m_ClosedU { false };
    bool m_ClosedV { false };
    TNatural m_SamplesU { 0 };
    TNatural m_SamplesV { 0 };
  };
} // end namespace

#endif // __PUJ_GL__ParametricModel__h__

// eof - ParametricModel.h
