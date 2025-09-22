// ========================================================================
// @author Leonardo Florez-Valencia  florez-l@javeriana.edu.co
// ========================================================================

#include "App.h"

int main( int argc, char** argv )
{
  App app( &argc, argv );
  app.init( );
  app.go( );

  return( EXIT_SUCCESS );
}

// eof - ShowOBJ.cxx
