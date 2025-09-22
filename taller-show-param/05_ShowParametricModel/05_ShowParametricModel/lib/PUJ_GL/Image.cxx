// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/Image.h>
#include <cstdlib>
#include <fstream>

// -------------------------------------------------------------------------
PUJ_GL::Image::
Image( )
{
}

// -------------------------------------------------------------------------
PUJ_GL::Image::
~Image( )
{
  this->_clear( );
}

// -------------------------------------------------------------------------
unsigned char* PUJ_GL::Image::
operator()( const unsigned int& r, const unsigned int& c )
{
  if( r < this->m_Height && c < this->m_Width )
  {
    unsigned long long i
      =
      ( r * this->m_Width * this->m_Channels ) + ( c * this->m_Channels );
    return( this->m_Data + i );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
unsigned char& PUJ_GL::Image::
operator()(
  const unsigned int& r, const unsigned int& c, const unsigned short& d
  )
{
  static unsigned char _z = 0;
  if( r < this->m_Height && c < this->m_Width && d < this->m_Channels )
  {
    unsigned long long i
      =
      ( r * this->m_Width * this->m_Channels ) + ( c * this->m_Channels ) + d;
    return( *( this->m_Data + i ) );
  }
  else
  {
    _z = 0;
    return( _z );
  } // end if
}

// -------------------------------------------------------------------------
unsigned char* PUJ_GL::Image::
operator()( const float& r, const float& c )
{
  if(
    float( 0 ) <= r && r <= float( 1 )
    &&
    float( 0 ) <= c && c <= float( 1 )
    )
  {
    return(
      this->operator()(
        ( unsigned int )( r * this->m_Height ),
        ( unsigned int )( c * this->m_Width )
        )
      );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
const unsigned char* PUJ_GL::Image::
operator()( const unsigned int& r, const unsigned int& c ) const
{
  if( r < this->m_Height && c < this->m_Width )
  {
    unsigned long long i
      =
      ( r * this->m_Width * this->m_Channels ) + ( c * this->m_Channels );
    return( this->m_Data + i );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
const unsigned char& PUJ_GL::Image::
operator()(
  const unsigned int& r, const unsigned int& c, const unsigned short& d
  ) const
{
  static const unsigned char _z = 0;
  if( r < this->m_Height && c < this->m_Width && d < this->m_Channels )
  {
    unsigned long long i
      =
      ( r * this->m_Width * this->m_Channels ) + ( c * this->m_Channels ) + d;
    return( *( this->m_Data + i ) );
  }
  else
    return( _z );
}

// -------------------------------------------------------------------------
const unsigned char* PUJ_GL::Image::
operator()( const float& r, const float& c ) const
{
  if(
    float( 0 ) <= r && r <= float( 1 )
    &&
    float( 0 ) <= c && c <= float( 1 )
    )
  {
    return(
      this->operator()(
        ( unsigned int )( r * ( this->m_Height - 1 ) ),
        ( unsigned int )( c * ( this->m_Width - 1 ) )
        )
      );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
bool PUJ_GL::Image::
read_from_Netpbm( const std::string& filename )
{
  this->_clear( );

  std::ifstream filestr( filename.c_str( ), std::ios::binary );
  if( !filestr )
    return( false );

  // Magic number
  std::string magic;
  filestr >> magic;
  if( magic.size( ) != 2 || magic[ 0 ] != 'P' )
    return( false );
  int type = magic[ 1 ] - '0';

  // Image dimensions
  this->_skip_comments_Netbpm( filestr );
  filestr >> this->m_Width;
  this->_skip_comments_Netbpm( filestr );
  filestr >> this->m_Height;

  // Maximum value
  unsigned short maxval = 1;
  if( type != 1 && type != 4 )
  {
    this->_skip_comments_Netbpm( filestr );
    filestr >> maxval;
  } // end if
  filestr.get( );
  float off = float( 255 ) / float( maxval );

  // Reserve data
  this->m_Channels = ( type == 3 || type == 6 )? 3: 1;
  unsigned long long S = this->m_Width * this->m_Height * this->m_Channels;
  this->m_Data
    =
    reinterpret_cast< unsigned char* >(
      std::calloc( S, sizeof( unsigned char ) )
      );

  // Read data
  if( type == 1 || type == 2 || type == 3 ) // ASCII formats
  {
    for( unsigned long long i = 0; i < S; i++ )
    {
      unsigned short val;
      filestr >> val;
      if( type == 1 )
        this->m_Data[ i ] = ( val != 0 )? 0: 255;
      else
        this->m_Data[ i ] = ( unsigned char )( off * float( val ) );
    } // end for
  } // end if
  else // Binary formats
  {
    if( type == 4 ) // PBM binary
    { 
      unsigned int rowBytes = ( this->m_Width + 7 ) / 8;
      unsigned char* row
        =
        reinterpret_cast< unsigned char* >(
          std::calloc( rowBytes, sizeof( unsigned char ) )
          );

      for( unsigned int y = 0; y < this->m_Height; ++y )
      {
        filestr.read( reinterpret_cast< char* >( row ), rowBytes );
        for( unsigned int x = 0; x < this->m_Width; ++x )
        {
          unsigned int byteIndex = x / 8;
          unsigned int bitIndex = 7 - ( x % 8 );
          bool bit = ( row[ byteIndex ] >> bitIndex ) & 1;
          this->m_Data[ ( y * this->m_Width ) + x ] = ( bit )? 0: 255;
        } // end for
      } // end for

      std::free( row );
    }
    else if( type == 5 || type == 6 ) // PGM/PPM binary
    {
      filestr.read( reinterpret_cast< char* >( this->m_Data ), S );
      if( maxval != 255 )
      {
        for( unsigned long long i = 0; i < S; ++i )
          this->m_Data[ i ]
            =
            ( unsigned char )( off * float( this->m_Data[ i ] ) );
      } // end if
    } // end if
  } // end if
  return( true );
}

// -------------------------------------------------------------------------
void PUJ_GL::Image::
_clear( )
{
  if( this->m_Data != nullptr )
    std::free( this->m_Data );
  this->m_Width = 0;
  this->m_Height = 0;
  this->m_Channels = 0;
  this->m_Data = nullptr;
}

// -------------------------------------------------------------------------
void PUJ_GL::Image::
_skip_comments_Netbpm( std::istream& in )
{
  char c;
  while( in >> std::ws && in.peek( ) == '#' )
  {
    std::string line;
    std::getline( in, line );
  } // end while
}

// eof - Image.cxx
