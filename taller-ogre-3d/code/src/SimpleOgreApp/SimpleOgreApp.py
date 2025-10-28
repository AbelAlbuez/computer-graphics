## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## Modified by Abel - Taller 4: Enemigos Cilindros (VERSIÓN SIMPLE)
## -------------------------------------------------------------------------

import os, sys, vtk, random
cur_dir = os.path.dirname(os.path.abspath(__file__))
imp_dir = os.path.abspath(os.path.join(cur_dir, '../../lib'))
sys.path.append(imp_dir)
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

from GeometryFactory import GeometryFactory

class MyPowerfulCameraMan(OgreBites.CameraMan):
  def __init__(self, node):
    super(MyPowerfulCameraMan, self).__init__(node)
  # end def
# end class

class SimpleOgreApp(PUJ_Ogre.BaseApplication):

  m_CamMan = None
  m_ArenaSize = 50.0
  
  # Variables para enemigos (simple)
  m_Enemies = []           # Lista de diccionarios con info de cada enemigo
  m_SpawnTimer = 0.0
  m_SpawnInterval = 2.0    # Cada 2 segundos
  m_MaxEnemies = 15
  m_EnemyCounter = 0

  def __init__(self):
    super(SimpleOgreApp, self).__init__('FPS Game - Taller 4', '')
    self.m_ResourcesFile = os.path.join(cur_dir, 'resources.cfg')
  # end def

  def _loadScene(self):

    win = self.getRenderWindow()
    root = self.getRoot()
    root_node = self.m_SceneMgr.getRootSceneNode()

    # Cámara
    cam = self.m_SceneMgr.createCamera('MainCamera')
    cam.setNearClipDistance(0.005)
    cam.setAutoAspectRatio(True)

    camnode = root_node.createChildSceneNode()
    camnode.setPosition([0, 1.7, 15])
    camnode.lookAt([0, 0, 0], Ogre.Node.TS_WORLD)
    camnode.attachObject(cam)

    self.m_CamMan = MyPowerfulCameraMan(camnode)
    self.m_CamMan.setStyle(OgreBites.CS_FREELOOK)
    self.m_CamMan.setTopSpeed(10)
    self.m_CamMan.setFixedYaw(True)
    self.addInputListener(self.m_CamMan)

    vp = win.addViewport(cam)
    vp.setBackgroundColour(Ogre.ColourValue(0.9, 0.75, 0.5))

    # Luz
    light = self.m_SceneMgr.createLight('MainLight')
    light.setType(Ogre.Light.LT_DIRECTIONAL)
    lightNode = root_node.createChildSceneNode()
    lightNode.setDirection([-0.5, -1, -0.5])
    lightNode.attachObject(light)

    # Suelo
    plane = Ogre.Plane(0, 1, 0, 0.0)
    Ogre.MeshManager.getSingleton().createPlane(
        "ground", "General", plane,
        self.m_ArenaSize, self.m_ArenaSize,
        20, 20, True, 1, 5, 5, [0, 0, 1]
    )
    
    ent = self.m_SceneMgr.createEntity("GroundEntity", "ground")
    ent.setMaterialName("tierra")
    node = root_node.createChildSceneNode()
    node.attachObject(ent)

    print("=" * 60)
    print("TALLER 4 - ENEMIGOS CILINDROS")
    print("=" * 60)
    print("CONTROLES: WASD + Mouse | ESC para salir")
    print("Cilindros aparecen cada 2s y te persiguen")
    print("=" * 60)
  # end def

  def frameRenderingQueued(self, evt):
    r = super(SimpleOgreApp, self).frameRenderingQueued(evt)
    
    # Corregir cámara
    self._correctCamera()
    
    # Obtener posición del jugador
    player_pos = self.m_CamMan.getCamera().getPosition()
    
    # Sistema de spawning de enemigos
    delta_time = evt.timeSinceLastFrame
    self.m_SpawnTimer += delta_time
    
    if self.m_SpawnTimer >= self.m_SpawnInterval and len(self.m_Enemies) < self.m_MaxEnemies:
      self.m_SpawnTimer = 0.0
      self._spawnEnemy()
    # end if
    
    # Actualizar cada enemigo
    for enemy in self.m_Enemies:
      self._updateEnemy(enemy, player_pos, delta_time)
    # end for
    
    return r
  # end def

  def _spawnEnemy(self):
    """Crea un nuevo enemigo en un borde aleatorio"""
    
    # Posición aleatoria en borde
    half = self.m_ArenaSize / 2.0
    margin = 2.0
    side = random.choice(['north', 'south', 'east', 'west'])
    
    if side == 'north':
      x = random.uniform(-half + margin, half - margin)
      z = -half + margin
    elif side == 'south':
      x = random.uniform(-half + margin, half - margin)
      z = half - margin
    elif side == 'east':
      x = half - margin
      z = random.uniform(-half + margin, half - margin)
    else:  # west
      x = -half + margin
      z = random.uniform(-half + margin, half - margin)
    # end if
    
    # Crear cilindro
    root_node = self.m_SceneMgr.getRootSceneNode()
    cylinder = GeometryFactory.create_cylinder(
        self.m_SceneMgr,
        f"enemy_{self.m_EnemyCounter}",
        1.0,  # radio
        3.0,  # altura
        "pelota"
    )
    
    # Crear nodo
    node = root_node.createChildSceneNode()
    node.attachObject(cylinder)
    node.setPosition([x, 1.5, z])  # 1.5 para que se vea bien
    
    # Guardar info del enemigo
    enemy = {
        'id': self.m_EnemyCounter,
        'node': node,
        'x': x,
        'z': z,
        'speed': 3.0
    }
    
    self.m_Enemies.append(enemy)
    self.m_EnemyCounter += 1
    
    print(f"Enemigo #{self.m_EnemyCounter} spawneado en ({x:.1f}, {z:.1f})")
  # end def

  def _updateEnemy(self, enemy, player_pos, delta_time):
    """Actualiza posición de un enemigo para perseguir al jugador"""
    
    # Calcular dirección hacia jugador (solo en XZ)
    dx = player_pos.x - enemy['x']
    dz = player_pos.z - enemy['z']
    
    # Distancia
    dist = (dx*dx + dz*dz) ** 0.5
    
    # Si está muy cerca, no moverse
    if dist < 0.5:
      return
    # end if
    
    # Normalizar dirección
    dx = dx / dist
    dz = dz / dist
    
    # Aplicar velocidad
    enemy['x'] += dx * enemy['speed'] * delta_time
    enemy['z'] += dz * enemy['speed'] * delta_time
    
    # Actualizar nodo visual
    enemy['node'].setPosition([enemy['x'], 1.5, enemy['z']])
  # end def

  def _correctCamera(self):
    """Mantiene la cámara dentro del área"""
    if self.m_CamMan is None:
      return
    # end if
    
    pos = self.m_CamMan.getCamera().getPosition()
    
    # Altura fija
    pos.y = 1.7
    
    # Límites
    half = self.m_ArenaSize / 2.0
    
    if pos.x > half - 1:
      pos.x = half - 1
    elif pos.x < -half + 1:
      pos.x = -half + 1
    # end if
    
    if pos.z > half - 1:
      pos.z = half - 1
    elif pos.z < -half + 1:
      pos.z = -half + 1
    # end if
    
    self.m_CamMan.getCamera().setPosition(pos)
  # end def

# end class

def main(argv):
  app = SimpleOgreApp()
  app.go()
# end def

if __name__ == '__main__':
  main(sys.argv)
# end def

## eof - SimpleOgreApp.py