// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/ParametricModel.h>
#include <vector>
// -------------------------------------------------------------------------
PUJ_GL::ParametricModel::
ParametricModel( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::ParametricModel::
~ParametricModel( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_parameters_ranges(
  const TReal& minU, const TReal& maxU, const TReal& minV, const TReal& maxV
  )
{
  this->m_MinU = minU;
  this->m_MaxU = maxU;
  this->m_MinV = minV;
  this->m_MaxV = maxV;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_parameters_closeness( const bool& u, const bool& v )
{
  this->m_ClosedU = u;
  this->m_ClosedV = v;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
set_number_of_samples( const TNatural& u, const TNatural& v )
{
  this->m_SamplesU = u;
  this->m_SamplesV = v;
}

// -------------------------------------------------------------------------
void PUJ_GL::ParametricModel::
build( TParametricFunction f )
{
  TReal ou = this->m_MaxU - this->m_MinU;
  TReal ov = this->m_MaxV - this->m_MinV;
  TNatural SU = this->m_SamplesU - ( ( this->m_ClosedU )? 0: 1 );
  TNatural SV = this->m_SamplesV - ( ( this->m_ClosedV )? 0: 1 );

  // Compute sizes
  this->m_NumberOfVertices =
    this->m_NumberOfNormals =
    this->m_NumberOfTextures = this->m_SamplesU * this->m_SamplesV;

  // Reserve buffers
  this->m_Vertices
    =
    reinterpret_cast< TReal* >(
      std::calloc( this->m_NumberOfVertices * 3, sizeof( TReal ) )
      );
  this->m_Normals
    =
    reinterpret_cast< TReal* >(
      std::calloc( this->m_NumberOfNormals * 3, sizeof( TReal ) )
      );
  this->m_Textures
    =
    reinterpret_cast< TReal* >(
      std::calloc( this->m_NumberOfTextures * 2, sizeof( TReal ) )
      );

  TReal* points = this->m_Vertices;
  TReal* normals = this->m_Normals;
  TReal* textures = this->m_Textures;
  size_t n_faces = 2 * ( this->m_SamplesU - 1 ) * ( this->m_SamplesV - 1 );
  TNatural* indices
    =
    reinterpret_cast< TNatural* >(
      std::calloc( n_faces * 9, sizeof( TNatural ) )
      );
  TNatural* idx = indices;
  for( TNatural su = 0; su < this->m_SamplesU; ++su )
  {
    TReal nu = ( TReal( su ) / TReal( SU ) );
    TReal u = ( ou * nu ) + this->m_MinU;
    for( TNatural sv = 0; sv < this->m_SamplesV; ++sv )
    {
      TReal nv = ( TReal( sv ) / TReal( SV ) );
      TReal v = ( ov * nv ) + this->m_MinV;

      // Create points and normals
      f( points, normals, u, v );

      // Create triangles
      if( su < this->m_SamplesU - 1 && sv < this->m_SamplesV - 1 )
      {
        size_t w = su + ( this->m_SamplesU * sv ) + 1;

        // Triangle 1, vertex 1
        *( idx++ ) = w;
        *( idx++ ) = w;
        *( idx++ ) = w;

        // Triangle 1, vertex 2
        *( idx++ ) = w + 1;
        *( idx++ ) = w + 1;
        *( idx++ ) = w + 1;
 
        // Triangle 1, vertex 3
        *( idx++ ) = w + 1 + this->m_SamplesU;
        *( idx++ ) = w + 1 + this->m_SamplesU;
        *( idx++ ) = w + 1 + this->m_SamplesU;

        // Triangle 2, vertex 1
        *( idx++ ) = w;
        *( idx++ ) = w;
        *( idx++ ) = w;

        // Triangle 2, vertex 2
        *( idx++ ) = w + 1 + this->m_SamplesU;
        *( idx++ ) = w + 1 + this->m_SamplesU;
        *( idx++ ) = w + 1 + this->m_SamplesU;

        // Triangle 2, vertex 3
        *( idx++ ) = w + this->m_SamplesU;
        *( idx++ ) = w + this->m_SamplesU;
        *( idx++ ) = w + this->m_SamplesU;
      } // end if

      // Keep track of texture coordinates
      textures[ 0 ] = nu;
      textures[ 1 ] = nv;

      points += 3;
      normals += 3;
      textures += 2;
    } // end for
  } // end for

  // Create topology
  TFaces triangles( n_faces, indices );
  TPolygons polys;
  TGroups group;

  polys.insert( std::make_pair( 3, triangles ) );
  group.insert( std::make_pair( "", polys ) );
  this->m_Objects.insert( std::make_pair( "parametric_object", group ) );

  this->_update_bounding_box( );
}

// eof - ParametricModel.cxx
