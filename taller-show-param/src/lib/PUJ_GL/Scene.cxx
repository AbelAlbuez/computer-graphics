// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Scene.h>
#include <PUJ_GL/MeshObject.h>
#include <PUJ_GL/OrthoBase.h>
#include <PUJ_GL/ParametricModel.h>

// -------------------------------------------------------------------------
PUJ_GL::Scene::
Scene( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::Scene::
~Scene( )
{
  this->_reset( );
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
draw( )
{
  for( PUJ_GL::Object* o: this->m_Objects )
    o->draw( );
}

// -------------------------------------------------------------------------
const PUJ_GL::Scene::
TReal* PUJ_GL::Scene::
clear_color( ) const
{
  return( this->m_Color );
}

// -------------------------------------------------------------------------
const PUJ_GL::Scene::
TReal* PUJ_GL::Scene::
bounding_box( ) const
{
  if( !( this->m_BoudingBoxUpdated ) )
  {
    if( this->m_Objects.size( ) > 0 )
    {
      std::memcpy(
        this->m_BoundingBox,
        this->m_Objects[ 0 ]->bounding_box( ),
        6 * sizeof( TReal )
        );
      for( size_t i = 1; i < this->m_Objects.size( ); ++i )
      {
        for( unsigned short d = 0; d < 3; ++d )
        {
          this->m_BoundingBox[ d << 1 ]
            =
            std::min(
              this->m_BoundingBox[ d << 1 ],
              this->m_Objects[ i ]->bounding_box( )[ d << 1 ]
              );
          this->m_BoundingBox[ ( d << 1 ) + 1 ]
            =
            std::max(
              this->m_BoundingBox[ ( d << 1 ) + 1 ],
              this->m_Objects[ i ]->bounding_box( )[ ( d << 1 ) + 1 ]
              );
        } // end for
      } // end for
    } // end if
    this->m_BoudingBoxUpdated = true;
  } // end if
  return( this->m_BoundingBox );
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_mesh( const std::string& fname )
{
  auto obj = new PUJ_GL::MeshObject( );
  obj->read( fname );
  this->m_Objects.push_back( obj );
  this->m_BoudingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_orthobase( const TReal& s )
{
  this->m_Objects.push_back( new PUJ_GL::OrthoBase( s ) );
  this->m_BoudingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
load_parametric_model(
  TParametricFunction function,
  const TReal& minU, const TReal& maxU,
  const TNatural& samplesU, bool closedU,
  const TReal& minV, const TReal& maxV,
  const TNatural& samplesV, bool closedV,
  PUJ_GL::Image* image
  )
{
  auto obj = new PUJ_GL::MeshObject( );
  auto mesh = new PUJ_GL::ParametricModel( );
  mesh->set_parameters_ranges( minU, maxU, minV, maxV );
  mesh->set_parameters_closeness( closedU, closedV );
  mesh->set_number_of_samples( samplesU, samplesV );
  mesh->build( function );
  mesh->set_image( image );
  obj->set_mesh( mesh );
  this->m_Objects.push_back( obj );
  this->m_BoudingBoxUpdated = false;
}

// -------------------------------------------------------------------------
void PUJ_GL::Scene::
_reset( )
{
  for( PUJ_GL::Object* o: this->m_Objects )
    delete o;
  this->m_Objects.clear( );
}

// eof - Scene.cxx
