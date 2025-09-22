// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/MeshObject.h>
#include <PUJ_GL/Mesh.h>

// -------------------------------------------------------------------------
PUJ_GL::MeshObject::
MeshObject( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::MeshObject::
~MeshObject( )
{
  if( this->m_Mesh != nullptr )
    delete this->m_Mesh;
}

// -------------------------------------------------------------------------
void PUJ_GL::MeshObject::
set_mesh( PUJ_GL::Mesh* mesh )
{
  if( this->m_Mesh != nullptr )
    delete this->m_Mesh;
  this->m_Mesh = mesh;
}

// -------------------------------------------------------------------------
void PUJ_GL::MeshObject::
read( const std::string& fname )
{
  this->m_Mesh = new PUJ_GL::Mesh( );
  this->m_Mesh->read( fname );
  std::memcpy(
    this->m_BoundingBox, this->m_Mesh->bounding_box( ), 6 * sizeof( TReal )
    );
}

// -------------------------------------------------------------------------
void PUJ_GL::MeshObject::
draw( )
{
  if( this->m_Mesh != nullptr )
    this->m_Mesh->draw( );
}

// eof - MeshObject.cxx
