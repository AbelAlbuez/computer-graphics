// =========================================================================
// @author Leonardo florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include "FrameBuffer.h"
#include <cmath>
#include <cstring>

// -------------------------------------------------------------------------
FrameBuffer::
FrameBuffer( const EMode& m )
  : m_W( 0 ),
    m_H( 0 ),
    m_B( nullptr ),
    m_M( m )
{
  if( this->m_M == Self::CMY )
    this->m_C = []( TChannel* c, const TReal* v ) -> void
      {
        for( TNatural i = 0; i < 3; ++i )
          c[ i ] = TChannel( ( TReal( 1 ) - v[ i ] ) * Self::s_M );
      };
  /* TODO
     else if( this->m_M == Self::HSV )
     else if( this->m_M == Self::HSL )
  */
  else // if( this->m_M == Self::RGB )
    this->m_C = []( TChannel* c, const TReal* v ) -> void
      {
        for( TNatural i = 0; i < 3; ++i )
          c[ i ] = TChannel( v[ i ] * Self::s_M );
      };
}

// -------------------------------------------------------------------------
FrameBuffer::
~FrameBuffer( )
{
  this->_free( );
}

// -------------------------------------------------------------------------
void FrameBuffer::
allocate( const TNatural& w, const TNatural& h )
{
  this->_free( );

  this->m_W = w;
  this->m_H = h;
  this->m_B
    =
    reinterpret_cast< TReal* >( std::calloc( w * h * 3, sizeof( TReal ) ) );
  this->fill( 0, 0, 0 );
}

// -------------------------------------------------------------------------
const FrameBuffer::
TNatural& FrameBuffer::
height( ) const
{
  return( this->m_H );
}

// -------------------------------------------------------------------------
const FrameBuffer::
TNatural& FrameBuffer::
width( ) const
{
  return( this->m_W );
}

// -------------------------------------------------------------------------
void FrameBuffer::
fill( const TReal& a, const TReal& b, const TReal& c )
{
  TNatural s = this->m_W * this->m_H * 3;
  for( TNatural i = 0; i < s; i += 3 )
  {
    this->m_B[ i ] = a;
    this->m_B[ i + 1 ] = b;
    this->m_B[ i + 2 ] = c;
  } // end for
}

// -------------------------------------------------------------------------
FrameBuffer::
TReal& FrameBuffer::
operator()( const TNatural& i, const TNatural& j, const TNatural& c )
{
  static TReal _z;
  if(
    0 <= i && i <= this->m_H &&
    0 <= j && j <= this->m_W &&
    0 <= c && c <= 3 &&
    this->m_B != nullptr
    )
  {
    TNatural idx = ( this->m_W * 3 * i ) + ( j * 3 ) + c;
    return( this->m_B[ idx ] );
  }
  else
  {
    _z = 0;
    return( _z );
  } // end if
}

// -------------------------------------------------------------------------
const FrameBuffer::
TReal& FrameBuffer::
operator()( const TNatural& i, const TNatural& j, const TNatural& c ) const
{
  static const TReal _z = 0;
  if(
    0 <= i && i <= this->m_H &&
    0 <= j && j <= this->m_W &&
    0 <= c && c <= 3 &&
    this->m_B != nullptr
    )
  {
    TNatural idx = ( this->m_W * 3 * i ) + ( j * 3 ) + c;
    return( this->m_B[ idx ] );
  }
  else
    return( _z );
}

// -------------------------------------------------------------------------
FrameBuffer::
TReal* FrameBuffer::
operator()( const TNatural& i, const TNatural& j )
{
  if(
    0 <= i && i <= this->m_H &&
    0 <= j && j <= this->m_W &&
    this->m_B != nullptr
    )
  {
    TNatural idx = ( this->m_W * 3 * i ) + ( j * 3 );
    return( this->m_B + idx );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
const FrameBuffer::
TReal* FrameBuffer::
operator()( const TNatural& i, const TNatural& j ) const
{
  if(
    0 <= i && i <= this->m_H &&
    0 <= j && j <= this->m_W &&
    this->m_B != nullptr
    )
  {
    TNatural idx = ( this->m_W * 3 * i ) + ( j * 3 );
    return( this->m_B + idx );
  }
  else
    return( nullptr );
}

// -------------------------------------------------------------------------
void FrameBuffer::
_free( )
{
  if( this->m_B != nullptr )
    std::free( this->m_B );
  this->m_B = nullptr;
}

// -------------------------------------------------------------------------
void FrameBuffer::
_to_stream( std::ostream& o ) const
{
  o
    << "P3" << std::endl
    << "# FrameBuffer" << std::endl
    << this->m_W << " " << this->m_H << std::endl
    << TNatural( std::numeric_limits< TChannel >::max( ) );

  TNatural s = this->m_W * this->m_H;
  TReal* b = this->m_B;
  TChannel c[ 3 ];

  for( TNatural i = 0; i < s; ++i, b += 3 )
  {
    if( i % this->m_W == 0 )
      o << std::endl;
    else
      o << "    ";
    this->m_C( c, b );
    o
      << TInteger( c[ 0 ] ) << " "
      << TInteger( c[ 1 ] ) << " "
      << TInteger( c[ 2 ] );
  } // end for
}

// eof - FrameBuffer.cxx
