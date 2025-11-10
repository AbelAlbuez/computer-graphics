## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, sys
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, './lib' ) )
sys.path.append( imp_dir )
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

"""
"""
class MovingSpheres( PUJ_Ogre.BaseApplicationWithVTK ):

  '''
  '''
  m_MovingBodies = {}
  m_StaticBodies = {}

  '''
  '''
  def __init__( self ):
    super( MovingSpheres, self ).__init__( 'MovingSpheres v0.1', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )
  # end def

  '''
  '''
  def _loadScene( self ):

    # Prepare Bullet
    pybullet.connect( pybullet.DIRECT )
    pybullet.setGravity( 0, -9.8, 0 )

    # Get root and create scene manager
    win = self.getRenderWindow( )
    root = self.getRoot( )
    root_node = self.m_SceneMgr.getRootSceneNode( )

    # Configure camera
    self._createCamera(
      top_speed = 3,
      position = [ 0, 1.70, 5.00 ],
      look_at = [ 0, 1.70, 0 ],
      background = [ 0.9, 0.75, 0.5 ],
      cam_style = OgreBites.CS_FREELOOK
      )

    # Light
    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    light.setDirection( [ 0, -1, 0 ] )

    # A ground
    self._ground( 'ground', [ -2.00, 2.00, -2.00, 2.00 ] )
    ground_bullet = pybullet.createCollisionShape( pybullet.GEOM_PLANE, planeNormal = [ 0, 1, 0 ] )
    ground_body = pybullet.createMultiBody( 0, ground_bullet, -1, [ 0, 0, 0 ] )
    pybullet.changeDynamics( ground_body, -1, restitution = 1, lateralFriction = 0.8 )
    self.m_StaticBodies[ 'ground' ] = ground_body

    # Load billiards
    red_ball = self._createManualObject(
      self._sphere( 0.057, 50, 50 ), 'red_ball', 'red_material'
      )
    red_ball.setPosition( 0, 1.70, 0 )
    red_ball_bullet = pybullet.createCollisionShape( pybullet.GEOM_SPHERE, radius = 0.057 )
    red_ball_body = pybullet.createMultiBody( 0.017, red_ball_bullet, -1, [ 0, 1.70, 0 ] )
    pybullet.changeDynamics( red_ball_body, -1, restitution = 0.5, lateralFriction = 0.3 )
    self.m_MovingBodies[ 'red_ball' ] = ( red_ball, red_ball_body )

    # Finish pybullet configuration
    pybullet.setPhysicsEngineParameter( numSolverIterations = 10 )
  # end def

  '''
  '''
  def frameRenderingQueued( self, evt ):
    r = super( PUJ_Ogre.BaseApplicationWithVTK, self ).frameRenderingQueued( evt )
    pybullet.setTimeStep( evt.timeSinceLastFrame )
    pybullet.stepSimulation( )

    for k in self.m_MovingBodies:
      node, nId = self.m_MovingBodies[ k ]
      pos, orn = pybullet.getBasePositionAndOrientation( nId )
      node.setPosition( pos )
      node.setOrientation( Ogre.Quaternion( orn[ 3 ], orn[ 0 ], orn[ 1 ], orn[ 2 ] ) )
    # end for

    return r
  # end def


# end class

"""
"""
def main( argv ):
  app = MovingSpheres( )
  app.go( )
# end def

if __name__ == '__main__':
  main( sys.argv )
# end def

## eof - MovingSpheres.py
