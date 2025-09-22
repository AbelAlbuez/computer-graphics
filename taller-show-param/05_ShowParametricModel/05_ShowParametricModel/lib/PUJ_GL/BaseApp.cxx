// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_GL/BaseApp.h>

// -------------------------------------------------------------------------
std::unique_ptr< PUJ_GL::BaseApp > PUJ_GL::BaseApp::s_Obj = nullptr;

// -------------------------------------------------------------------------
PUJ_GL::BaseApp::
BaseApp(
  int* argc, char** argv, int mode,
  int w, int h,
  int x, int y,
  const std::string& window_title
  )
{
  if( Self::s_Obj == nullptr )
  {
    glutInit( argc, argv );
    glutInitDisplayMode( mode );
    glutInitWindowSize( w, h );
    glutInitWindowPosition( x, y );
    this->m_WindowID = glutCreateWindow( window_title.c_str( ) );
    Self::s_Obj.reset( this );
  } // end if
}

// -------------------------------------------------------------------------
PUJ_GL::BaseApp::
~BaseApp( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
init( )
{
  glutDisplayFunc( Self::_scb_display );
  glutOverlayDisplayFunc( Self::_scb_overlay_display );
  glutReshapeFunc( Self::_scb_reshape );
  glutKeyboardFunc( Self::_scb_keyboard );
  glutMouseFunc( Self::_scb_mouse );
  glutMotionFunc( Self::_scb_motion );
  glutPassiveMotionFunc( Self::_scb_passive_motion );
  glutVisibilityFunc( Self::_scb_visibility );
  glutEntryFunc( Self::_scb_entry );
  glutSpecialFunc( Self::_scb_special );
  glutSpaceballMotionFunc( Self::_scb_spaceball_motion );
  glutSpaceballRotateFunc( Self::_scb_spaceball_rotate );
  glutSpaceballButtonFunc( Self::_scb_spaceball_button );
  glutButtonBoxFunc( Self::_scb_button_box );
  glutDialsFunc( Self::_scb_dials );
  glutTabletMotionFunc( Self::_scb_tablet_motion );
  glutTabletButtonFunc( Self::_scb_tablet_button );
  glutMenuStatusFunc( Self::_scb_menu_status );
  glutMenuStateFunc( Self::_scb_menu_state );
  glutIdleFunc( Self::_scb_idle );
  // TODO: glutTimerFunc( Self::_scb_timer );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
close( )
{
  glutDestroyWindow( this->m_WindowID );
  this->m_WindowID = 0;
  Self::s_Obj.release( );
  Self::s_Obj.reset( );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
go( )
{
  glutMainLoop( );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_display( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_overlay_display( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_reshape( int width, int height )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_keyboard( unsigned char key, int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_mouse( int button, int state, int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_motion( int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_passive_motion( int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_visibility( int state )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_entry( int state )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_special( int key, int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_spaceball_motion( int x, int y, int z )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_spaceball_rotate( int x, int y, int z )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_spaceball_button( int button, int state )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_button_box( int button, int state )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_dials( int dial, int value )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_tablet_motion( int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_tablet_button( int button, int state, int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_menu_status( int status, int x, int y )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_menu_state( int status )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_idle( )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_cb_timer( unsigned int msecs, void( *func )( int value ), int value )
{
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_display( )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_display( );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_overlay_display( )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_overlay_display( );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_reshape( int width, int height )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_reshape( width, height );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_keyboard( unsigned char key, int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_keyboard( key, x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_mouse( int button, int state, int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_mouse( button, state, x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_motion( int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_motion( x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_passive_motion( int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_passive_motion( x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_visibility( int state )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_visibility( state );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_entry( int state )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_entry( state );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_special( int key, int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_special( key, x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_spaceball_motion( int x, int y, int z )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_spaceball_motion( x, y, z );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_spaceball_rotate( int x, int y, int z )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_spaceball_rotate( x, y, z );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_spaceball_button( int button, int state )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_spaceball_button( button, state );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_button_box( int button, int state )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_button_box( button, state );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_dials( int dial, int value )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_dials( dial, value );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_tablet_motion( int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_tablet_motion( x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_tablet_button( int button, int state, int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_tablet_button( button, state, x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_menu_status( int status, int x, int y )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_menu_status( status, x, y );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_menu_state( int status )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_menu_state( status );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_idle( )
{
  if( Self::s_Obj.get( ) != nullptr )
    Self::s_Obj->_cb_idle( );
}

// -------------------------------------------------------------------------
void PUJ_GL::BaseApp::
_scb_timer( unsigned int msecs, void( *func )( int value ), int value )
{
  /* TODO
     if( Self::s_Obj.get( ) != nullptr )
     Self::s_Obj->_cb_timer( msecs, func, value );
  */
}

// eof - BaseApp.cxx
