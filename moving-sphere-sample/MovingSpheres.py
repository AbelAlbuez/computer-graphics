## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------

import os, sys, random
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, './lib' ) )
sys.path.append( imp_dir )
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

class MovingSpheres( PUJ_Ogre.BaseApplicationWithVTK ):

  m_MovingBodies = {}
  m_StaticBodies = {}
  
  # Configuracion
  altura_caida = 3.0
  tiempo_entre_esferas = 0.5
  limites_plano = [ -3.00, 3.00, -3.00, 3.00 ]
  
  contador_esferas = 0
  tiempo_acumulado = 0.0

  def __init__( self ):
    super( MovingSpheres, self ).__init__( 'Simulador Caída Libre', '' )
    self.m_ResourcesFile = os.path.join( cur_dir, 'resources.cfg' )

  def _loadScene( self ):
    pybullet.connect( pybullet.DIRECT )
    pybullet.setGravity( 0, -9.8, 0 )

    root_node = self.m_SceneMgr.getRootSceneNode( )

    self._createCamera(
      top_speed = 3,
      position = [ 0, 2.00, 6.00 ],
      look_at = [ 0, 1.50, 0 ],
      background = [ 0.5, 0.7, 0.9 ],
      cam_style = OgreBites.CS_ORBIT
      )

    light = self.m_SceneMgr.createLight( 'MainLight' )
    light.setType( Ogre.Light.LT_DIRECTIONAL )
    lightNode = root_node.createChildSceneNode( )
    lightNode.setDirection( [ 0, -1, 0 ] )
    lightNode.attachObject( light )

    self._ground( 'ground', self.limites_plano )
    ground_bullet = pybullet.createCollisionShape( pybullet.GEOM_PLANE, planeNormal = [ 0, 1, 0 ] )
    ground_body = pybullet.createMultiBody( 0, ground_bullet, -1, [ 0, 0, 0 ] )
    pybullet.changeDynamics( ground_body, -1, restitution = 0.8, lateralFriction = 0.6 )
    self.m_StaticBodies[ 'ground' ] = ground_body

    pybullet.setPhysicsEngineParameter( numSolverIterations = 10 )
    
    print( "\n=== SIMULADOR DE CAÍDA LIBRE ===" )
    print( f"Altura de caída: {self.altura_caida} m" )
    print( f"Plano: {self.limites_plano}" )
    print( "Las esferas caerán infinitamente" )
    print( "Presiona ESC para salir\n" )

  def _generarEsfera( self ):
    nombre = f'esfera_{self.contador_esferas}'
    
    x = random.uniform( self.limites_plano[0] + 0.3, self.limites_plano[1] - 0.3 )
    z = random.uniform( self.limites_plano[2] + 0.3, self.limites_plano[3] - 0.3 )
    y = self.altura_caida
    
    materiales = [ 'red_material', 'green_material', 'yellow_material', 'white_material' ]
    material = random.choice( materiales )
    
    esfera_node = self._createManualObject(
      self._sphere( 0.1, 30, 30 ), 
      nombre, 
      material
      )
    esfera_node.setPosition( x, y, z )
    
    esfera_bullet = pybullet.createCollisionShape( pybullet.GEOM_SPHERE, radius = 0.1 )
    esfera_body = pybullet.createMultiBody( 0.1, esfera_bullet, -1, [ x, y, z ] )
    pybullet.changeDynamics( esfera_body, -1, restitution = 0.7, lateralFriction = 0.5 )
    
    self.m_MovingBodies[ nombre ] = ( esfera_node, esfera_body )
    
    print( f"Esfera {self.contador_esferas} en ({x:.2f}, {y:.2f}, {z:.2f})" )
    self.contador_esferas += 1

  def frameRenderingQueued( self, evt ):
    r = super( PUJ_Ogre.BaseApplicationWithVTK, self ).frameRenderingQueued( evt )
    pybullet.setTimeStep( evt.timeSinceLastFrame )
    pybullet.stepSimulation( )

    self.tiempo_acumulado += evt.timeSinceLastFrame
    if self.tiempo_acumulado >= self.tiempo_entre_esferas:
      self._generarEsfera( )
      self.tiempo_acumulado = 0.0

    for nombre, (node, body_id) in self.m_MovingBodies.items( ):
      pos, orn = pybullet.getBasePositionAndOrientation( body_id )
      node.setPosition( pos )
      node.setOrientation( Ogre.Quaternion( orn[ 3 ], orn[ 0 ], orn[ 1 ], orn[ 2 ] ) )

    return r


def main( argv ):
  app = MovingSpheres( )
  app.go( )

if __name__ == '__main__':
  main( sys.argv )

## eof - MovingSpheres.py