// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_GL__BaseApp__h__
#define __PUJ_GL__BaseApp__h__

#include <memory>
#include <GL/glut.h>

namespace PUJ_GL
{
  /**
   */
  class BaseApp
  {
  public:
    using Self = BaseApp;

  public:
    BaseApp(
      int* argc, char** argv, int mode,
      int w, int h,
      int x, int y,
      const std::string& window_title
      );
    virtual ~BaseApp( );

    virtual void init( );
    virtual void close( );
    virtual void go( );

  protected:
    virtual void _cb_display( );
    virtual void _cb_overlay_display( );
    virtual void _cb_reshape( int width, int height );
    virtual void _cb_keyboard( unsigned char key, int x, int y );
    virtual void _cb_mouse( int button, int state, int x, int y );
    virtual void _cb_motion( int x, int y );
    virtual void _cb_passive_motion( int x, int y );
    virtual void _cb_visibility( int state );
    virtual void _cb_entry( int state );
    virtual void _cb_special( int key, int x, int y );
    virtual void _cb_spaceball_motion( int x, int y, int z );
    virtual void _cb_spaceball_rotate( int x, int y, int z );
    virtual void _cb_spaceball_button( int button, int state );
    virtual void _cb_button_box( int button, int state );
    virtual void _cb_dials( int dial, int value );
    virtual void _cb_tablet_motion( int x, int y );
    virtual void _cb_tablet_button( int button, int state, int x, int y );
    virtual void _cb_menu_status( int status, int x, int y );
    virtual void _cb_menu_state( int status );
    virtual void _cb_idle( );
    virtual void _cb_timer(
      unsigned int msecs, void( *func )( int value ), int value
      );

  private:
    static void _scb_display( );
    static void _scb_overlay_display( );
    static void _scb_reshape( int width, int height );
    static void _scb_keyboard( unsigned char key, int x, int y );
    static void _scb_mouse( int button, int state, int x, int y );
    static void _scb_motion( int x, int y );
    static void _scb_passive_motion( int x, int y );
    static void _scb_visibility( int state );
    static void _scb_entry( int state );
    static void _scb_special( int key, int x, int y );
    static void _scb_spaceball_motion( int x, int y, int z );
    static void _scb_spaceball_rotate( int x, int y, int z );
    static void _scb_spaceball_button( int button, int state );
    static void _scb_button_box( int button, int state );
    static void _scb_dials( int dial, int value );
    static void _scb_tablet_motion( int x, int y );
    static void _scb_tablet_button( int button, int state, int x, int y );
    static void _scb_menu_status( int status, int x, int y );
    static void _scb_menu_state( int status );
    static void _scb_idle( );
    static void _scb_timer(
      unsigned int msecs, void( *func )( int value ), int value
      );

  protected:
    int m_WindowID { 0 };
    static std::unique_ptr< Self > s_Obj;
  };
} // end namespace

#endif // __PUJ_GL__BaseApp__h__

// eof - BaseApp.h
