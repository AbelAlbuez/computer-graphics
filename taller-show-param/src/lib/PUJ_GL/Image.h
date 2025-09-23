// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__Image__h__
#define __PUJ_GL__Image__h__

#include <PUJ_GL/Traits.h>

namespace PUJ_GL
{
  /**
   */
  class PUJ_GL_EXPORT Image
  {
    PUJ_GL_Traits;

  public:
    using Self = Image;

  public:
    Image( );
    virtual ~Image( );

    unsigned char* operator()(
      const unsigned int& r, const unsigned int& c
      );
    unsigned char& operator()(
      const unsigned int& r, const unsigned int& c, const unsigned short& d
      );
    unsigned char* operator()( const float& r, const float& c );
    const unsigned char* operator()(
      const unsigned int& r, const unsigned int& c
      ) const;
    const unsigned char& operator()(
      const unsigned int& r, const unsigned int& c, const unsigned short& d
      ) const;
    const unsigned char* operator()( const float& r, const float& c ) const;

    bool read_from_Netpbm( const std::string& filename );

  protected:
    void _clear( );
    void _skip_comments_Netbpm( std::istream& in );

  protected:
    unsigned int m_Width { 0 };
    unsigned int m_Height { 0 };
    unsigned short m_Channels { 0 };
    unsigned char* m_Data { nullptr };
  };
} // end namespace

#endif // __PUJ_GL__Image__h__

// eof - Image.h
