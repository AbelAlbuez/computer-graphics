## -------------------------------------------------------------------------
## @author Abel Albuez & Ricardo Cruz (Taller 4)
## Based on GeometricFPS by Leonardo Florez-Valencia
## -------------------------------------------------------------------------

import os, random, sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
imp_dir = os.path.abspath(os.path.join(cur_dir, '../../lib'))
sys.path.append(imp_dir)
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

class GeometricFPS(PUJ_Ogre.BaseApplicationWithVTK, OgreBites.InputListener):

  m_Ground = None
  m_Camera = None
  m_CamMan = None
  m_Enemies = None
  m_AliveEnemies = None
  m_AvailableNames = None
  m_Projectiles = []
  m_ProjectileNames = []
  m_MouseCursor = None  # Cursor visual del mouse
  m_MouseX = 0.5
  m_MouseY = 0.5
  m_PlayerHealth = 3  # Vida del jugador
  m_MaxHealth = 3
  m_GameOver = False
  m_HealthBar = None  # Barra de vida visual

  def __init__(self):
    PUJ_Ogre.BaseApplicationWithVTK.__init__(self, 'GeometricFPS v0.2', '')
    OgreBites.InputListener.__init__(self)
    self.m_ResourcesFile = os.path.join(cur_dir, 'resources.cfg')
  # end def

  def _loadScene(self):
    win = self.getRenderWindow()
    root_node = self.m_SceneMgr.getRootSceneNode()
    res_mgr = Ogre.ResourceGroupManager.getSingleton()

    # Leer configuración
    scene_stream = res_mgr.openResource('scene.txt', 'General')
    scene = dict([(s.split()[0], s.split()[1:]) for s in scene_stream.getAsString().splitlines()])
    scene_stream.close()

    # Suelo
    self.m_Ground = [-100.0, 100.0, -100.0, 100.0]
    if 'ground' in scene:
      self.m_Ground = [float(v) for v in scene['ground']]
    self._ground('ground', self.m_Ground)

    # Cámara
    self.m_Camera = [1e-3, 1.7, 1.0]
    if 'camera' in scene:
      self.m_Camera = [float(v) for v in scene['camera']]
    cam = self._camera(self.m_Ground, self.m_Camera)

    # Luz
    light = self.m_SceneMgr.createLight('MainLight')
    light.setType(Ogre.Light.LT_POINT)
    light.setDiffuseColour(1, 1, 1)
    light_node = root_node.createChildSceneNode()
    light_node.setPosition(
      (self.m_Ground[1] + self.m_Ground[0]) * 0.5,
      500 * self.m_Camera[1],
      (self.m_Ground[3] + self.m_Ground[2]) * 0.5
    )
    light_node.attachObject(light)

    # Viewport
    skycolor = [1, 1, 1]
    if 'skycolor' in scene:
      skycolor = [float(v) for v in scene['skycolor']]
    vp = win.addViewport(cam)
    vp.setBackgroundColour(skycolor)
    
    # Crear mira en el centro
    self._createCrosshair()
    
    # Crear cursor del mouse (esfera pequeña)
    self._createMouseCursor()
    
    # Crear barra de vida
    self._createHealthBar()

    # Enemigos
    self.m_Enemies = {'sphere': None}
    self.m_AliveEnemies = {'sphere': []}
    self.m_AvailableNames = {'sphere': []}
    
    if 'sphere' in scene:
      material = scene['sphere'][-4]
      stamina = int(scene['sphere'][-3])
      spawn_prob = float(scene['sphere'][-2])
      max_enemies = int(scene['sphere'][-1])
      self.m_Enemies['sphere'] = [material, stamina, spawn_prob, max_enemies, 
                                    self._sphere(float(scene['sphere'][0]), 100, 100)]
      self.m_AvailableNames['sphere'] = ['sphere_' + str(i) for i in range(max_enemies)]
    # end if
    
    # Proyectiles
    self.m_ProjectileNames = ['proj_' + str(i) for i in range(100)]
  # end def

  def mousePressed(self, evt):
    if evt.button == OgreBites.BUTTON_LEFT and len(self.m_ProjectileNames) > 0:
      print(f"[SHOOT] Projectiles available: {len(self.m_ProjectileNames)}")
      self._shoot()
    return True
  # end def
  
  def mouseMoved(self, evt):
    # Actualizar posición del cursor (normalizado 0-1)
    win = self.getRenderWindow()
    self.m_MouseX = evt.x / win.getWidth()
    self.m_MouseY = evt.y / win.getHeight()
    self._updateMouseCursor()
    return True
  # end def

  def _shoot(self):
    if len(self.m_ProjectileNames) == 0:
      print("[SHOOT] No projectiles available!")
      return
    
    # SIMPLE: Disparar desde la cámara hacia adelante
    cam_node = self.m_CamMan.getCamera()
    cam_pos = cam_node.getPosition()
    
    # Dirección hacia adelante del nodo de cámara
    forward = Ogre.Vector3(0, 0, -1)
    world_forward = cam_node._getDerivedOrientation() * forward
    
    name = self.m_ProjectileNames.pop(0)
    # Proyectil grande y visible (radio 0.8)
    node = self._createManualObject(self._sphere(0.8, 20, 20), name, 'bad_guy1')
    
    # Posición inicial: un poco adelante de la cámara
    start_pos = cam_pos + (world_forward * 2.0)
    node.setPosition(start_pos)
    
    self.m_Projectiles += [{'node': node, 'dir': world_forward, 'life': 3.0, 'name': name}]
    print(f"[SHOOT] PEW! Projectile #{len(self.m_Projectiles)}")
  # end def

  def frameRenderingQueued(self, evt):
    r = super(PUJ_Ogre.BaseApplication, self).frameRenderingQueued(evt)
    dt = evt.timeSinceLastFrame
    
    # Imprimir vida cada segundo
    if not hasattr(self, 'm_LastHealthPrint'):
      self.m_LastHealthPrint = 0.0
    self.m_LastHealthPrint += dt
    
    if self.m_LastHealthPrint >= 1.0:
      hearts = "❤️" * self.m_PlayerHealth + "💔" * (self.m_MaxHealth - self.m_PlayerHealth)
      print(f"[HP] {hearts} ({self.m_PlayerHealth}/{self.m_MaxHealth})", end='\r')
      self.m_LastHealthPrint = 0.0
    
    # Si el jugador murió, terminar juego
    if self.m_GameOver:
      print("\n" + "="*50)
      print("GAME OVER - Presiona ESC para salir")
      print("="*50)
      return r

    # Crear enemigos
    for k in self.m_Enemies:
      if not self.m_Enemies[k] is None:
        n_max = self.m_Enemies[k][3]
        n_bad = len(self.m_AliveEnemies[k])
        p = random.uniform(0, 1)
        if p <= self.m_Enemies[k][2] and n_bad < n_max:
          if len(self.m_AvailableNames[k]) > 0:
            name = self.m_AvailableNames[k].pop(0)
            node = self._createManualObject(self.m_Enemies[k][4], name, self.m_Enemies[k][0])
            pos = node.getAttachedObject(0).getBoundingBox().getMinimum()
            qos = Ogre.Vector3(
              random.uniform(self.m_Ground[0], self.m_Ground[1]),
              pos.y * -1.0,
              random.uniform(self.m_Ground[2], self.m_Ground[3])
            )
            node.setPosition(qos)
            self.m_AliveEnemies[k] += [node]
          # end if
        # end if
      # end if
    # end for

    # Actualizar cámara
    pos = self.m_CamMan.getCamera().getPosition()
    pos.y = self.m_Camera[1]
    self.m_CamMan.getCamera().setPosition(pos)

    # Mover enemigos (más rápido: 8.0 u/s)
    for k in self.m_AliveEnemies:
      for n in self.m_AliveEnemies[k]:
        d = ((pos - n.getPosition()).normalisedCopy()) * 8.0 * dt
        n.translate(d)
      # end for
    # end for

    # Mover proyectiles
    dead = []
    for p in self.m_Projectiles:
      p['node'].translate(p['dir'] * 50.0 * dt)
      p['life'] -= dt
      if p['life'] <= 0:
        dead += [p]
    # end for

    # Eliminar proyectiles muertos
    for p in dead:
      self.m_SceneMgr.destroyManualObject(p['name'])
      p['node'].getParentSceneNode().removeChild(p['node'])
      self.m_SceneMgr.destroySceneNode(p['node'])
      self.m_Projectiles.remove(p)
      self.m_ProjectileNames += [p['name']]
    # end for

    # Colisiones
    for p in self.m_Projectiles:
      p_pos = p['node'].getPosition()
      for k in self.m_AliveEnemies:
        for e in self.m_AliveEnemies[k][:]:
          e_pos = e.getPosition()
          dist = (p_pos - e_pos).length()
          if dist < 2.0:
            # Eliminar enemigo
            name = e.getAttachedObject(0).getName()
            self.m_SceneMgr.destroyManualObject(name)
            e.getParentSceneNode().removeChild(e)
            self.m_SceneMgr.destroySceneNode(e)
            self.m_AliveEnemies[k].remove(e)
            self.m_AvailableNames[k] += [name]
            
            # Eliminar proyectil
            self.m_SceneMgr.destroyManualObject(p['name'])
            p['node'].getParentSceneNode().removeChild(p['node'])
            self.m_SceneMgr.destroySceneNode(p['node'])
            if p in self.m_Projectiles:
              self.m_Projectiles.remove(p)
            self.m_ProjectileNames += [p['name']]
            break
          # end if
        # end for
      # end for
    # end for

    # Detectar colisión enemigos con jugador
    cam_pos = pos
    for k in self.m_AliveEnemies:
      for e in self.m_AliveEnemies[k][:]:
        e_pos = e.getPosition()
        dist = (cam_pos - e_pos).length()
        if dist < 2.0:  # Enemigo tocó al jugador
          self.m_PlayerHealth -= 1
          print(f"[DAMAGE] Golpeado! Vida: {self.m_PlayerHealth}/{self.m_MaxHealth}")
          self._updateHealthBar()
          
          # Eliminar enemigo que golpeó
          name = e.getAttachedObject(0).getName()
          self.m_SceneMgr.destroyManualObject(name)
          e.getParentSceneNode().removeChild(e)
          self.m_SceneMgr.destroySceneNode(e)
          self.m_AliveEnemies[k].remove(e)
          self.m_AvailableNames[k] += [name]
          
          # Verificar muerte
          if self.m_PlayerHealth <= 0:
            self.m_GameOver = True
            print("\n" + "="*50)
            print("¡HAS MUERTO!")
            print("="*50 + "\n")
          # end if
        # end if
      # end for
    # end for

    return r
  # end def

  def _createMouseCursor(self):
    # Crear esfera MUY pequeña para el cursor (0.1 unidades)
    root_node = self.m_SceneMgr.getRootSceneNode()
    cursor = self._createManualObject(self._sphere(0.1, 8, 8), 'mouse_cursor', 'bad_guy1')
    self.m_MouseCursor = cursor
    print("[+] Mouse cursor created (small sphere)")
  # end def
  
  def _updateMouseCursor(self):
    if self.m_MouseCursor is None:
      return
    
    # Obtener cámara correctamente
    cam_node = self.m_CamMan.getCamera()
    cam = self.m_SceneMgr.getCamera('camera')
    
    # Crear rayo desde la cámara hacia el mouse
    ray = cam.getCameraToViewportRay(self.m_MouseX, self.m_MouseY)
    
    # Posicionar cursor a distancia fija (10 unidades)
    distance = 10.0
    cursor_pos = ray.getOrigin() + ray.getDirection() * distance
    
    self.m_MouseCursor.setPosition(cursor_pos)
  # end def

  def _createHealthBar(self):
    try:
      overlay_mgr = Ogre.OverlayManager.getSingleton()
      
      # Crear overlay para la barra de vida
      health_overlay = overlay_mgr.create('HealthOverlay')
      
      # Barra de vida (roja con fondo)
      health_panel = overlay_mgr.createOverlayElement('Panel', 'HealthBar')
      health_panel.setMetricsMode(Ogre.GMM_PIXELS)
      health_panel.setPosition(10, 10)
      health_panel.setDimensions(300, 40)
      health_panel.setMaterialName('BaseWhite')
      health_panel.setColour(Ogre.ColourValue(0, 1, 0, 1))  # Verde inicial
      
      health_overlay.add2D(health_panel)
      health_overlay.show()
      
      self.m_HealthBar = health_panel
      print("[+] Health bar created (TOP-LEFT corner)")
    except Exception as e:
      print(f"[!] Health bar failed: {e}")
      # Crear esferas visuales de vida como alternativa
      self._createHealthSpheres()
    # end try
  # end def
  
  def _createHealthSpheres(self):
    """Crear esferas GRANDES rojas visibles para la vida"""
    try:
      root_node = self.m_SceneMgr.getRootSceneNode()
      self.m_HealthSpheres = []
      
      for i in range(3):
        # Crear nodo para cada esfera
        sphere_node = root_node.createChildSceneNode()
        sphere = self._createManualObject(
            self._sphere(2.0, 20, 20),  # GRANDES: radio 2.0
            f'health_sphere_{i}', 
            'bad_guy1'
        )
        sphere_node.attachObject(sphere)
        
        # Posición FIJA en el mundo (arriba a la izquierda)
        x = -25 + (i * 6)  # Separadas 6 unidades
        y = 12  # Muy arriba
        z = 0  # Centro en Z
        
        sphere_node.setPosition([x, y, z])
        self.m_HealthSpheres.append(sphere_node)
      # end for
      
      print("[+] Health spheres created: 3 BIG RED spheres (top-left)")
    except Exception as e:
      print(f"[!] Health spheres failed: {e}")
      print("[+] Health in CONSOLE only")
    # end try
  # end def
  
  def _updateHealthBar(self):
    if self.m_HealthBar is None:
      # Si no hay barra, actualizar esferas si existen
      if hasattr(self, 'm_HealthSpheres'):
        for i, sphere in enumerate(self.m_HealthSpheres):
          if i < self.m_PlayerHealth:
            sphere.setVisible(True)
          else:
            sphere.setVisible(False)
        # end for
      # end if
      return
    # end if
    
    try:
      # Calcular porcentaje de vida
      health_percent = self.m_PlayerHealth / self.m_MaxHealth
      
      # Actualizar ancho de la barra
      new_width = 300 * health_percent
      self.m_HealthBar.setDimensions(new_width, 40)
      
      # Cambiar color según vida
      if health_percent > 0.66:
        color = Ogre.ColourValue(0, 1, 0, 1)  # Verde
      elif health_percent > 0.33:
        color = Ogre.ColourValue(1, 1, 0, 1)  # Amarillo
      else:
        color = Ogre.ColourValue(1, 0, 0, 1)  # Rojo
      # end if
      
      self.m_HealthBar.setColour(color)
    except Exception as e:
      print(f"[!] Update health bar error: {e}")
    # end try
  # end def

  def _createCrosshair(self):
    try:
      overlay_mgr = Ogre.OverlayManager.getSingleton()
      overlay = overlay_mgr.create('CrosshairOverlay')
      
      panel = overlay_mgr.createOverlayElement('Panel', 'CrosshairPanel')
      panel.setMetricsMode(Ogre.GMM_PIXELS)
      win = self.getRenderWindow()
      panel.setPosition(win.getWidth() / 2 - 2, win.getHeight() / 2 - 2)
      panel.setDimensions(4, 4)
      panel.setMaterialName('BaseWhiteNoLighting')
      
      overlay.add2D(panel)
      overlay.show()
    except:
      # Si falla el overlay, solo imprimir en consola
      print("[+] Crosshair: Apunta con el centro de la pantalla")
    # end try
  # end def

  def _ground(self, i, l):
    c = [(l[1] + l[0]) * 0.5, 0.0, (l[3] + l[2]) * 0.5]
    p = Ogre.Plane(0, 1, 0, 0)
    m = Ogre.MeshManager.getSingleton().createPlane(
      i, 'General', p, l[1] - l[0], l[3] - l[2],
      20, 20, True, 1, 5, 5, [0, 0, 1]
    )
    e = self.m_SceneMgr.createEntity(i, i)
    e.setMaterialName(i)
    n = self.m_SceneMgr.getRootSceneNode().createChildSceneNode()
    n.attachObject(e)
    n.setPosition(c)
  # end def

  def _camera(self, l, p):
    cam = self.m_SceneMgr.createCamera('camera')
    cam.setNearClipDistance(p[0])
    cam.setAutoAspectRatio(True)

    cam_node = self.m_SceneMgr.getRootSceneNode().createChildSceneNode()
    cam_node.setPosition(l[0], p[1], l[1])
    cam_node.lookAt([0, 0, 0], Ogre.Node.TS_WORLD)
    cam_node.attachObject(cam)

    self.m_CamMan = OgreBites.CameraMan(cam_node)
    self.m_CamMan.setStyle(OgreBites.CS_FREELOOK)
    self.m_CamMan.setTopSpeed(10)
    self.m_CamMan.setFixedYaw(True)
    self.addInputListener(self.m_CamMan)
    self.addInputListener(self)

    return cam
  # end def
# end class

def main(argv):
  app = GeometricFPS()
  app.go()
# end def

if __name__ == '__main__':
  main(sys.argv)
# end def

## eof - GeometricFPS.py