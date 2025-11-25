"""
Sistema de UI usando OgreBites TrayManager
Muestra texto real en pantalla para el juego de Tejo
"""

import Ogre.Bites as OgreBites


class UISystemTrays:
    """
    Sistema de UI con texto visible usando OgreBites TrayManager.
    Reemplaza el sistema de billboards que no podía mostrar texto.
    """
    
    def __init__(self, context, scene_mgr, camera):
        """
        Inicializa el sistema de UI.
        
        Args:
            context: La instancia de TejoGame (ApplicationContext)
            scene_mgr: El SceneManager de Ogre
            camera: La cámara principal
        """
        self.context = context
        self.scene_mgr = scene_mgr
        self.camera = camera
        self.tray_mgr = None
        
        # Valores actuales
        self.power = 75
        self.angle = 45
        self.score_a = 0
        self.score_b = 0
        self.current_team = "A"
        self.tejos_remaining = 6
        
        # Referencias a los labels
        self.team_a_label = None
        self.turn_label = None
        self.team_b_label = None
        self.power_label = None
        self.controls_label = None
        self.angle_label = None
    
    def initialize(self):
        """Inicializar el sistema de UI con TrayManager"""
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("Flechas ↑/↓: Ajustar ángulo (20-70°)")
        print("ESPACIO: Lanzar el tejo")
        print("R: Reiniciar juego")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        try:
            # Crear TrayManager
            self.tray_mgr = OgreBites.TrayManager(
                "TejoUI", 
                self.context.getRenderWindow()
            )
            
            # Agregar como input listener para que maneje eventos del mouse
            self.context.addInputListener(self.tray_mgr)
            
            # Mostrar el cursor del tray manager (opcional)
            self.tray_mgr.hideCursor()
            
            # ===== PANEL SUPERIOR =====
            
            # Equipo A (izquierda superior)
            self.team_a_label = self.tray_mgr.createLabel(
                OgreBites.TL_TOPLEFT,
                "TeamALabel",
                "EQUIPO A (Rojo)\nPuntos: 0",
                180
            )
            
            # Turno actual (centro superior)
            self.turn_label = self.tray_mgr.createLabel(
                OgreBites.TL_TOP,
                "TurnLabel", 
                "TURNO: EQUIPO A\nTejos restantes: 6",
                220
            )
            
            # Equipo B (derecha superior)
            self.team_b_label = self.tray_mgr.createLabel(
                OgreBites.TL_TOPRIGHT,
                "TeamBLabel",
                "EQUIPO B (Verde)\nPuntos: 0",
                180
            )
            
            # ===== PANEL INFERIOR =====
            
            # Fuerza (izquierda inferior)
            self.power_label = self.tray_mgr.createLabel(
                OgreBites.TL_BOTTOMLEFT,
                "PowerLabel",
                "FUERZA\n75%",
                120
            )
            
            # Controles (centro inferior)
            self.controls_label = self.tray_mgr.createLabel(
                OgreBites.TL_BOTTOM,
                "ControlsLabel",
                "W/S: Fuerza | ESPACIO: Lanzar | Flechas: Angulo | R: Reiniciar",
                450
            )
            
            # Ángulo (derecha inferior)
            self.angle_label = self.tray_mgr.createLabel(
                OgreBites.TL_BOTTOMRIGHT,
                "AngleLabel",
                "ANGULO\n45 grados",
                120
            )
            
            print("UI inicializada correctamente con TrayManager")
            
        except Exception as e:
            print(f"Error inicializando TrayManager: {e}")
            print("La UI mostrará información solo en consola")
    
    def update_team_display(self, team_name, team_number, tejos_remaining):
        """Actualizar la visualización del equipo actual"""
        self.current_team = team_name
        self.tejos_remaining = tejos_remaining
        
        try:
            if self.turn_label:
                self.turn_label.setCaption(
                    f"TURNO: EQUIPO {team_name}\nTejos restantes: {tejos_remaining}"
                )
        except Exception as e:
            print(f"Error actualizando turno: {e}")
        
        print(f"\n>>> TURNO: EQUIPO {team_name} - Quedan {tejos_remaining} tejos")
    
    def update_score_display(self, score_a, score_b):
        """Actualizar los puntajes mostrados"""
        self.score_a = score_a
        self.score_b = score_b
        
        try:
            if self.team_a_label:
                self.team_a_label.setCaption(
                    f"EQUIPO A (Rojo)\nPuntos: {score_a}"
                )
            
            if self.team_b_label:
                self.team_b_label.setCaption(
                    f"EQUIPO B (Verde)\nPuntos: {score_b}"
                )
        except Exception as e:
            print(f"Error actualizando puntajes: {e}")
        
        print(f"MARCADOR - Equipo A: {score_a} | Equipo B: {score_b}")
    
    def show_launch_info(self, power, angle):
        """Mostrar información del lanzamiento"""
        self.power = power
        self.angle = angle
        
        try:
            if self.controls_label:
                self.controls_label.setCaption(
                    f"LANZANDO! Fuerza: {power}% | Angulo: {angle} grados"
                )
        except Exception as e:
            print(f"Error mostrando lanzamiento: {e}")
        
        print(f"\n¡LANZADO! Fuerza: {power}% | Ángulo: {angle}°")
        print("-" * 40)
    
    def show_score_info(self, breakdown, team_scores, current_team):
        """Mostrar información detallada de puntuación"""
        try:
            if self.controls_label:
                if breakdown['final_total'] > 0:
                    self.controls_label.setCaption(
                        f"PUNTOS: {breakdown['final_total']} | Equipo A: {team_scores[0]} | Equipo B: {team_scores[1]}"
                    )
                else:
                    self.controls_label.setCaption(
                        "Sin puntos | W/S: Fuerza | ESPACIO: Lanzar | Flechas: Angulo"
                    )
        except Exception as e:
            print(f"Error mostrando puntuación: {e}")
        
        print("RESULTADO:")
        for detail in breakdown['details']:
            print(f"  • {detail}")
        
        if breakdown['final_total'] > 0:
            print(f"  • Puntos: {breakdown['final_total']}")
        else:
            print(f"  • Sin puntos")
        print("-" * 40)
    
    def update_power(self, power):
        """Actualizar el valor de fuerza"""
        self.power = power
        
        try:
            if self.power_label:
                self.power_label.setCaption(f"FUERZA\n{int(power)}%")
        except Exception as e:
            print(f"Error actualizando fuerza: {e}")
        
        self._print_status()
    
    def update_angle(self, angle):
        """Actualizar el valor del ángulo"""
        self.angle = angle
        
        try:
            if self.angle_label:
                self.angle_label.setCaption(f"ANGULO\n{int(angle)} grados")
        except Exception as e:
            print(f"Error actualizando ángulo: {e}")
        
        self._print_status()
    
    def update(self, power, angle):
        """Actualizar tanto fuerza como ángulo"""
        self.power = power
        self.angle = angle
        
        try:
            if self.power_label:
                self.power_label.setCaption(f"FUERZA\n{int(power)}%")
            
            if self.angle_label:
                self.angle_label.setCaption(f"ANGULO\n{int(angle)} grados")
        except Exception as e:
            print(f"Error actualizando UI: {e}")
    
    def _print_status(self):
        """Imprimir estado actual en consola"""
        print(f"\rFuerza: {int(self.power):3d}% | Ángulo: {int(self.angle):2d}°  ", end="", flush=True)
    
    def reset_controls_label(self):
        """Restaurar el label de controles al texto por defecto"""
        try:
            if self.controls_label:
                self.controls_label.setCaption(
                    "W/S: Fuerza | ESPACIO: Lanzar | Flechas: Angulo | R: Reiniciar"
                )
        except Exception as e:
            print(f"Error restaurando controles: {e}")
    
    def cleanup(self):
        """Limpiar recursos de UI"""
        try:
            if self.tray_mgr:
                # Destruir todos los widgets
                self.tray_mgr.destroyAllWidgets()
                
                # Remover el input listener
                self.context.removeInputListener(self.tray_mgr)
                
                self.tray_mgr = None
                
            print("\nUI limpiada correctamente")
        except Exception as e:
            print(f"Error durante limpieza de UI: {e}")
    
    def frame_update(self, time_since_last_frame):
        """Actualización por frame - requerido por compatibilidad"""
        # TrayManager no necesita actualizaciones manuales por frame
        pass