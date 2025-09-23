// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Traits__h__
#define __PUJ_GL__Traits__h__




#include <iostream>





#include <PUJ_GL/Export.h>
#include <limits>
#include <Eigen/Core>

namespace PUJ_GL
{
  /**
   */
  class Traits
  {
  public:
    using TNatural = unsigned short;
    using TReal    = float;
    using TMatrix  = Eigen::Matrix< TReal, 4, 4 >;
    using TColumn  = Eigen::Matrix< TReal, 4, 1 >;
    using TRow     = Eigen::Matrix< TReal, 1, 4 >;
  };
} // end namespace

// -------------------------------------------------------------------------
#define PUJ_GL_Traits                           \
  public:                                       \
  using TNatural = PUJ_GL::Traits::TNatural;    \
  using TReal    = PUJ_GL::Traits::TReal;       \
  using TMatrix  = PUJ_GL::Traits::TMatrix

#endif // __PUJ_GL__Traits__h__

// eof - Traits.h
