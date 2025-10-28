## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## Modified for Taller 4 - FPS Game (Minimal changes version)
## -------------------------------------------------------------------------

import os, sys, vtk
cur_dir = os.path.dirname(os.path.abspath(__file__))
imp_dir = os.path.abspath(os.path.join(cur_dir, '../../lib'))
sys.path.append(imp_dir)
import Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

class MyPowerfulCameraMan(OgreBites.CameraMan):
  def __init__(self, node):
    super(MyPowerfulCameraMan, self).__init__(node)
  # end def
# end class

"""
FPS Game - Taller 4
"""
class SimpleOgreApp(PUJ_Ogre.BaseApplication):

  '''
  Camera controller
  '''
  m_CamMan = None
  
  '''
  NUEVAS VARIABLES PARA EL JUEGO
  '''
  m_ArenaSize = 50.0  # Tamaño del área de juego

  '''
  Constructor
  '''
  def __init__(self):
    super(SimpleOgreApp, self).__init__('SimpleOgreApp v0.1', '')
    self.m_ResourcesFile = os.path.join(cur_dir, 'resources.cfg')
  # end def

  '''
  Load scene
  '''
  def _loadScene(self):

    # Get root and create scene manager
    win = self.getRenderWindow()
    root = self.getRoot()
    root_node = self.m_SceneMgr.getRootSceneNode()

    # ========================================
    # CONFIGURACIÓN DE CÁMARA (ORIGINAL)
    # ========================================
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

    # Configure viewport
    vp = win.addViewport(cam)
    vp.setBackgroundColour(Ogre.ColourValue(0.9, 0.75, 0.5))

    # ========================================
    # LUZ (ORIGINAL)
    # ========================================
    light = self.m_SceneMgr.createLight('MainLight')
    light.setType(Ogre.Light.LT_DIRECTIONAL)
    lightNode = root_node.createChildSceneNode()
    lightNode.setDirection([-0.5, -1, -0.5])
    lightNode.attachObject(light)

    # ========================================
    # SUELO - MODIFICADO: Arena más pequeña
    # ========================================
    plane = Ogre.Plane(0, 1, 0, 0.0)
    Ogre.MeshManager.getSingleton().createPlane(
        "ground",
        "General",
        plane,
        self.m_ArenaSize, self.m_ArenaSize,  # <- CAMBIO: 50x50 en vez de 1500x1500
        20, 20,
        True,
        1,
        5, 5,
        [0, 0, 1]
    )
    
    ent = self.m_SceneMgr.createEntity("GroundEntity", "ground")
    ent.setMaterialName("tierra")
    node = root_node.createChildSceneNode()
    node.attachObject(ent)

    # ========================================
    # OBJETOS DE PRUEBA (SIMPLIFICADO)
    # Solo una esfera en el centro para referencia
    # ========================================
    vsphere = vtk.vtkSphereSource()
    vsphere.SetRadius(3)
    vsphere.SetThetaResolution(100)
    vsphere.SetPhiResolution(100)
    vsphere.Update()
    
    man = self.m_SceneMgr.createManualObject("target1")
    man.begin("pelota", Ogre.RenderOperation.OT_TRIANGLE_LIST)
    
    for i in range(vsphere.GetOutput().GetNumberOfPoints()):
      pos = vsphere.GetOutput().GetPoint(i)
      man.position(pos)
    # end for

    for i in range(vsphere.GetOutput().GetNumberOfCells()):
      cell = vsphere.GetOutput().GetCell(i)
      if cell.GetNumberOfPoints() == 3:
        man.triangle(
          cell.GetPointId(0), 
          cell.GetPointId(1), 
          cell.GetPointId(2)
        )
      # end if
    # end for
    
    man.end()
    node = root_node.createChildSceneNode()
    node.attachObject(man)
    node.setPosition([0, 3, 0])  # Centro del mapa
    
  # end def

  '''
  NUEVO: Corregir posición de cámara cada frame
  '''
  def _correctCamera(self):
    """
    Mantiene la cámara dentro del área de juego
    """
    # Obtener posición actual de la cámara
    pos = self.m_CamMan.getCamera().getPosition()
    
    # LÍMITE 1: Mantener altura fija
    pos.y = 1.7
    
    # LÍMITE 2: No salir del área 50x50
    half_arena = self.m_ArenaSize / 2.0  # 25.0
    
    # Si se sale por los lados, lo regresamos
    if pos.x > half_arena - 1:
      pos.x = half_arena - 1
    elif pos.x < -half_arena + 1:
      pos.x = -half_arena + 1
    # end if
    
    if pos.z > half_arena - 1:
      pos.z = half_arena - 1
    elif pos.z < -half_arena + 1:
      pos.z = -half_arena + 1
    # end if
    
    # Aplicar la posición corregida
    self.m_CamMan.getCamera().setPosition(pos)
  # end def

# end class

"""
Main entry point
"""
def main(argv):
  app = SimpleOgreApp()
  app.go()
# end def

if __name__ == '__main__':
  main(sys.argv)
# end def

## eof - SimpleOgreApp.py