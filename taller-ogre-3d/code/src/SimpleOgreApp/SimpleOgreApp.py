## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, sys, vtk
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, '../../lib' ) )
sys.path.append( imp_dir )
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

class MyPowerfulCameraMan( OgreBites.CameraMan ):
  def __init__( self, node ):
    super( MyPowerfulCameraMan, self ).__init__( node )
  # end def
# end class

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
    camnode.setPosition( [ 0, 1.7, 15 ] )

    camnode.lookAt( [ 0, 0, 0 ], Ogre.Node.TS_WORLD )
    camnode.attachObject( cam )

    self.m_CamMan = MyPowerfulCameraMan( camnode )
    self.m_CamMan.setStyle( OgreBites.CS_FREELOOK )
    self.m_CamMan.setTopSpeed( 10 )
    self.m_CamMan.setFixedYaw( True )
    self.addInputListener( self.m_CamMan )

    # Configure viewport
    vp = win.addViewport( cam )
    vp.setBackgroundColour( Ogre.ColourValue( 0.9, 0.75, 0.5 ) )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    light.setDirection( [ -0.5, -1, -0.5 ] )

    # Load a mesh
    ent = self.m_SceneMgr.createEntity( 'Sinbad', 'Sinbad.mesh' )
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
    node.setPosition( 0, 8, 0 )

    ent = self.m_SceneMgr.createEntity( 'C_Chusma', 'C_Chusma.mesh' )
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
    node.setPosition( 0, 1, 0 )

    ent = self.m_SceneMgr.createEntity( 'C_Chusma_LTra', 'C_Chusma_LTra.mesh' )
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
    node.setPosition( 0, -0.5, -1 )
    
    plane = Ogre.Plane( 0, 1, 0, 0.0 )
    planePtr = Ogre.MeshManager.getSingleton().createPlane(
        "ground",
        "General",
        plane,
        1500, 1500,
        20, 20,
        True,
        1,
        5, 5,
        [ 0, 0, 1 ]
       )
    ent = self.m_SceneMgr.createEntity("GroundEntity", "ground")
    ent.setMaterialName("tierra")
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
    
    vsphere = vtk.vtkSphereSource( )
    vsphere.SetRadius( 3 )
    vsphere.SetThetaResolution( 100 )
    vsphere.SetPhiResolution( 100 )
    vsphere.Update( )
    
    man = self.m_SceneMgr.createManualObject("target1")
    man.begin("pelota", Ogre.RenderOperation.OT_TRIANGLE_LIST)
    
    for i in range( vsphere.GetOutput( ).GetNumberOfPoints( ) ):
      pos = vsphere.GetOutput( ).GetPoint( i )
      man.position( pos )
    # end for

    for i in range( vsphere.GetOutput( ).GetNumberOfCells( ) ):
      cell = vsphere.GetOutput( ).GetCell( i )
      if cell.GetNumberOfPoints( ) == 3:
        man.triangle( cell.GetPointId( 0 ), cell.GetPointId( 1 ), cell.GetPointId( 2 ) )
      # end if
    # end for
    
    
    man.end( )
    node = root_node.createChildSceneNode( )
    node.attachObject( man )
    
  def _correctCamera( self ):
    pos = self.m_CamMan.getCamera( ).getPosition( )
    pos.y = 1.7
    self.m_CamMan.getCamera( ).setPosition( pos )
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
