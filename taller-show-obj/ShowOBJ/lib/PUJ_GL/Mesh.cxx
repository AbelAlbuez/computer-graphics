// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Mesh.h>
#include <fstream>
#include <sstream>
#include <GL/gl.h>

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
Mesh( )
{
  this->m_Color[ 0 ] = 1;
  this->m_Color[ 1 ] = 1;
  this->m_Color[ 2 ] = 1;
}

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
~Mesh( )
{
}

// -------------------------------------------------------------------------
const PUJ_GL::Mesh::
TReal* PUJ_GL::Mesh::
bounding_box( ) const
{
  return( this->m_BoundingBox );
}

// -------------------------------------------------------------------------
bool PUJ_GL::Mesh::
read_from_OBJ( const std::string& fname )
{
  this->m_Points.clear( );
  this->m_Edges.clear( );
  this->m_Triangles.clear( );
  this->m_Quads.clear( );

  // Read file into a memory buffer
  std::ifstream obj_file( fname.c_str( ), std::ios::binary | std::ios::ate );
  if( !obj_file.is_open( ) )
    return( false );
  std::streamsize file_size = obj_file.tellg();
  obj_file.seekg( 0, std::ios::beg );
  std::vector< char > obj_buffer( file_size );
  bool ok = bool( obj_file.read( obj_buffer.data( ), file_size ) );
  obj_file.close( );
  if( !ok )
    return( false );

  // Create stream
  std::istringstream obj_str( obj_buffer.data( ) );

  // Read line-by-line
  std::string line;
  while( std::getline( obj_str, line ) )
  {
    std::istringstream line_str( line );
    std::string cmd;
    line_str >> cmd;

    if( cmd == "v" )
    {
      TReal x, y, z;
      line_str >> x >> y >> z;
      if( this->m_Points.size( ) > 0 )
      {
        this->m_BoundingBox[ 0 ] = std::min( x, this->m_BoundingBox[ 0 ] );
        this->m_BoundingBox[ 2 ] = std::min( y, this->m_BoundingBox[ 2 ] );
        this->m_BoundingBox[ 4 ] = std::min( z, this->m_BoundingBox[ 4 ] );

        this->m_BoundingBox[ 1 ] = std::max( x, this->m_BoundingBox[ 1 ] );
        this->m_BoundingBox[ 3 ] = std::max( y, this->m_BoundingBox[ 3 ] );
        this->m_BoundingBox[ 5 ] = std::max( z, this->m_BoundingBox[ 5 ] );
      }
      else
      {
        this->m_BoundingBox[ 0 ] = this->m_BoundingBox[ 1 ] = x;
        this->m_BoundingBox[ 2 ] = this->m_BoundingBox[ 3 ] = y;
        this->m_BoundingBox[ 4 ] = this->m_BoundingBox[ 5 ] = z;
      } // end if
      this->m_Points.push_back( x );
      this->m_Points.push_back( y );
      this->m_Points.push_back( z );
    }
    else if( cmd == "f" )
    {
      std::vector< TNatural > idx;
      TNatural i;
      while( line_str >> i )
        idx.push_back( i - 1 );

      std::vector< TNatural >* o = nullptr;
      if     ( idx.size( ) == 2 ) o = &( this->m_Edges );
      else if( idx.size( ) == 3 ) o = &( this->m_Triangles );
      else if( idx.size( ) == 4 ) o = &( this->m_Quads );
      if( o != nullptr )
        o->insert( o->end( ), idx.begin( ), idx.end( ) );
    } // end if

  } // end while

  // Free unneeded memory
  this->m_Points.shrink_to_fit( );
  this->m_Edges.shrink_to_fit( );
  this->m_Triangles.shrink_to_fit( );
  this->m_Quads.shrink_to_fit( );

  return( true );
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
draw( )
{
  glColor3fv( this->m_Color );

  const TReal* p = this->m_Points.data( );

  glBegin( GL_LINES );
  {
    for( size_t i = 0; i < this->m_Edges.size( ); ++i )
      glVertex3fv( p + ( this->m_Edges[ i ] * 3 ) );
  }
  glEnd( );

  for( size_t i = 0; i < this->m_Triangles.size( ); i += 3 )
  {
    glBegin( GL_LINE_LOOP );
    {
      glVertex3fv( p + ( this->m_Triangles[   i   ] * 3 ) );
      glVertex3fv( p + ( this->m_Triangles[ i + 1 ] * 3 ) );
      glVertex3fv( p + ( this->m_Triangles[ i + 2 ] * 3 ) );
    }
    glEnd( );
  } // end for

  for( size_t i = 0; i < this->m_Quads.size( ); i += 4 )
  {
    glBegin( GL_LINE_LOOP );
    {
      glVertex3fv( p + ( this->m_Quads[   i   ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 1 ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 2 ] * 3 ) );
      glVertex3fv( p + ( this->m_Quads[ i + 3 ] * 3 ) );
    }
    glEnd( );
  } // end for
}

// eof - Mesh.cxx
