import Ogre
import math

class UISystem:
    """
    Sistema de UI con texto visible usando ManualObject para dibujar caracteres.
    Los textos se dibujan en negro sobre los paneles blancos.
    """
    
    def __init__(self, scene_mgr, camera):
        self.scene_mgr = scene_mgr
        self.camera = camera
        self.power = 75
        self.angle = 45
        
        # Almacenar información del juego
        self.score_a = 0
        self.score_b = 0
        self.current_team = "A"
        self.tejos_remaining = 6
        
        # Billboards sets para cada sección
        self.top_billboards = {}
        self.bottom_billboards = {}
        self.manual_objects = {}
        
        # Nodos para organizar la UI
        self.ui_top_node = None
        self.ui_bottom_node = None
        
        # Materiales para la UI
        self._create_ui_materials()
    
    def _create_ui_materials(self):
        """Crear materiales personalizados para la UI con fondos blancos para texto negro"""
        mat_mgr = Ogre.MaterialManager.getSingleton()
        
        # Lista de materiales a crear con sus colores (R, G, B, Alpha)
        materials_to_create = [
            # Paneles principales con fondos más claros para contraste con texto negro
            ('ui_red_panel', 0.9, 0.3, 0.3, 0.95),      # Rojo más claro
            ('ui_green_panel', 0.3, 0.9, 0.3, 0.95),    # Verde más claro
            ('ui_gray_panel', 0.7, 0.7, 0.7, 0.95),     # Gris claro para fondo
            ('ui_white_panel', 0.95, 0.95, 0.95, 0.95), # Blanco para fondos de texto
            ('ui_power_indicator', 1.0, 0.7, 0.2, 1.0), # Naranja brillante
            ('ui_angle_indicator', 0.2, 0.7, 1.0, 1.0), # Azul brillante
            ('ui_black_text', 0.0, 0.0, 0.0, 1.0),      # Negro para texto
            ('ui_dark_bg', 0.15, 0.15, 0.15, 0.9),      # Fondo oscuro
        ]
        
        for mat_name, r, g, b, a in materials_to_create:
            if not mat_mgr.resourceExists(mat_name):
                try:
                    mat = mat_mgr.create(mat_name, 'General')
                    tech = mat.getTechnique(0)
                    pass_ = tech.getPass(0)
                    pass_.setLightingEnabled(False)
                    pass_.setDiffuse(r, g, b, a)
                    pass_.setAmbient(r, g, b)
                    pass_.setEmissive(r * 0.6, g * 0.6, b * 0.6)
                    pass_.setSceneBlending(Ogre.SBT_TRANSPARENT_ALPHA)
                    pass_.setDepthCheckEnabled(False)
                    pass_.setDepthWriteEnabled(False)
                except Exception as e:
                    print(f"Advertencia: No se pudo crear material {mat_name}: {e}")
    
    def initialize(self):
        """Inicializar el sistema de UI con las 3 secciones"""
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("↑/↓: Ajustar ángulo (20-70°)")
        print("ESPACIO: Lanzar el tejo")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        # Crear las secciones de UI
        self._create_top_section()
        self._create_bottom_section()
        self._create_text_overlays()
        
        # Actualizar posiciones iniciales
        self._update_ui_positions()
    
    def _create_top_section(self):
        """Crear la sección superior con fondos blancos para texto negro"""
        try:
            self.ui_top_node = self.scene_mgr.getRootSceneNode().createChildSceneNode('UITopNode')
            
            # Fondo oscuro general para toda la sección superior
            top_bg_set = self.scene_mgr.createBillboardSet('TopBackground', 1)
            top_bg_set.setMaterialName('ui_dark_bg')
            top_bg_set.setBillboardType(Ogre.BBT_POINT)
            top_bg_set.setDefaultDimensions(26.0, 3.0)
            top_bg_set.createBillboard(0, 0, 0)
            self.ui_top_node.attachObject(top_bg_set)
            self.top_billboards['background'] = top_bg_set
            
            # Panel Equipo A con fondo blanco para texto
            team_a_bg = self.scene_mgr.createBillboardSet('TeamABg', 1)
            team_a_bg.setMaterialName('ui_white_panel')
            team_a_bg.setBillboardType(Ogre.BBT_POINT)
            team_a_bg.setDefaultDimensions(7.0, 2.2)
            team_a_bg.createBillboard(-8.0, 0, 0.1)
            self.ui_top_node.attachObject(team_a_bg)
            self.top_billboards['team_a_bg'] = team_a_bg
            
            # Marco rojo para Equipo A
            team_a_frame = self.scene_mgr.createBillboardSet('TeamAFrame', 1)
            team_a_frame.setMaterialName('ui_red_panel')
            team_a_frame.setBillboardType(Ogre.BBT_POINT)
            team_a_frame.setDefaultDimensions(7.2, 2.4)
            team_a_frame.createBillboard(-8.0, 0, 0.05)
            self.ui_top_node.attachObject(team_a_frame)
            self.top_billboards['team_a_frame'] = team_a_frame
            
            # Panel de Turno con fondo blanco
            turn_bg = self.scene_mgr.createBillboardSet('TurnBg', 1)
            turn_bg.setMaterialName('ui_white_panel')
            turn_bg.setBillboardType(Ogre.BBT_POINT)
            turn_bg.setDefaultDimensions(5.5, 2.2)
            turn_bg.createBillboard(0, 0, 0.1)
            self.ui_top_node.attachObject(turn_bg)
            self.top_billboards['turn_bg'] = turn_bg
            
            # Marco para turno (cambiará de color)
            turn_frame = self.scene_mgr.createBillboardSet('TurnFrame', 1)
            turn_frame.setMaterialName('ui_gray_panel')
            turn_frame.setBillboardType(Ogre.BBT_POINT)
            turn_frame.setDefaultDimensions(5.7, 2.4)
            turn_frame.createBillboard(0, 0, 0.05)
            self.ui_top_node.attachObject(turn_frame)
            self.top_billboards['turn_frame'] = turn_frame
            
            # Panel Equipo B con fondo blanco
            team_b_bg = self.scene_mgr.createBillboardSet('TeamBBg', 1)
            team_b_bg.setMaterialName('ui_white_panel')
            team_b_bg.setBillboardType(Ogre.BBT_POINT)
            team_b_bg.setDefaultDimensions(7.0, 2.2)
            team_b_bg.createBillboard(8.0, 0, 0.1)
            self.ui_top_node.attachObject(team_b_bg)
            self.top_billboards['team_b_bg'] = team_b_bg
            
            # Marco verde para Equipo B
            team_b_frame = self.scene_mgr.createBillboardSet('TeamBFrame', 1)
            team_b_frame.setMaterialName('ui_green_panel')
            team_b_frame.setBillboardType(Ogre.BBT_POINT)
            team_b_frame.setDefaultDimensions(7.2, 2.4)
            team_b_frame.createBillboard(8.0, 0, 0.05)
            self.ui_top_node.attachObject(team_b_frame)
            self.top_billboards['team_b_frame'] = team_b_frame
            
        except Exception as e:
            print(f"Error creando sección superior: {e}")
    
    def _create_bottom_section(self):
        """Crear la sección inferior con fondos blancos para texto negro"""
        try:
            self.ui_bottom_node = self.scene_mgr.getRootSceneNode().createChildSceneNode('UIBottomNode')
            
            # Fondo oscuro general
            bottom_bg_set = self.scene_mgr.createBillboardSet('BottomBackground', 1)
            bottom_bg_set.setMaterialName('ui_dark_bg')
            bottom_bg_set.setBillboardType(Ogre.BBT_POINT)
            bottom_bg_set.setDefaultDimensions(26.0, 3.0)
            bottom_bg_set.createBillboard(0, 0, 0)
            self.ui_bottom_node.attachObject(bottom_bg_set)
            self.bottom_billboards['background'] = bottom_bg_set
            
            # Panel de Fuerza con fondo blanco
            power_panel = self.scene_mgr.createBillboardSet('PowerPanel', 1)
            power_panel.setMaterialName('ui_white_panel')
            power_panel.setBillboardType(Ogre.BBT_POINT)
            power_panel.setDefaultDimensions(7.0, 2.0)
            power_panel.createBillboard(-8.0, 0, 0.1)
            self.ui_bottom_node.attachObject(power_panel)
            self.bottom_billboards['power_panel'] = power_panel
            
            # Barra de progreso para fuerza (fondo)
            power_bar_bg = self.scene_mgr.createBillboardSet('PowerBarBg', 1)
            power_bar_bg.setMaterialName('ui_black_text')
            power_bar_bg.setBillboardType(Ogre.BBT_POINT)
            power_bar_bg.setDefaultDimensions(5.5, 0.5)
            power_bar_bg.createBillboard(-8.0, -0.5, 0.15)
            self.ui_bottom_node.attachObject(power_bar_bg)
            self.bottom_billboards['power_bar_bg'] = power_bar_bg
            
            # Barra de progreso para fuerza (relleno)
            power_bar = self.scene_mgr.createBillboardSet('PowerBar', 1)
            power_bar.setMaterialName('ui_gray_panel')
            power_bar.setBillboardType(Ogre.BBT_POINT)
            power_bar.setDefaultDimensions(5.3, 0.3)
            power_bar.createBillboard(-8.0, -0.5, 0.16)
            self.ui_bottom_node.attachObject(power_bar)
            self.bottom_billboards['power_bar'] = power_bar
            
            # Indicador de Fuerza
            power_indicator = self.scene_mgr.createBillboardSet('PowerIndicator', 1)
            power_indicator.setMaterialName('ui_power_indicator')
            power_indicator.setBillboardType(Ogre.BBT_POINT)
            power_indicator.setDefaultDimensions(0.8, 0.8)
            power_indicator.createBillboard(-10.0, -0.5, 0.2)
            self.ui_bottom_node.attachObject(power_indicator)
            self.bottom_billboards['power_indicator'] = power_indicator
            
            # Panel de Información central con fondo blanco
            info_panel = self.scene_mgr.createBillboardSet('InfoPanel', 1)
            info_panel.setMaterialName('ui_white_panel')
            info_panel.setBillboardType(Ogre.BBT_POINT)
            info_panel.setDefaultDimensions(8.0, 2.2)
            info_panel.createBillboard(0, 0, 0.1)
            self.ui_bottom_node.attachObject(info_panel)
            self.bottom_billboards['info_panel'] = info_panel
            
            # Panel de Ángulo con fondo blanco
            angle_panel = self.scene_mgr.createBillboardSet('AnglePanel', 1)
            angle_panel.setMaterialName('ui_white_panel')
            angle_panel.setBillboardType(Ogre.BBT_POINT)
            angle_panel.setDefaultDimensions(7.0, 2.0)
            angle_panel.createBillboard(8.0, 0, 0.1)
            self.ui_bottom_node.attachObject(angle_panel)
            self.bottom_billboards['angle_panel'] = angle_panel
            
            # Barra de progreso para ángulo (fondo)
            angle_bar_bg = self.scene_mgr.createBillboardSet('AngleBarBg', 1)
            angle_bar_bg.setMaterialName('ui_black_text')
            angle_bar_bg.setBillboardType(Ogre.BBT_POINT)
            angle_bar_bg.setDefaultDimensions(5.5, 0.5)
            angle_bar_bg.createBillboard(8.0, -0.5, 0.15)
            self.ui_bottom_node.attachObject(angle_bar_bg)
            self.bottom_billboards['angle_bar_bg'] = angle_bar_bg
            
            # Barra de progreso para ángulo (relleno)
            angle_bar = self.scene_mgr.createBillboardSet('AngleBar', 1)
            angle_bar.setMaterialName('ui_gray_panel')
            angle_bar.setBillboardType(Ogre.BBT_POINT)
            angle_bar.setDefaultDimensions(5.3, 0.3)
            angle_bar.createBillboard(8.0, -0.5, 0.16)
            self.ui_bottom_node.attachObject(angle_bar)
            self.bottom_billboards['angle_bar'] = angle_bar
            
            # Indicador de Ángulo
            angle_indicator = self.scene_mgr.createBillboardSet('AngleIndicator', 1)
            angle_indicator.setMaterialName('ui_angle_indicator')
            angle_indicator.setBillboardType(Ogre.BBT_POINT)
            angle_indicator.setDefaultDimensions(0.8, 0.8)
            angle_indicator.createBillboard(6.0, -0.5, 0.2)
            self.ui_bottom_node.attachObject(angle_indicator)
            self.bottom_billboards['angle_indicator'] = angle_indicator
            
        except Exception as e:
            print(f"Error creando sección inferior: {e}")
    
    def _create_text_overlays(self):
        """Crear overlays de texto usando pequeños billboards negros para simular letras"""
        try:
            # TEXTOS SUPERIORES
            # "EQUIPO A" - usar múltiples billboards pequeños negros
            for i, char in enumerate("EQUIPO-A"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharA{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                if char == '-':
                    char_bb.setDefaultDimensions(0.2, 0.05)
                    x_offset = -8.5 + (i * 0.5)
                else:
                    char_bb.setDefaultDimensions(0.3, 0.4)
                    x_offset = -9.5 + (i * 0.5)
                char_bb.createBillboard(x_offset, 0.6, 0.2)
                self.ui_top_node.attachObject(char_bb)
                self.manual_objects[f'char_a_{i}'] = char_bb
            
            # Número del puntaje A (usar barras para formar dígitos)
            self._create_digit_display('score_a', -8.0, 0.0, self.ui_top_node)
            
            # "TURNO" 
            for i, char in enumerate("TURNO"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharTurn{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                char_bb.setDefaultDimensions(0.3, 0.4)
                char_bb.createBillboard(-1.0 + (i * 0.5), 0.6, 0.2)
                self.ui_top_node.attachObject(char_bb)
                self.manual_objects[f'char_turn_{i}'] = char_bb
            
            # "EQUIPO B"
            for i, char in enumerate("EQUIPO-B"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharB{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                if char == '-':
                    char_bb.setDefaultDimensions(0.2, 0.05)
                    x_offset = 6.5 + (i * 0.5)
                else:
                    char_bb.setDefaultDimensions(0.3, 0.4)
                    x_offset = 5.5 + (i * 0.5)
                char_bb.createBillboard(x_offset, 0.6, 0.2)
                self.ui_top_node.attachObject(char_bb)
                self.manual_objects[f'char_b_{i}'] = char_bb
            
            # Número del puntaje B
            self._create_digit_display('score_b', 8.0, 0.0, self.ui_top_node)
            
            # TEXTOS INFERIORES
            # "FUERZA"
            for i, char in enumerate("FUERZA"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharPower{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                char_bb.setDefaultDimensions(0.3, 0.4)
                char_bb.createBillboard(-9.0 + (i * 0.5), 0.6, 0.2)
                self.ui_bottom_node.attachObject(char_bb)
                self.manual_objects[f'char_power_{i}'] = char_bb
            
            # Valor de fuerza
            self._create_digit_display('power_value', -8.0, 0.0, self.ui_bottom_node)
            
            # "LISTO" en el centro
            for i, char in enumerate("LISTO"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharReady{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                char_bb.setDefaultDimensions(0.4, 0.5)
                char_bb.createBillboard(-1.0 + (i * 0.6), 0.0, 0.2)
                self.ui_bottom_node.attachObject(char_bb)
                self.manual_objects[f'char_ready_{i}'] = char_bb
            
            # "ANGULO"
            for i, char in enumerate("ANGULO"):
                char_bb = self.scene_mgr.createBillboardSet(f'CharAngle{i}', 1)
                char_bb.setMaterialName('ui_black_text')
                char_bb.setBillboardType(Ogre.BBT_POINT)
                char_bb.setDefaultDimensions(0.3, 0.4)
                char_bb.createBillboard(6.5 + (i * 0.5), 0.6, 0.2)
                self.ui_bottom_node.attachObject(char_bb)
                self.manual_objects[f'char_angle_{i}'] = char_bb
            
            # Valor de ángulo
            self._create_digit_display('angle_value', 8.0, 0.0, self.ui_bottom_node)
            
        except Exception as e:
            print(f"Error creando overlays de texto: {e}")
    
    def _create_digit_display(self, name, x_pos, y_pos, parent_node):
        """Crear un display de dígitos usando billboards para formar números"""
        try:
            # Crear 3 billboards para formar hasta 3 dígitos (ej: "100", "45°")
            for digit in range(3):
                digit_bb = self.scene_mgr.createBillboardSet(f'{name}_digit{digit}', 1)
                digit_bb.setMaterialName('ui_black_text')
                digit_bb.setBillboardType(Ogre.BBT_POINT)
                digit_bb.setDefaultDimensions(0.4, 0.6)
                digit_bb.createBillboard(x_pos + (digit * 0.5) - 0.5, y_pos, 0.25)
                parent_node.attachObject(digit_bb)
                self.manual_objects[f'{name}_{digit}'] = digit_bb
        except Exception as e:
            print(f"Error creando display de dígitos {name}: {e}")
    
    def _update_digit_display(self, name, value):
        """Actualizar el display de dígitos para mostrar un número"""
        try:
            value_str = str(int(value)).zfill(3)  # Convertir a string de 3 dígitos
            for i, digit in enumerate(value_str):
                if f'{name}_{i}' in self.manual_objects:
                    # Cambiar el tamaño del billboard según el dígito para simular números
                    bb = self.manual_objects[f'{name}_{i}']
                    if digit == '0':
                        bb.setDefaultDimensions(0.4, 0.6)  # O
                    elif digit == '1':
                        bb.setDefaultDimensions(0.1, 0.6)  # I
                    else:
                        bb.setDefaultDimensions(0.35, 0.6) # Otros
        except Exception as e:
            print(f"Error actualizando dígitos {name}: {e}")
    
    def _update_ui_positions(self):
        """Actualizar posiciones de UI"""
        if not self.camera:
            return
        
        try:
            # Obtener posición y orientación de la cámara
            try:
                cam_pos = self.camera.getRealPosition()
                cam_dir = self.camera.getRealDirection() 
                cam_up = self.camera.getRealUp()
            except AttributeError:
                try:
                    cam_pos = self.camera.getPosition()
                    cam_dir = self.camera.getDirection()
                    cam_up = self.camera.getUp()
                except AttributeError:
                    parent_node = self.camera.getParentSceneNode()
                    if parent_node:
                        cam_pos = parent_node.getPosition()
                        cam_dir = self.camera.getDerivedDirection()
                        cam_up = self.camera.getDerivedUp()
                    else:
                        cam_pos = Ogre.Vector3(0, 1.5, 15)
                        cam_dir = Ogre.Vector3(0, 0, -1)
                        cam_up = Ogre.Vector3(0, 1, 0)
            
            # Distancia fija de la UI desde la cámara
            ui_distance = 24.0
            
            # Usar valores fijos para evitar problemas con FOV
            fov_y_rad = math.radians(50)
            aspect_ratio = 16.0 / 9.0
            
            # Altura visible a la distancia UI
            visible_height = 2 * ui_distance * math.tan(fov_y_rad / 2)
            
            # SECCIÓN SUPERIOR
            top_offset_y = visible_height * 0.38
            top_position = Ogre.Vector3(
                cam_pos.x + cam_dir.x * ui_distance,
                cam_pos.y + cam_dir.y * ui_distance + top_offset_y,
                cam_pos.z + cam_dir.z * ui_distance
            )
            
            if self.ui_top_node:
                self.ui_top_node.setPosition(top_position)
                try:
                    self.ui_top_node.lookAt(cam_pos, Ogre.Node.TS_WORLD)
                except:
                    direction = cam_pos - top_position
                    direction.normalise()
                    self.ui_top_node.setDirection(direction)
            
            # SECCIÓN INFERIOR
            bottom_offset_y = -visible_height * 0.38
            bottom_position = Ogre.Vector3(
                cam_pos.x + cam_dir.x * ui_distance,
                cam_pos.y + cam_dir.y * ui_distance + bottom_offset_y,
                cam_pos.z + cam_dir.z * ui_distance
            )
            
            if self.ui_bottom_node:
                self.ui_bottom_node.setPosition(bottom_position)
                try:
                    self.ui_bottom_node.lookAt(cam_pos, Ogre.Node.TS_WORLD)
                except:
                    direction = cam_pos - bottom_position
                    direction.normalise()
                    self.ui_bottom_node.setDirection(direction)
            
            # Actualizar indicador de fuerza
            if 'power_indicator' in self.bottom_billboards:
                power_normalized = (self.power - 50) / 50.0
                power_x = -10.5 + (power_normalized * 5.0)
                power_indicator = self.bottom_billboards['power_indicator'].getBillboard(0)
                try:
                    power_indicator.setPosition(Ogre.Vector3(power_x, -0.5, 0.2))
                except:
                    power_indicator.setPosition(power_x, -0.5, 0.2)
            
            # Actualizar indicador de ángulo
            if 'angle_indicator' in self.bottom_billboards:
                angle_normalized = (self.angle - 20) / 50.0
                angle_x = 5.5 + (angle_normalized * 5.0)
                angle_indicator = self.bottom_billboards['angle_indicator'].getBillboard(0)
                try:
                    angle_indicator.setPosition(Ogre.Vector3(angle_x, -0.5, 0.2))
                except:
                    angle_indicator.setPosition(angle_x, -0.5, 0.2)
            
            # Actualizar displays de números
            self._update_digit_display('score_a', self.score_a)
            self._update_digit_display('score_b', self.score_b)
            self._update_digit_display('power_value', self.power)
            self._update_digit_display('angle_value', self.angle)
                    
        except Exception as e:
            print(f"Error en _update_ui_positions: {e}")
            try:
                if self.ui_top_node:
                    self.ui_top_node.setPosition(0, 8, -10)
                if self.ui_bottom_node:
                    self.ui_bottom_node.setPosition(0, -8, -10)
            except:
                pass
    
    def update_team_display(self, team_name, team_number, tejos_remaining):
        """Actualizar la visualización del equipo actual"""
        self.current_team = team_name
        self.tejos_remaining = tejos_remaining
        
        try:
            # Cambiar color del marco de turno según el equipo
            if 'turn_frame' in self.top_billboards:
                if team_name == "A":
                    self.top_billboards['turn_frame'].setMaterialName('ui_red_panel')
                else:
                    self.top_billboards['turn_frame'].setMaterialName('ui_green_panel')
        except Exception as e:
            print(f"Error actualizando panel de turno: {e}")
        
        self._update_ui_positions()
        print(f"\n>>> TURNO: EQUIPO {team_name} - Quedan {tejos_remaining} tejos")
    
    def update_score_display(self, score_a, score_b):
        """Actualizar los puntajes mostrados"""
        self.score_a = score_a
        self.score_b = score_b
        
        try:
            # Actualizar displays de números
            self._update_digit_display('score_a', score_a)
            self._update_digit_display('score_b', score_b)
            
            # Efecto visual: hacer crecer el marco del equipo con más puntos
            if 'team_a_frame' in self.top_billboards:
                scale = 1.0 + (score_a * 0.01)
                self.top_billboards['team_a_frame'].setDefaultDimensions(7.2 * scale, 2.4 * scale)
            
            if 'team_b_frame' in self.top_billboards:
                scale = 1.0 + (score_b * 0.01)
                self.top_billboards['team_b_frame'].setDefaultDimensions(7.2 * scale, 2.4 * scale)
                
        except Exception as e:
            print(f"Error actualizando puntajes: {e}")
        
        print(f"MARCADOR - Equipo A: {score_a} | Equipo B: {score_b}")
    
    def show_launch_info(self, power, angle):
        """Mostrar información del lanzamiento"""
        self.power = power
        self.angle = angle
        
        self._update_ui_positions()
        
        # Cambiar texto central a "LANZANDO"
        try:
            if 'info_panel' in self.bottom_billboards:
                # Cambiar color temporalmente
                self.bottom_billboards['info_panel'].setMaterialName('ui_power_indicator')
        except:
            pass
        
        print(f"\n\n¡Lanzado! F:{power}% A:{angle}°")
        print("-" * 40)
    
    def show_score_info(self, breakdown, team_scores, current_team):
        """Mostrar información detallada de puntuación"""
        try:
            if 'info_panel' in self.bottom_billboards:
                if breakdown['final_total'] > 0:
                    # Verde claro si hay puntos
                    self.bottom_billboards['info_panel'].setMaterialName('ui_green_panel')
                else:
                    # Volver a blanco si no hay puntos
                    self.bottom_billboards['info_panel'].setMaterialName('ui_white_panel')
        except:
            pass
        
        print("RESULTADO:")
        for detail in breakdown['details']:
            print(f"  • {detail}")
        
        if breakdown['final_total'] > 0:
            if breakdown['multiplier'] > 1.0:
                print(f"  • Puntos: {breakdown['final_total']} (base:{breakdown['base_total']} x{breakdown['multiplier']:.1f})")
            else:
                print(f"  • Puntos: {breakdown['final_total']}")
        else:
            print(f"  • Sin puntos")
        
        print("-" * 40)
        team_actual = "A" if current_team == 0 else "B"
        print(f"F:{breakdown['launch_force']}% | A:45° | Equipo {team_actual} | Puntaje A:{team_scores[0]} B:{team_scores[1]}")
        print()
    
    def update_power(self, power):
        """Actualizar el valor de fuerza"""
        self.power = power
        self._update_ui_positions()
        self._print_status()
    
    def update_angle(self, angle):
        """Actualizar el valor del ángulo"""
        self.angle = angle
        self._update_ui_positions()
        self._print_status()
    
    def update(self, power, angle):
        """Actualizar tanto fuerza como ángulo"""
        self.power = power
        self.angle = angle
        self._update_ui_positions()
    
    def _print_status(self):
        """Imprimir estado actual en consola"""
        print(f"\rF:{int(self.power):3d}% | A:{int(self.angle):2d}°  ", end="", flush=True)
    
    def cleanup(self):
        """Limpiar recursos de UI"""
        try:
            for name, billboard_set in self.top_billboards.items():
                if billboard_set:
                    self.scene_mgr.destroyBillboardSet(billboard_set)
            
            for name, billboard_set in self.bottom_billboards.items():
                if billboard_set:
                    self.scene_mgr.destroyBillboardSet(billboard_set)
            
            for name, obj in self.manual_objects.items():
                if obj:
                    self.scene_mgr.destroyBillboardSet(obj)
            
            if self.ui_top_node:
                self.scene_mgr.destroySceneNode(self.ui_top_node)
            if self.ui_bottom_node:
                self.scene_mgr.destroySceneNode(self.ui_bottom_node)
        except Exception as e:
            print(f"Error durante limpieza: {e}")
        
        print("\n")
    
    def frame_update(self, time_since_last_frame):
        """Actualización por frame"""
        self._update_ui_positions()