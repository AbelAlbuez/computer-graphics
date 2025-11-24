"""Sistema de UI para mostrar información del juego"""
import Ogre

class UISystem:
    """Maneja la UI del juego con salida por consola y barras verticales"""
    
    def __init__(self, scene_mgr, camera):
        self.scene_mgr = scene_mgr
        self.camera = camera
        self.power = 75
        self.angle = 45
        self.billboard_sets = []
    # end def
    
    def initialize(self):
        """Inicializa el sistema de UI"""
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("↑/↓: Ajustar ángulo (20-70°)")
        print("ESPACIO: Lanzar el tejo")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        # Crear barras verticales
        self._create_vertical_bars()
        
        self._print_status()
    # end def
    
    def _create_vertical_bars(self):
        """Crea barras verticales para fuerza y ángulo"""
        # Panel de fondo para FUERZA (izquierda)
        self._create_panel([-1.5, 1.2, 1.5], [0.15, 1.0], [0.1, 0.1, 0.1, 0.8])
        
        # Barra vertical de fuerza (amarilla)
        self.power_bar_set = self.scene_mgr.createBillboardSet("PowerBarSet", 1)
        self.power_bar_set.setMaterialName("BaseWhiteNoLighting")
        self.power_bar_set.setBillboardType(Ogre.BBT_POINT)
        self.power_bar_billboard = self.power_bar_set.createBillboard([-1.5, 1.2, 1.5])
        self.power_bar_billboard.setDimensions(0.12, 0.95)
        self.power_bar_billboard.setColour(Ogre.ColourValue(1, 1, 0, 0.7))
        
        power_bar_node = self.scene_mgr.getRootSceneNode().createChildSceneNode()
        power_bar_node.attachObject(self.power_bar_set)
        self.billboard_sets.append(self.power_bar_set)
        
        # Indicador de fuerza (punto rojo que se mueve verticalmente)
        self.power_indicator_set = self.scene_mgr.createBillboardSet("PowerIndicatorSet", 1)
        self.power_indicator_set.setMaterialName("BaseWhiteNoLighting")
        self.power_indicator_set.setBillboardType(Ogre.BBT_POINT)
        self.power_indicator_billboard = self.power_indicator_set.createBillboard([-1.5, 1.2, 1.5])
        self.power_indicator_billboard.setDimensions(0.18, 0.08)
        self.power_indicator_billboard.setColour(Ogre.ColourValue(1, 0, 0, 1))
        
        power_indicator_node = self.scene_mgr.getRootSceneNode().createChildSceneNode()
        power_indicator_node.attachObject(self.power_indicator_set)
        self.billboard_sets.append(self.power_indicator_set)
        
        # Panel de fondo para ANGULO (derecha)
        self._create_panel([-1.5, 1.2, 2.5], [0.15, 1.0], [0.1, 0.1, 0.1, 0.8])
        
        # Barra vertical de ángulo (cian)
        self.angle_bar_set = self.scene_mgr.createBillboardSet("AngleBarSet", 1)
        self.angle_bar_set.setMaterialName("BaseWhiteNoLighting")
        self.angle_bar_set.setBillboardType(Ogre.BBT_POINT)
        self.angle_bar_billboard = self.angle_bar_set.createBillboard([-1.5, 1.2, 2.5])
        self.angle_bar_billboard.setDimensions(0.12, 0.95)
        self.angle_bar_billboard.setColour(Ogre.ColourValue(0, 1, 1, 0.7))
        
        angle_bar_node = self.scene_mgr.getRootSceneNode().createChildSceneNode()
        angle_bar_node.attachObject(self.angle_bar_set)
        self.billboard_sets.append(self.angle_bar_set)
        
        # Indicador de ángulo (punto azul que se mueve verticalmente)
        self.angle_indicator_set = self.scene_mgr.createBillboardSet("AngleIndicatorSet", 1)
        self.angle_indicator_set.setMaterialName("BaseWhiteNoLighting")
        self.angle_indicator_set.setBillboardType(Ogre.BBT_POINT)
        self.angle_indicator_billboard = self.angle_indicator_set.createBillboard([-1.5, 1.2, 2.5])
        self.angle_indicator_billboard.setDimensions(0.18, 0.08)
        self.angle_indicator_billboard.setColour(Ogre.ColourValue(0, 0, 1, 1))
        
        angle_indicator_node = self.scene_mgr.getRootSceneNode().createChildSceneNode()
        angle_indicator_node.attachObject(self.angle_indicator_set)
        self.billboard_sets.append(self.angle_indicator_set)
        
        # Actualizar posiciones iniciales
        self._update_indicators()
    # end def
    
    def _create_panel(self, position, size, color):
        """Crea un panel de fondo"""
        panel_set = self.scene_mgr.createBillboardSet(f"Panel_{len(self.billboard_sets)}", 1)
        panel_set.setMaterialName("BaseWhiteNoLighting")
        panel_set.setBillboardType(Ogre.BBT_POINT)
        panel = panel_set.createBillboard(position)
        panel.setDimensions(size[0], size[1])
        panel.setColour(Ogre.ColourValue(color[0], color[1], color[2], color[3]))
        
        panel_node = self.scene_mgr.getRootSceneNode().createChildSceneNode()
        panel_node.attachObject(panel_set)
        self.billboard_sets.append(panel_set)
    # end def
    
    def _update_indicators(self):
        """Actualiza la posición de los indicadores según los valores (movimiento vertical)"""
        # Actualizar indicador de fuerza (50-100 -> movimiento en Y de 0.7 a 1.7)
        power_y = 0.7 + ((self.power - 50) / 50) * 1.0
        self.power_indicator_billboard.setPosition([-1.5, power_y, 1.5])
        
        # Actualizar indicador de ángulo (20-70 -> movimiento en Y de 0.7 a 1.7)
        angle_y = 0.7 + ((self.angle - 20) / 50) * 1.0
        self.angle_indicator_billboard.setPosition([-1.5, angle_y, 2.5])
    # end def
    
    def _print_status(self):
        """Imprime el estado actual en consola"""
        print(f"\rFUERZA: {int(self.power):3d}  |  ANGULO: {int(self.angle):2d}°", end="", flush=True)
    # end def
    
    def update_power(self, power):
        """Actualiza el display de fuerza"""
        self.power = power
        self._update_indicators()
        self._print_status()
    # end def
    
    def update_angle(self, angle):
        """Actualiza el display de ángulo"""
        self.angle = angle
        self._update_indicators()
        self._print_status()
    # end def
    
    def update(self, power, angle):
        """Actualiza ambos displays"""
        self.power = power
        self.angle = angle
        self._update_indicators()
    # end def
    
    def cleanup(self):
        """Limpia los recursos de UI"""
        print("\n")
    # end def
# end class

