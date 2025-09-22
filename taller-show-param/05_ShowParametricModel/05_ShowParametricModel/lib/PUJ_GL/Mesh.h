// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Mesh__h__
#define __PUJ_GL__Mesh__h__

#include <PUJ_GL/Traits.h>
#include <cstddef>
#include <map>
#include <string>

namespace PUJ_GL
{
  // Forward declaration
  class Image;

  /**
   */
  class PUJ_GL_EXPORT Mesh
  {
    PUJ_GL_Traits;

  public:
    using Self = Mesh;

    // Object -> Group -> Topology -> Count -> Buffer
    using TFaces    = std::pair< TNatural, TNatural* >;
    using TPolygons = std::map< TNatural, TFaces >;
    using TGroups   = std::map< std::string, TPolygons >;
    using TObjects  = std::map< std::string, TGroups >;

  public:
    Mesh( );
    virtual ~Mesh( );

    const TReal* bounding_box( ) const;
    void clear( );
    bool read( const std::string& fname );
    void set_image( PUJ_GL::Image* image );
    void draw( );

  protected:

    template< class _TStreams >
    size_t _vertices( TReal** buffer, _TStreams& vertices );

    template< class _TStreams >
    size_t _normals( TReal** buffer, _TStreams& normals );

    template< class _TStreams >
    size_t _textures( TReal** buffer, _TStreams& textures );

    template< class _TFaces >
    void _faces(
      TNatural** buffer, const TNatural& face_size, const _TFaces& faces
      );

    void _update_bounding_box( );

  protected:
    TReal m_Color[ 3 ];
    TReal m_BoundingBox[ 6 ];

    TReal*   m_Vertices { nullptr };
    TReal*   m_Normals  { nullptr };
    TReal*   m_Textures { nullptr };
    TObjects m_Objects;

    size_t m_NumberOfVertices { 0 };
    size_t m_NumberOfNormals  { 0 };
    size_t m_NumberOfTextures { 0 };

    PUJ_GL::Image* m_Image { nullptr };
  };
} // end namespace

#endif // __PUJ_GL__Mesh__h__

// eof - Mesh.h
