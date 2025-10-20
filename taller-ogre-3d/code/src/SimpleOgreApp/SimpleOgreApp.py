## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, '../../lib' ) )
sys.path.append( imp_dir )
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

"""
"""
class SimpleOgreApp( PUJ_Ogre.BaseApplication ):

  '''
  '''
  m_CamMan = None

  '''
  '''
  def __init__( self ):
    super( SimpleOgreApp, self ).__init__( 'SimpleOgreApp v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
  # end def

  '''
  '''
  def _loadScene( self ):

    # Get root and create scene manager
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )

    # Configure camera
    cam = self.m_SceneMgr.createCamera( 'MainCamera' )
    cam.setNearClipDistance( 0.005 )
    cam.setAutoAspectRatio( True )

    camnode = root_node.createChildSceneNode( )
    camnode.setPosition( [ 0, 0, 15 ] )

    camnode.lookAt( [ 0, 0, 0 ], Ogre.Node.TS_WORLD )
    camnode.attachObject( cam )

    self.m_CamMan = OgreBites.CameraMan( camnode )
    self.m_CamMan.setStyle( OgreBites.CS_ORBIT )
    self.m_CamMan.setTopSpeed( 3 )
    self.m_CamMan.setFixedYaw( True )
    self.addInputListener( self.m_CamMan )

    # Configure viewport
    vp = win.addViewport( cam )
    ## TODO: vp.setBackgroundColour( Ogre.ColourValue( 0.9, 0.75, 0.5 ) )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    light.setDirection( [ -0.5, -1, -0.5 ] )

    # Load a mesh
    ent = self.m_SceneMgr.createEntity( 'C_Chusma', 'C_Chusma.mesh' )
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
    node.setPosition( 0, 0, 0 )
  # end def

# end class

"""
"""
def main( argv ):
  app = SimpleOgreApp( )
  app.go( )
# end def

if __name__ == '__main__':
  main( sys.argv )
# end def

## eof - SimpleOgreApp.py
