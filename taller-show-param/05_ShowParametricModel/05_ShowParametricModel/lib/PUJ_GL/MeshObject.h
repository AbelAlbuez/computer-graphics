// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__MeshObject__h__
#define __PUJ_GL__MeshObject__h__

#include <PUJ_GL/Object.h>

namespace PUJ_GL
{
  // Forward declaration
  class Mesh;

  /**
   */
  class PUJ_GL_EXPORT MeshObject
    : public PUJ_GL::Object
  {
    PUJ_GL_Traits;

  public:
    using Self       = MeshObject;
    using Superclass = PUJ_GL::Object;

  public:
    MeshObject( );
    virtual ~MeshObject( ) override;

    virtual void set_mesh( PUJ_GL::Mesh* mesh );
    virtual void read( const std::string& fname );

    virtual void draw( ) override;

  protected:
    PUJ_GL::Mesh* m_Mesh { nullptr };
  };
} // end namespace

#endif // __PUJ_GL__MeshObject__h__

// eof - MeshObject.h
