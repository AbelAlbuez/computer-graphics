## -------------------------------------------------------------------------
## @author Abel Albuez & Ricardo Cruz (Taller 4 - Versión Final v1.1)
## Based on GeometricFPS by Leonardo Florez-Valencia
## -------------------------------------------------------------------------
## MEJORAS v1.1:
## 1. Colisiones activadas - proyectiles destruyen enemigos ✅
## 2. Texto de reinicio al perder ✅
## 3. Score visible en pantalla (daño recibido) ✅
## -------------------------------------------------------------------------

import os, random, sys, math
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
  m_MouseCursor = None
  m_MouseX = 0.5
  m_MouseY = 0.5
  m_PlayerHealth = 3
  m_MaxHealth = 3
  m_GameOver = False
  m_HealthBar = None
  m_Score = 0
  m_DamageTaken = 0  # Nuevo: contador de daño recibido
  m_KillEffects = []
  m_LastHealthPrint = 0.0
  m_GameOverText = None  # Texto de Game Over
  m_ScoreText = None
  m_DamageText = None  # Texto de daño recibido

  def __init__(self):
    PUJ_Ogre.BaseApplicationWithVTK.__init__(self, 'GeometricFPS v1.1 FINAL', '')
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

    # Luz principal
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
    
    # Crear cursor del mouse (esfera pequeña brillante)
    self._createMouseCursor()
    
    # Crear HUD (barra de vida, puntuación y daño)
    self._createHUD()

    # Enemigos - Esferas
    self.m_Enemies = {'sphere': None, 'cylinder': None}
    self.m_AliveEnemies = {'sphere': [], 'cylinder': []}
    self.m_AvailableNames = {'sphere': [], 'cylinder': []}
    
    # Configurar esferas
    if 'sphere' in scene:
      radius = float(scene['sphere'][0])
      material = scene['sphere'][1]
      stamina = 1  # CAMBIADO: 1 HP para que mueran de un disparo
      spawn_prob = float(scene['sphere'][3])
      max_enemies = int(scene['sphere'][4])
      self.m_Enemies['sphere'] = [material, stamina, spawn_prob, max_enemies, 
                                    self._sphere(radius, 100, 100), radius]
      self.m_AvailableNames['sphere'] = ['sphere_' + str(i) for i in range(max_enemies)]
      print(f"[+] Sphere enemies: radius={radius}, max={max_enemies}, spawn_prob={spawn_prob}, HP={stamina}")
    # end if
    
    # Configurar cilindros
    if 'cylinder' in scene:
      radius = float(scene['cylinder'][0])
      height = float(scene['cylinder'][1])
      material = scene['cylinder'][2]
      stamina = 1  # CAMBIADO: 1 HP para que mueran de un disparo
      spawn_prob = float(scene['cylinder'][4])
      max_enemies = int(scene['cylinder'][5])
      self.m_Enemies['cylinder'] = [material, stamina, spawn_prob, max_enemies, 
                                     self._cylinder(radius, height, 50, 50), radius]
      self.m_AvailableNames['cylinder'] = ['cylinder_' + str(i) for i in range(max_enemies)]
      print(f"[+] Cylinder enemies: radius={radius}, height={height}, max={max_enemies}, HP={stamina}")
    # end if
    
    # Proyectiles
    self.m_ProjectileNames = ['proj_' + str(i) for i in range(100)]
    print("[+] Scene loaded successfully!")
    print("[+] Collisions ENABLED - projectiles destroy enemies!")
  # end def

  def keyPressed(self, evt):
    """Capturar teclas - especialmente R para reiniciar"""
    if evt.keysym.sym == OgreBites.SDLK_r and self.m_GameOver:
      # REINICIAR JUEGO
      print("\n[RESTART] Reiniciando juego...")
      self._restartGame()
      return True
    return True
  # end def

  def mousePressed(self, evt):
    if self.m_GameOver:
      return True
    
    if evt.button == OgreBites.BUTTON_LEFT and len(self.m_ProjectileNames) > 0:
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
    
    # Disparar desde la cámara hacia adelante
    cam_node = self.m_CamMan.getCamera()
    cam_pos = cam_node.getPosition()
    
    # Dirección hacia adelante
    forward = Ogre.Vector3(0, 0, -1)
    world_forward = cam_node._getDerivedOrientation() * forward
    
    name = self.m_ProjectileNames.pop(0)
    # Proyectil visible (radio 0.5)
    node = self._createManualObject(self._sphere(0.5, 20, 20), name, 'projectile')
    
    # Posición inicial: adelante de la cámara
    start_pos = cam_pos + (world_forward * 2.0)
    node.setPosition(start_pos)
    
    self.m_Projectiles += [{'node': node, 'dir': world_forward, 'life': 5.0, 'name': name}]
    
    print(f"\n[SHOOT] Projectile created at {start_pos} | Active: {len(self.m_Projectiles)} | Available: {len(self.m_ProjectileNames)}")
  # end def

  def _restartGame(self):
    """Reiniciar el juego completo"""
    try:
      # Resetear variables de juego
      self.m_PlayerHealth = self.m_MaxHealth
      self.m_Score = 0
      self.m_DamageTaken = 0
      self.m_GameOver = False
      
      # Limpiar todos los proyectiles
      for p in self.m_Projectiles[:]:
        self._destroyProjectile(p)
      
      # Limpiar todos los enemigos
      for k in self.m_AliveEnemies:
        for enemy in self.m_AliveEnemies[k][:]:
          self._destroyEnemy(enemy, k)
      
      # Limpiar efectos
      for effect in self.m_KillEffects[:]:
        try:
          self.m_SceneMgr.destroyManualObject(effect['name'])
          effect['node'].getParentSceneNode().removeChild(effect['node'])
          self.m_SceneMgr.destroySceneNode(effect['node'])
        except:
          pass
      self.m_KillEffects = []
      
      # Ocultar texto de Game Over
      if self.m_GameOverText:
        try:
          self.m_GameOverText.hide()
        except:
          pass
      
      # Resetear posición de cámara
      cam_node = self.m_CamMan.getCamera()
      cam_node.setPosition(0, self.m_Camera[1], 50)
      
      # Actualizar HUD
      self._updateHUD()
      
      print("[RESTART] ¡Juego reiniciado! Buena suerte!")
      
    except Exception as e:
      print(f"[ERROR] Error al reiniciar: {e}")
  # end def

  def frameRenderingQueued(self, evt):
    r = super(PUJ_Ogre.BaseApplication, self).frameRenderingQueued(evt)
    dt = evt.timeSinceLastFrame
    
    # Actualizar HUD cada frame
    self._updateHUD()
    
    # Imprimir estado cada segundo
    self.m_LastHealthPrint += dt
    if self.m_LastHealthPrint >= 1.0:
      hearts = "❤️" * self.m_PlayerHealth + "💔" * (self.m_MaxHealth - self.m_PlayerHealth)
      print(f"[HP] {hearts} | Score: {self.m_Score} | Damage: {self.m_DamageTaken} | Enemies: {sum(len(v) for v in self.m_AliveEnemies.values())}", end='\r')
      self.m_LastHealthPrint = 0.0
    
    # Si el jugador murió, mostrar Game Over
    if self.m_GameOver:
      self._showGameOver()
      return r

    # Obtener posición de cámara
    cam_node = self.m_CamMan.getCamera()
    pos = cam_node.getPosition()

    # Crear enemigos - ESFERAS
    if self.m_Enemies['sphere'] is not None:
      n_max = self.m_Enemies['sphere'][3]
      n_bad = len(self.m_AliveEnemies['sphere'])
      p = random.uniform(0, 1)
      if p <= self.m_Enemies['sphere'][2] and n_bad < n_max:
        if len(self.m_AvailableNames['sphere']) > 0:
          name = self.m_AvailableNames['sphere'].pop(0)
          node = self._createManualObject(self.m_Enemies['sphere'][4], name, self.m_Enemies['sphere'][0])
          bb = node.getAttachedObject(0).getBoundingBox()
          min_pos = bb.getMinimum()
          qos = Ogre.Vector3(
            random.uniform(self.m_Ground[0], self.m_Ground[1]),
            min_pos.y * -1.0,
            random.uniform(self.m_Ground[2], self.m_Ground[3])
          )
          node.setPosition(qos)
          self.m_AliveEnemies['sphere'] += [{
            'node': node, 
            'name': name, 
            'type': 'sphere',
            'radius': self.m_Enemies['sphere'][5],
            'health': self.m_Enemies['sphere'][1]
          }]
        # end if
      # end if
    # end if

    # Crear enemigos - CILINDROS
    if self.m_Enemies['cylinder'] is not None:
      n_max = self.m_Enemies['cylinder'][3]
      n_bad = len(self.m_AliveEnemies['cylinder'])
      p = random.uniform(0, 1)
      if p <= self.m_Enemies['cylinder'][2] and n_bad < n_max:
        if len(self.m_AvailableNames['cylinder']) > 0:
          name = self.m_AvailableNames['cylinder'].pop(0)
          node = self._createManualObject(self.m_Enemies['cylinder'][4], name, self.m_Enemies['cylinder'][0])
          bb = node.getAttachedObject(0).getBoundingBox()
          min_pos = bb.getMinimum()
          qos = Ogre.Vector3(
            random.uniform(self.m_Ground[0], self.m_Ground[1]),
            min_pos.y * -1.0,
            random.uniform(self.m_Ground[2], self.m_Ground[3])
          )
          node.setPosition(qos)
          self.m_AliveEnemies['cylinder'] += [{
            'node': node, 
            'name': name, 
            'type': 'cylinder',
            'radius': self.m_Enemies['cylinder'][5],
            'health': self.m_Enemies['cylinder'][1]
          }]
        # end if
      # end if
    # end if

    # Actualizar cámara (mantener altura)
    pos.y = self.m_Camera[1]
    cam_node.setPosition(pos)

    # Mover enemigos hacia el jugador (8.0 u/s)
    for k in self.m_AliveEnemies:
      for enemy in self.m_AliveEnemies[k]:
        n = enemy['node']
        d = ((pos - n.getPosition()).normalisedCopy()) * 8.0 * dt
        n.translate(d)
      # end for
    # end for

    # Mover proyectiles
    dead_projectiles = []
    for p in self.m_Projectiles:
      p['node'].translate(p['dir'] * 60.0 * dt)
      p['life'] -= dt
      if p['life'] <= 0:
        dead_projectiles += [p]
    # end for

    # Eliminar proyectiles muertos
    for p in dead_projectiles:
      self._destroyProjectile(p)
    # end for

    # ===============================================
    # COLISIONES ACTIVADAS - Proyectil vs Enemigo
    # ===============================================
    projectiles_checked = 0
    enemies_checked = 0
    collisions_detected = 0
    
    for p in self.m_Projectiles[:]:
      p_pos = p['node'].getPosition()
      hit = False
      projectiles_checked += 1
      
      for k in self.m_AliveEnemies:
        for enemy in self.m_AliveEnemies[k][:]:
          e_pos = enemy['node'].getPosition()
          enemies_checked += 1
          
          # Colisión esférica OPTIMIZADA
          dist_sq = (p_pos - e_pos).squaredLength()
          dist = math.sqrt(dist_sq)  # Para debug
          collision_radius = enemy['radius'] + 1.5  # AUMENTADO: Radio más grande para facilitar colisiones
          
          # Debug cada 60 frames (~1 segundo)
          if hasattr(self, 'm_DebugCounter'):
            self.m_DebugCounter += 1
          else:
            self.m_DebugCounter = 0
          
          if self.m_DebugCounter >= 60 and enemies_checked == 1:
            print(f"\n[DEBUG] Checking collision: dist={dist:.2f}, threshold={collision_radius:.2f}")
            self.m_DebugCounter = 0
          
          if dist_sq < (collision_radius * collision_radius):
            # ¡COLISIÓN! Reducir vida del enemigo
            enemy['health'] -= 1
            collisions_detected += 1
            print(f"\n[COLLISION] Distance: {dist:.2f} < {collision_radius:.2f} - HIT!")
            
            if enemy['health'] <= 0:
              # Enemigo muerto - crear efecto visual
              self._createKillEffect(e_pos)
              self.m_Score += 10 if k == 'sphere' else 15
              print(f"[KILL] {enemy['type']} destroyed! +{10 if k == 'sphere' else 15} pts | Total score: {self.m_Score}")
              
              # Eliminar enemigo
              self._destroyEnemy(enemy, k)
            else:
              print(f"[HIT] {enemy['type']} hit! HP: {enemy['health']}")
            # end if
            
            # Eliminar proyectil
            if p in self.m_Projectiles:
              self._destroyProjectile(p)
            hit = True
            break
          # end if
        # end for
        if hit:
          break
      # end for
    # end for

    # COLISIONES - Enemigo vs Jugador
    cam_pos = pos
    for k in self.m_AliveEnemies:
      for enemy in self.m_AliveEnemies[k][:]:
        e_pos = enemy['node'].getPosition()
        
        # Colisión esférica OPTIMIZADA
        dist_sq = (cam_pos - e_pos).squaredLength()
        collision_radius = enemy['radius'] + 1.0
        
        if dist_sq < (collision_radius * collision_radius):
          # Jugador recibe daño
          self.m_PlayerHealth -= 1
          self.m_DamageTaken += 1  # Incrementar contador de daño
          print(f"\n[DAMAGE] Golpeado por {enemy['type']}! Vida: {self.m_PlayerHealth}/{self.m_MaxHealth} | Daño total: {self.m_DamageTaken}")
          
          # Eliminar enemigo que golpeó
          self._destroyEnemy(enemy, k)
          
          # Verificar muerte
          if self.m_PlayerHealth <= 0:
            self.m_GameOver = True
            print("\n" + "="*60)
            print(f"¡GAME OVER! Score final: {self.m_Score} | Daño recibido: {self.m_DamageTaken}")
            print("="*60 + "\n")
          # end if
        # end if
      # end for
    # end for

    # Actualizar efectos visuales
    dead_effects = []
    for effect in self.m_KillEffects:
      effect['life'] -= dt
      effect['scale'] += dt * 2.0
      effect['node'].setScale([effect['scale']] * 3)
      
      # Fade out
      if effect['life'] <= 0:
        dead_effects += [effect]
    # end for
    
    # Eliminar efectos terminados
    for effect in dead_effects:
      try:
        self.m_SceneMgr.destroyManualObject(effect['name'])
        effect['node'].getParentSceneNode().removeChild(effect['node'])
        self.m_SceneMgr.destroySceneNode(effect['node'])
      except:
        pass
      self.m_KillEffects.remove(effect)
    # end for

    return r
  # end def

  def _destroyProjectile(self, p):
    """Eliminar proyectil de forma segura"""
    try:
      self.m_SceneMgr.destroyManualObject(p['name'])
      p['node'].getParentSceneNode().removeChild(p['node'])
      self.m_SceneMgr.destroySceneNode(p['node'])
      if p in self.m_Projectiles:
        self.m_Projectiles.remove(p)
      self.m_ProjectileNames += [p['name']]
    except:
      pass
  # end def

  def _destroyEnemy(self, enemy, enemy_type):
    """Eliminar enemigo de forma segura"""
    try:
      name = enemy['name']
      node = enemy['node']
      self.m_SceneMgr.destroyManualObject(name)
      node.getParentSceneNode().removeChild(node)
      self.m_SceneMgr.destroySceneNode(node)
      self.m_AliveEnemies[enemy_type].remove(enemy)
      self.m_AvailableNames[enemy_type] += [name]
    except:
      pass
  # end def

  def _createKillEffect(self, position):
    """Crear efecto visual cuando se mata un enemigo"""
    try:
      effect_name = f'effect_{len(self.m_KillEffects)}_{random.randint(0,9999)}'
      node = self._createManualObject(self._sphere(0.3, 10, 10), effect_name, 'projectile')
      node.setPosition(position)
      
      self.m_KillEffects += [{
        'node': node,
        'name': effect_name,
        'life': 0.5,
        'scale': 1.0
      }]
    except:
      pass
  # end def

  def _createMouseCursor(self):
    """Crear cursor 3D del mouse (esfera pequeña brillante)"""
    try:
      cursor = self._createManualObject(self._sphere(0.15, 12, 12), 'mouse_cursor', 'projectile')
      self.m_MouseCursor = cursor
      print("[+] Mouse cursor created (bright sphere)")
    except Exception as e:
      print(f"[!] Mouse cursor failed: {e}")
  # end def
  
  def _updateMouseCursor(self):
    """Actualizar posición del cursor 3D según movimiento del mouse"""
    if self.m_MouseCursor is None:
      return
    
    try:
      cam_node = self.m_CamMan.getCamera()
      cam = self.m_SceneMgr.getCamera('camera')
      
      # Crear rayo desde la cámara hacia el mouse
      ray = cam.getCameraToViewportRay(self.m_MouseX, self.m_MouseY)
      
      # Posicionar cursor a distancia fija (15 unidades)
      distance = 15.0
      cursor_pos = ray.getOrigin() + ray.getDirection() * distance
      
      self.m_MouseCursor.setPosition(cursor_pos)
    except:
      pass
  # end def

  def _createHUD(self):
    """Crear interfaz de usuario completa"""
    try:
      overlay_mgr = Ogre.OverlayManager.getSingleton()
      
      # Overlay principal
      hud_overlay = overlay_mgr.create('HUDOverlay')
      
      # BARRA DE VIDA - Fondo negro
      health_bg = overlay_mgr.createOverlayElement('Panel', 'HealthBG')
      health_bg.setMetricsMode(Ogre.GMM_PIXELS)
      health_bg.setPosition(10, 10)
      health_bg.setDimensions(320, 50)
      health_bg.setMaterialName('BaseWhite')
      health_bg.setColour(Ogre.ColourValue(0.2, 0.2, 0.2, 0.8))
      
      # BARRA DE VIDA - Verde
      health_bar = overlay_mgr.createOverlayElement('Panel', 'HealthBar')
      health_bar.setMetricsMode(Ogre.GMM_PIXELS)
      health_bar.setPosition(15, 15)
      health_bar.setDimensions(310, 40)
      health_bar.setMaterialName('BaseWhite')
      health_bar.setColour(Ogre.ColourValue(0, 1, 0, 1))
      
      # TEXTO DE PUNTUACIÓN
      score_text = overlay_mgr.createOverlayElement('TextArea', 'ScoreText')
      score_text.setMetricsMode(Ogre.GMM_PIXELS)
      score_text.setPosition(10, 70)
      score_text.setDimensions(300, 30)
      score_text.setParameter('font_name', 'BlueHighway')
      score_text.setParameter('char_height', '24')
      score_text.setColour(Ogre.ColourValue(1, 1, 1, 1))
      score_text.setCaption('Score: 0')
      
      # TEXTO DE DAÑO RECIBIDO
      damage_text = overlay_mgr.createOverlayElement('TextArea', 'DamageText')
      damage_text.setMetricsMode(Ogre.GMM_PIXELS)
      damage_text.setPosition(10, 100)
      damage_text.setDimensions(300, 30)
      damage_text.setParameter('font_name', 'BlueHighway')
      damage_text.setParameter('char_height', '24')
      damage_text.setColour(Ogre.ColourValue(1, 0.3, 0.3, 1))  # Rojo para daño
      damage_text.setCaption('Damage: 0')
      
      # Agregar elementos al overlay
      hud_overlay.add2D(health_bg)
      hud_overlay.add2D(health_bar)
      hud_overlay.add2D(score_text)
      hud_overlay.add2D(damage_text)
      hud_overlay.show()
      
      self.m_HealthBar = health_bar
      self.m_ScoreText = score_text
      self.m_DamageText = damage_text
      
      print("[+] HUD created (health + score + damage)")
    except Exception as e:
      print(f"[!] HUD creation failed: {e}")
      print("[+] Stats in console only")
  # end def
  
  def _showGameOver(self):
    """Mostrar pantalla de Game Over con instrucciones de reinicio"""
    if self.m_GameOverText is None:
      try:
        overlay_mgr = Ogre.OverlayManager.getSingleton()
        
        # Crear overlay de Game Over
        gameover_overlay = overlay_mgr.create('GameOverOverlay')
        
        # Panel semi-transparente de fondo
        bg_panel = overlay_mgr.createOverlayElement('Panel', 'GameOverBG')
        bg_panel.setMetricsMode(Ogre.GMM_RELATIVE)
        bg_panel.setPosition(0, 0)
        bg_panel.setDimensions(1, 1)
        bg_panel.setMaterialName('BaseWhite')
        bg_panel.setColour(Ogre.ColourValue(0, 0, 0, 0.7))
        
        # Texto GAME OVER
        title_text = overlay_mgr.createOverlayElement('TextArea', 'GameOverTitle')
        title_text.setMetricsMode(Ogre.GMM_PIXELS)
        win = self.getRenderWindow()
        title_text.setPosition(win.getWidth() / 2 - 150, win.getHeight() / 2 - 100)
        title_text.setDimensions(400, 50)
        title_text.setParameter('font_name', 'BlueHighway')
        title_text.setParameter('char_height', '48')
        title_text.setColour(Ogre.ColourValue(1, 0, 0, 1))
        title_text.setCaption('GAME OVER')
        
        # Texto de estadísticas
        stats_text = overlay_mgr.createOverlayElement('TextArea', 'GameOverStats')
        stats_text.setMetricsMode(Ogre.GMM_PIXELS)
        stats_text.setPosition(win.getWidth() / 2 - 150, win.getHeight() / 2 - 30)
        stats_text.setDimensions(400, 30)
        stats_text.setParameter('font_name', 'BlueHighway')
        stats_text.setParameter('char_height', '24')
        stats_text.setColour(Ogre.ColourValue(1, 1, 1, 1))
        stats_text.setCaption(f'Score: {self.m_Score} | Damage: {self.m_DamageTaken}')
        
        # Texto de instrucciones de reinicio
        restart_text = overlay_mgr.createOverlayElement('TextArea', 'GameOverRestart')
        restart_text.setMetricsMode(Ogre.GMM_PIXELS)
        restart_text.setPosition(win.getWidth() / 2 - 200, win.getHeight() / 2 + 20)
        restart_text.setDimensions(500, 30)
        restart_text.setParameter('font_name', 'BlueHighway')
        restart_text.setParameter('char_height', '20')
        restart_text.setColour(Ogre.ColourValue(0, 1, 0, 1))
        restart_text.setCaption('Press [R] to Restart')
        
        # Texto de salida
        quit_text = overlay_mgr.createOverlayElement('TextArea', 'GameOverQuit')
        quit_text.setMetricsMode(Ogre.GMM_PIXELS)
        quit_text.setPosition(win.getWidth() / 2 - 200, win.getHeight() / 2 + 50)
        quit_text.setDimensions(500, 30)
        quit_text.setParameter('font_name', 'BlueHighway')
        quit_text.setParameter('char_height', '20')
        quit_text.setColour(Ogre.ColourValue(1, 1, 0, 1))
        quit_text.setCaption('Press [ESC] to Quit')
        
        # Agregar al overlay
        gameover_overlay.add2D(bg_panel)
        gameover_overlay.add2D(title_text)
        gameover_overlay.add2D(stats_text)
        gameover_overlay.add2D(restart_text)
        gameover_overlay.add2D(quit_text)
        gameover_overlay.show()
        
        self.m_GameOverText = gameover_overlay
        
        print("\n[GAME OVER] Presiona R para reiniciar o ESC para salir")
      except Exception as e:
        print(f"[!] Game Over screen failed: {e}")
        print("\n[GAME OVER] Presiona R para reiniciar o ESC para salir (consola)")
  # end def
  
  def _updateHUD(self):
    """Actualizar interfaz de usuario cada frame"""
    if self.m_HealthBar is None:
      return
    
    try:
      # Calcular porcentaje de vida
      health_percent = max(0, self.m_PlayerHealth / self.m_MaxHealth)
      
      # Actualizar ancho de la barra
      new_width = 310 * health_percent
      self.m_HealthBar.setDimensions(new_width, 40)
      
      # Cambiar color según vida
      if health_percent > 0.66:
        color = Ogre.ColourValue(0, 1, 0, 1)  # Verde
      elif health_percent > 0.33:
        color = Ogre.ColourValue(1, 1, 0, 1)  # Amarillo
      else:
        color = Ogre.ColourValue(1, 0, 0, 1)  # Rojo
      
      self.m_HealthBar.setColour(color)
      
      # Actualizar puntuación
      if hasattr(self, 'm_ScoreText') and self.m_ScoreText:
        self.m_ScoreText.setCaption(f'Score: {self.m_Score}')
      
      # Actualizar daño recibido
      if hasattr(self, 'm_DamageText') and self.m_DamageText:
        self.m_DamageText.setCaption(f'Damage: {self.m_DamageTaken}')
    except:
      pass
  # end def

  def _cylinder(self, radius, height, u=20, v=20):
    """Generar geometría de cilindro usando VTK"""
    import vtk
    
    cylinder_source = vtk.vtkCylinderSource()
    cylinder_source.SetRadius(radius)
    cylinder_source.SetHeight(height)
    cylinder_source.SetResolution(u)
    cylinder_source.Update()
    
    normals = vtk.vtkPolyDataNormals()
    normals.SetInputConnection(cylinder_source.GetOutputPort())
    normals.Update()
    
    mesh = normals.GetOutput()
    
    P = []
    N = []
    T = []
    
    for i in range(mesh.GetNumberOfPoints()):
      point = mesh.GetPoint(i)
      P.append(point)
      
      normal = [0, 0, 0]
      if mesh.GetPointData().GetNormals():
        normal = mesh.GetPointData().GetNormals().GetTuple(i)
      N.append(normal)
      
      T.append((point[0] * 0.5 + 0.5, point[2] * 0.5 + 0.5))
    
    C = []
    for i in range(mesh.GetNumberOfCells()):
      cell = mesh.GetCell(i)
      cell_points = []
      for j in range(cell.GetNumberOfPoints()):
        cell_points.append(cell.GetPointId(j))
      C.append(cell_points)
    
    return (P, N, T, C)
  # end def

  def _ground(self, i, l):
    """Crear suelo texturizado"""
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
    """Configurar cámara FPS"""
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

## eof - GeometricFPS_FINAL_v1.1.py