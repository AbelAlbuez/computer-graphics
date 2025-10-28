## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, random, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, '../../lib' ) )
sys.path.append( imp_dir )
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

"""
"""
class GeometricFPS( PUJ_Ogre.BaseApplicationWithVTK ):

  '''
  '''
  m_Ground = None
  m_Camera = None
  m_CamMan = None
  m_BadGuys = None
  m_AliveBadGuys = None
  m_AvailableNames = None

  '''
  '''
  def __init__( self ):
    super( GeometricFPS, self ).__init__( 'GeometricFPS v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
  # end def

  '''
  '''
  def _loadScene( self ):

    # Some objects
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )
    res_mgr = Ogre.ResourceGroupManager.getSingleton( )
    mesh_mgr = Ogre.MeshManager.getSingleton( )

    # Read scene descriptor
    scene_stream = res_mgr.openResource( 'scene.txt', 'General' )
    scene = dict( [ ( s.split( )[ 0 ], s.split( )[ 1 : ] ) for s in scene_stream.getAsString( ).splitlines( ) ] )
    scene_stream.close( )

    # Floor_limits
    self.m_Ground = [ -100.0, 100.0, -100.0, 100.0 ]
    if 'ground' in scene:
      self.m_Ground = [ float( v ) for v in scene[ 'ground' ] ]
    # end if
    self._ground( 'ground', self.m_Ground )

    # Camera
    self.m_Camera = [ 1e-3, 1.7, 1.0 ]
    if 'camera' in scene:
      self.m_Camera = [ float( v ) for v in scene[ 'camera' ] ]
    # end if
    cam = self._camera( self.m_Ground, self.m_Camera )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_POINT )
    light.setDiffuseColour( 1, 1, 1 )
    light_node = root_node.createChildSceneNode( )
    light_node.setPosition(
      ( self.m_Ground[ 1 ] + self.m_Ground[ 0 ] ) * 0.5,
      500 * self.m_Camera[ 1 ],
      ( self.m_Ground[ 3 ] + self.m_Ground[ 2 ] ) * 0.5
      )
    light_node.attachObject( light )

    # Viewport
    skycolor = [ 1, 1, 1 ]
    if 'skycolor' in scene:
      skycolor = [ float( v ) for v in scene[ 'skycolor' ] ]
    # end if
    vp = win.addViewport( cam )
    vp.setBackgroundColour( skycolor )

    # Load 'bad guys'
    self.m_BadGuys = { 'sphere' : None, 'cylinder' : None, 'cone' : None }
    self.m_AliveBadGuys = { 'sphere' : [], 'cylinder' : [], 'cone' : [] }
    self.m_AvailableNames = { 'sphere' : [], 'cylinder' : [], 'cone' : [] }
    if 'sphere' in scene:
      bad_guy_material = scene[ 'sphere' ][ -4 ]
      bad_guy_stamina = int( scene[ 'sphere' ][ -3 ] )
      bad_guy_spawn_prob = float( scene[ 'sphere' ][ -2 ] )
      bad_guy_max = int( scene[ 'sphere' ][ -1 ] )
      self.m_BadGuys[ 'sphere' ] = [ bad_guy_material, bad_guy_stamina, bad_guy_spawn_prob, bad_guy_max, self._sphere( float( scene[ 'sphere' ][ 0 ] ), 100, 100 ) ]
      self.m_AvailableNames[ 'sphere' ] = [ 'sphere_' + str( i ) for i in range( bad_guy_max ) ]
    # end if
  # end def

  '''
  '''
  def frameRenderingQueued( self, evt ):
    r = super( PUJ_Ogre.BaseApplication, self ).frameRenderingQueued( evt )

    # Create bad guys
    for k in self.m_BadGuys:
      if not self.m_BadGuys[ k ] is None:
        n_max = self.m_BadGuys[ k ][ 3 ]
        n_bad = len( self.m_AliveBadGuys[ k ] )
        p = random.uniform( 0, 1 )
        if p <= self.m_BadGuys[ k ][ 2 ] and n_bad < n_max:
          if len( self.m_AvailableNames[ k ] ) > 0:
            name = self.m_AvailableNames[ k ].pop( 0 )
            node = self._createManualObject(
              self.m_BadGuys[ k ][ 4 ], name, self.m_BadGuys[ k ][ 0 ]
              )
            pos = node.getAttachedObject( 0 ).getBoundingBox( ).getMinimum( )
            qos = Ogre.Vector3(
              random.uniform( self.m_Ground[ 0 ], self.m_Ground[ 1 ] ),
              pos.y * -1.0,
              random.uniform( self.m_Ground[ 2 ], self.m_Ground[ 3 ] )
              )
            node.setPosition( qos )
            self.m_AliveBadGuys[ k ] += [ node ]
          # end if
        # end if
      # end if
    # end for

    # Get camera position and force it to the ground
    pos = self.m_CamMan.getCamera( ).getPosition( )
    pos.y = self.m_Camera[ 1 ]
    self.m_CamMan.getCamera( ).setPosition( pos )

    # Move bad guys
    for k in self.m_AliveBadGuys:
      for n in self.m_AliveBadGuys[ k ]:
        d = ( ( pos - n.getPosition( ) ).normalisedCopy( ) ) * 1e-1
        n.translate( d )
      # end for
    # end for

    return r
  # end def

  '''
  '''
  def _ground( self, i, l ):
    c = [ ( l[ 1 ] + l[ 0 ] ) * 0.5, 0.0, ( l[ 3 ] + l[ 2 ] ) * 0.5 ]
    p = Ogre.Plane( 0, 1, 0, 0 )
    m = Ogre.MeshManager.getSingleton( ).createPlane(
      i, 'General', p,
      l[ 1 ] - l[ 0 ],
      l[ 3 ] - l[ 2 ],
      20, 20, True, 1, 5, 5, [ 0, 0, 1 ]
      )
    e = self.m_SceneMgr.createEntity( i, i )
    e.setMaterialName( i )
    n = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    n.attachObject( e )
    n.setPosition( c )
  # end def

  '''
  '''
  def _camera( self, l, p ):
    cam = self.m_SceneMgr.createCamera( 'camera' )
    cam.setNearClipDistance( p[ 0 ] )
    cam.setAutoAspectRatio( True )

    cam_node = self.m_SceneMgr.getRootSceneNode( ).createChildSceneNode( )
    cam_node.setPosition( l[ 0 ], p[ 1 ], l[ 1 ] )
    cam_node.lookAt( [ 0, 0, 0 ], Ogre.Node.TS_WORLD )
    cam_node.attachObject( cam )

    self.m_CamMan = OgreBites.CameraMan( cam_node )
    self.m_CamMan.setStyle( OgreBites.CS_FREELOOK )
    self.m_CamMan.setTopSpeed( 10 )
    self.m_CamMan.setFixedYaw( True )
    self.addInputListener( self.m_CamMan )

    return cam
  # end def


# end class

"""
"""
def main( argv ):
  app = GeometricFPS( )
  app.go( )
# end def

if __name__ == '__main__':
  main( sys.argv )
# end def

## eof - GeometricFPS.py
