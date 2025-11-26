"""
Sistema de UI usando OgreBites TrayManager para el juego de Tejo
Usa ParamsPanel que funciona con el binding Python de Ogre
"""

import Ogre
import Ogre.Bites as OgreBites


class UISystemTrays:
    def __init__(self, context):
        self.context = context
        self.tray_mgr = None
        
        self.power = 75
        self.angle = 45
        self.score_a = 0
        self.score_b = 0
        self.current_team = "A"
        self.tejos_remaining = 6
        
        self.top_panel = None
        self.bottom_panel = None
    
    def initialize(self):
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("Flechas Arriba/Abajo: Ajustar angulo (20-70)")
        print("ESPACIO: Lanzar el tejo")
        print("R: Reiniciar juego")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        try:
            self.tray_mgr = OgreBites.TrayManager(
                "TejoUI", 
                self.context.getRenderWindow()
            )
            self.tray_mgr.hideCursor()
            
            # Panel superior - Scores y Turno
            self.top_panel = self.tray_mgr.createParamsPanel(
                OgreBites.TL_TOP,
                "TopPanel",
                350.0,
                ["Equipo A", "Turno", "Tejos", "Equipo B"]
            )
            self.top_panel.setParamValue(0, "0 pts")
            self.top_panel.setParamValue(1, "EQUIPO A")
            self.top_panel.setParamValue(2, "6")
            self.top_panel.setParamValue(3, "0 pts")
            
            # Panel inferior - Fuerza y Angulo
            self.bottom_panel = self.tray_mgr.createParamsPanel(
                OgreBites.TL_BOTTOM,
                "BottomPanel",
                300.0,
                ["Fuerza", "Angulo", "Controles"]
            )
            self.bottom_panel.setParamValue(0, "75%")
            self.bottom_panel.setParamValue(1, "45 gr")
            self.bottom_panel.setParamValue(2, "ESPACIO=Lanzar")
            
            print("TrayManager UI inicializada correctamente")
            
        except Exception as e:
            print(f"Error inicializando TrayManager: {e}")
    
    def update_team_display(self, team_name, team_number, tejos_remaining):
        self.current_team = team_name
        self.tejos_remaining = tejos_remaining
        
        if self.top_panel:
            self.top_panel.setParamValue(1, "EQUIPO " + str(team_name))
            self.top_panel.setParamValue(2, str(tejos_remaining))
        
        print(f"\n>>> TURNO: EQUIPO {team_name} - Quedan {tejos_remaining} tejos")
    
    def update_score_display(self, score_a, score_b):
        self.score_a = score_a
        self.score_b = score_b
        
        if self.top_panel:
            self.top_panel.setParamValue(0, str(score_a) + " pts")
            self.top_panel.setParamValue(3, str(score_b) + " pts")
        
        print(f"MARCADOR - Equipo A: {score_a} | Equipo B: {score_b}")
    
    def show_launch_info(self, power, angle):
        self.power = power
        self.angle = angle
        
        if self.bottom_panel:
            self.bottom_panel.setParamValue(2, "LANZADO!")
        
        print(f"\nLANZADO! Fuerza: {power}% | Angulo: {angle} grados")
        print("-" * 40)
    
    def show_score_info(self, breakdown, team_scores, current_team):
        if self.bottom_panel:
            if breakdown['final_total'] > 0:
                self.bottom_panel.setParamValue(2, "+" + str(breakdown['final_total']) + " pts!")
            else:
                self.bottom_panel.setParamValue(2, "Sin puntos")
        
        print("RESULTADO:")
        for detail in breakdown['details']:
            print(f"  - {detail}")
        print("-" * 40)
    
    def update_power(self, power):
        self.power = power
        
        if self.bottom_panel:
            self.bottom_panel.setParamValue(0, str(int(power)) + "%")
        
        self._print_status()
    
    def update_angle(self, angle):
        self.angle = angle
        
        if self.bottom_panel:
            self.bottom_panel.setParamValue(1, str(int(angle)) + " gr")
        
        self._print_status()
    
    def update(self, power, angle):
        self.power = power
        self.angle = angle
        
        if self.bottom_panel:
            self.bottom_panel.setParamValue(0, str(int(power)) + "%")
            self.bottom_panel.setParamValue(1, str(int(angle)) + " gr")
    
    def _print_status(self):
        print(f"\rFuerza: {int(self.power):3d}% | Angulo: {int(self.angle):2d} gr  ", end="", flush=True)
    
    def reset_controls_label(self):
        if self.bottom_panel:
            self.bottom_panel.setParamValue(2, "ESPACIO=Lanzar")
    
    def frame_update(self, delta_time):
        pass
    
    def cleanup(self):
        if self.tray_mgr:
            self.tray_mgr.destroyAllWidgets()
            self.tray_mgr = None
        print("\nTrayManager UI limpiada")