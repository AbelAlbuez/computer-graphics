// =========================================================================
// @author Leonardo florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __FrameBuffer__h__
#define __FrameBuffer__h__

#include <cstdint>
#include <functional>
#include <limits>
#include <ostream>

/**
 */
class FrameBuffer
{
public:
  using Self     = FrameBuffer;
  using TNatural = std::uint32_t;
  using TInteger = std::int32_t;
  using TReal    = float;
  using TChannel = std::uint8_t;

  using TColorFunction = std::function< void( TChannel*, const TReal* ) >;

  enum EMode
  {
    RGB = 0,
    CMY,
    HSV,
    HSL
  };

public:
  FrameBuffer( const EMode& m = Self::RGB );
  virtual ~FrameBuffer( );

  void allocate( const TNatural& w, const TNatural& h );

  const TNatural& height( ) const;
  const TNatural& width( ) const;

  void fill( const TReal& a, const TReal& b, const TReal& c );

  TReal& operator()(
    const TNatural& i, const TNatural& j, const TNatural& c
    );
  const TReal& operator()(
    const TNatural& i, const TNatural& j, const TNatural& c
    ) const;

  TReal* operator()( const TNatural& i, const TNatural& j );
  const TReal* operator()( const TNatural& i, const TNatural& j ) const;

protected:
  void _free( );
  void _to_stream( std::ostream& o ) const;

protected:
  TNatural m_W { 0 };
  TNatural m_H { 0 };
  TReal*   m_B { nullptr };
  EMode    m_M { Self::RGB };

  TColorFunction m_C;

  static constexpr TReal s_M = TReal( std::numeric_limits< TChannel >::max( ) );

public:
  friend std::ostream& operator<<( std::ostream& o, const FrameBuffer& b )
    {
      b._to_stream( o );
      return( o );
    }
};

#endif // __FrameBuffer__h__

// eof - FrameBuffer.h
