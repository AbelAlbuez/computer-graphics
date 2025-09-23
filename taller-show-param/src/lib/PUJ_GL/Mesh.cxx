// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Mesh.h>
#include <PUJ_GL/Image.h>
#include <fstream>
#include <sstream>
#include <OpenGL/gl.h>

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
Mesh( )
{
  this->clear( );

  this->m_Color[ 0 ] = 1;
  this->m_Color[ 1 ] = 1;
  this->m_Color[ 2 ] = 1;
}

// -------------------------------------------------------------------------
PUJ_GL::Mesh::
~Mesh( )
{
  this->clear( );
}

// -------------------------------------------------------------------------
const PUJ_GL::Mesh::
TReal* PUJ_GL::Mesh::
bounding_box( ) const
{
  return( this->m_BoundingBox );
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
clear( )
{
  if( this->m_Vertices != nullptr )
    std::free( this->m_Vertices );
  if( this->m_Normals != nullptr )
    std::free( this->m_Normals );
  if( this->m_Textures != nullptr )
    std::free( this->m_Textures );
  for( const auto& o: this->m_Objects )
    for( const auto& g: o.second )
      for( const auto& s: g.second )
        if( s.second.second != nullptr )
          std::free( s.second.second );
  if( this->m_Image != nullptr )
    delete this->m_Image;


  this->m_Vertices = nullptr;
  this->m_Normals = nullptr;
  this->m_Textures = nullptr;
  this->m_Objects.clear( );

  this->m_NumberOfVertices = 0;
  this->m_NumberOfNormals = 0;
  this->m_NumberOfTextures = 0;

  this->m_Image = nullptr;
}

// -------------------------------------------------------------------------
bool PUJ_GL::Mesh::
read( const std::string& fname )
{
  using _TStreams = std::vector< std::istringstream >;
  using _TLines = std::map< std::string, _TStreams >;
  using _TObjects = std::map< std::string, _TLines >;

  this->clear( );

  // Read file into a memory buffer
  std::ifstream obj_file( fname.c_str( ), std::ios::binary | std::ios::ate );
  if( !obj_file.is_open( ) )
    return( false );
  std::streamsize file_size = obj_file.tellg( );
  obj_file.seekg( 0, std::ios::beg );
  std::vector< char > obj_buffer( file_size );
  bool ok = bool( obj_file.read( obj_buffer.data( ), file_size ) );
  obj_file.close( );
  if( !ok )
    return( false );

  // Create stream
  std::istringstream obj_str( obj_buffer.data( ) );

  // Read line-by-line
  _TLines geometry;
  _TObjects objects;

  std::string line, cur_obj = "", cur_grp = "", cur_mat = "";
  while( std::getline( obj_str, line ) )
  {
    std::istringstream line_str( line );
    std::string cmd;
    line_str >> cmd;

    if( cmd == "v" || cmd == "vn" || cmd == "vt" )
      geometry.insert(
        std::make_pair( cmd, _TStreams( ) )
        ).first->second.push_back( std::istringstream( line ) );
    else if( cmd == "f" )
    {
      auto oIt = objects.insert( std::make_pair( cur_obj, _TLines( ) ) ).first;
      oIt->second.insert(
        std::make_pair( cur_grp, _TStreams( ) )
        ).first->second.push_back( std::istringstream( line ) );
    }
    else if( cmd == "o" ) line_str >> cur_obj;
    else if( cmd == "g" ) line_str >> cur_grp;
  } // end while

  auto vIt = geometry.find( "v" );
  if( vIt != geometry.end( ) )
    this->m_NumberOfVertices
      =
      this->_vertices( &( this->m_Vertices ), vIt->second );
  auto nIt = geometry.find( "vn" );
  if( nIt != geometry.end( ) )
    this->m_NumberOfNormals
      =
      this->_normals( &( this->m_Normals ), vIt->second );
  auto tIt = geometry.find( "vt" );
  if( tIt != geometry.end( ) )
    this->m_NumberOfTextures
      =
      this->_textures( &( this->m_Textures ), vIt->second );

  for( auto& o: objects )
  {
    for( auto& g: o.second )
    {
      std::vector< std::vector< std::string > > triangles_str, quads_str;
      for( auto& s: g.second )
      {
        std::string c, t;
        s >> c;
        std::vector< std::string > tok;
        while( s >> t )
          tok.push_back( t );
        if( tok.size( ) == 3 )
          triangles_str.push_back( tok );
        else if( tok.size( ) == 4 )
          quads_str.push_back( tok );
      } // end for

      TNatural* triangles = nullptr;
      TNatural* quads = nullptr;

      this->_faces( &triangles, 3, triangles_str );
      this->_faces( &quads, 4, quads_str );
      auto oIt
        =
        this->m_Objects.insert( std::make_pair( o.first, TGroups( ) ) ).first;
      auto gIt
        =
        oIt->second.insert( std::make_pair( g.first, TPolygons( ) ) ).first;
      if( triangles != nullptr )
        gIt->second.insert(
          std::make_pair(
            3, std::make_pair( triangles_str.size( ), triangles )
            )
          );
      if( quads != nullptr )
        gIt->second.insert(
          std::make_pair( 4, std::make_pair( quads_str.size( ), quads ) )
          );
    } // end for
  } // end for

  this->_update_bounding_box( );
  return( true );
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
set_image( PUJ_GL::Image* image )
{
  if( this->m_Image != nullptr )
    delete this->m_Image;
  this->m_Image = image;
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
draw( )
{
  const TReal* v = this->m_Vertices;
  const TReal* n = this->m_Normals;
  const TReal* t = this->m_Textures;
  const PUJ_GL::Image* i = this->m_Image;

  for( const auto& object: this->m_Objects )
  {
    for( const auto& group: object.second )
    {
      for( const auto& polygons: group.second )
      {
        TNatural n_faces = polygons.second.first;
        const TNatural* faces = polygons.second.second;
        if( n_faces > 0 && faces != nullptr )
        {
          size_t nF = n_faces * 3 * polygons.first;
          glBegin( ( polygons.first == 3 )? GL_TRIANGLES: GL_QUADS );
          {
            for( size_t f = 0; f < nF; f += 3 )
            {
              if( t != nullptr && i != nullptr )
              {
                const TReal* tc = t + ( 2 * ( faces[ f + 1 ] - 1 ) );
                const unsigned char* tv = ( *i )( tc[ 1 ], tc[ 0 ] );
                glColor3f(
                  TReal( tv[ 0 ] ) / TReal( 255 ),
                  TReal( tv[ 1 ] ) / TReal( 255 ),
                  TReal( tv[ 2 ] ) / TReal( 255 )
                  );
              } // end if
              if( n != nullptr )
                glNormal3fv( n + ( 3 * ( faces[ f + 1 ] - 1 ) ) );
              glVertex3fv( v + ( 3 * ( faces[ f ] - 1 ) ) );
            } // end for
          }
          glEnd( );
        } // end if
      } // end for
    } // end for
  } // end for
}

// -------------------------------------------------------------------------
template< class _TStreams >
size_t  PUJ_GL::Mesh::
_vertices( TReal** buffer, _TStreams& vertices )
{
  std::string c;
  TReal v;

  size_t nVerts = vertices.size( );
  *buffer
    =
    reinterpret_cast< TReal* >( std::calloc( nVerts * 3, sizeof( TReal ) ) );
  if( *buffer == nullptr )
    return( 0 );
  TReal* b = *buffer;
  for( std::istringstream& s: vertices )
  {
    s >> c;

    std::vector< TReal > values;
    while( s >> v )
      values.push_back( v );

    v = ( values.size( ) == 4 )? values[ 3 ]: TReal( 1 );
    *( b++ ) = ( ( values.size( ) > 0 )? values[ 0 ]: TReal( 0 ) ) / v;
    *( b++ ) = ( ( values.size( ) > 1 )? values[ 1 ]: TReal( 0 ) ) / v;
    *( b++ ) = ( ( values.size( ) > 2 )? values[ 2 ]: TReal( 0 ) ) / v;
  } // end for
  return( nVerts );
}

// -------------------------------------------------------------------------
template< class _TStreams >
size_t PUJ_GL::Mesh::
_normals( TReal** buffer, _TStreams& normals )
{
  std::string c;
  TReal v, n;

  size_t nNorms = normals.size( );
  *buffer
    =
    reinterpret_cast< TReal* >( std::calloc( nNorms * 3, sizeof( TReal ) ) );
  if( *buffer == nullptr )
    return( 0 );
  TReal* b = *buffer;
  for( std::istringstream& s: normals )
  {
    s >> c;

    std::vector< TReal > values;
    n = 0;
    while( s >> v )
    {
      n += v * v;
      values.push_back( v );
    } // end while
    n = std::sqrt( n );
    n = ( n != TReal( 0 ) )? n: TReal( 1 );
    *( b++ ) = ( ( values.size( ) > 0 )? values[ 0 ]: TReal( 0 ) ) / n;
    *( b++ ) = ( ( values.size( ) > 1 )? values[ 1 ]: TReal( 0 ) ) / n;
    *( b++ ) = ( ( values.size( ) > 2 )? values[ 2 ]: TReal( 0 ) ) / n;
  } // end for
  return( nNorms );
}

// -------------------------------------------------------------------------
template< class _TStreams >
size_t PUJ_GL::Mesh::
_textures( TReal** buffer, _TStreams& textures )
{
  std::string c;
  TReal v;

  size_t nTexts = textures.size( );
  *buffer
    =
    reinterpret_cast< TReal* >( std::calloc( nTexts * 2, sizeof( TReal ) ) );
  if( *buffer == nullptr )
    return( 0 );
  TReal* b = *buffer;
  for( std::istringstream& s: textures )
  {
    s >> c;

    std::vector< TReal > values;
    while( s >> v )
      values.push_back( v );

    *( b++ ) = ( values.size( ) > 0 )? values[ 0 ]: TReal( 0 );
    *( b++ ) = ( values.size( ) > 1 )? values[ 1 ]: TReal( 0 );
  } // end for
  return( nTexts );
}

// -------------------------------------------------------------------------
template< class _TFaces >
void PUJ_GL::Mesh::
_faces( TNatural** buffer, const TNatural& face_size, const _TFaces& faces )
{
  if( faces.size( ) == 0 )
    return;

  std::string c, t;
  TNatural vi;

  size_t nFaces = faces.size( );
  *buffer
    =
    reinterpret_cast< TNatural* >(
      std::calloc( nFaces * face_size * 3, sizeof( TNatural ) )
      );
  if( *buffer == nullptr )
    return;
  TNatural* b = *buffer;

  for( const auto& f: faces )
  {
    for( const auto& i: f )
    {
      TNatural n = 0;
      std::string d = i;
      for( auto& v: d )
      {
        if( v == '/' )
        {
          v = ' ';
          n += 1;
        } // end if
      } // end for

      std::istringstream str( d );
      std::vector< TNatural > idx;
      while( str >> vi )
        idx.push_back( vi );

      if( n == 0 )
      {
        *( b++ ) = idx[ 0 ];
        *( b++ ) = 0;
        *( b++ ) = 0;
      }
      else if( n == 1 )
      {
        *( b++ ) = idx[ 0 ];
        *( b++ ) = 0;
        *( b++ ) = idx[ 1 ];
      }
      else if( n == 2 )
      {
        if( idx.size( ) == 2 )
        {
          *( b++ ) = idx[ 0 ];
          *( b++ ) = idx[ 1 ];
          *( b++ ) = 0;
        }
        else if( idx.size( ) == 3 )
        {
          *( b++ ) = idx[ 0 ];
          *( b++ ) = idx[ 1 ];
          *( b++ ) = idx[ 2 ];
        } // end if
      } // end if
    } // end for
  } // end for
}

// -------------------------------------------------------------------------
void PUJ_GL::Mesh::
_update_bounding_box( )
{
  TReal* b = this->m_BoundingBox;
  TReal* v = this->m_Vertices;
  for( size_t i = 0; i < this->m_NumberOfVertices; i += 3 )
  {
    if( i > 0 )
    {
      for( short d = 0; d < 3; ++d )
      {
        short m = d << 1;
        short M = m + 1;
        b[ m ] = ( b[ m ] < v[ i + d ] )? b[ m ]: v[ i + d ];
        b[ M ] = ( v[ i + d ] < b[ M ] )? b[ M ]: v[ i + d ];
      } // end for
    }
    else
    {
      b[ 0 ] = b[ 1 ] = v[ i ];
      b[ 2 ] = b[ 3 ] = v[ i + 1 ];
      b[ 4 ] = b[ 5 ] = v[ i + 2 ];
    } // end if
  } // end for
}

// eof - Mesh.cxx
