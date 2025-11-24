import Ogre

class UISystem:
    def __init__(self, scene_mgr, camera):
        self.scene_mgr = scene_mgr
        self.camera = camera
        self.power = 75
        self.angle = 45
        self.billboard_sets = []
    
    def initialize(self):
        print("\n" + "="*50)
        print("CONTROLES DEL JUEGO DE TEJO")
        print("="*50)
        print("W/S: Ajustar fuerza (50-100)")
        print("↑/↓: Ajustar ángulo (20-70°)")
        print("ESPACIO: Lanzar el tejo")
        print("ESC: Salir")
        print("="*50 + "\n")
        
        self._print_status()
    
    def _print_status(self):
        print(f"\rF:{int(self.power):3d}% | A:{int(self.angle):2d}°  ", end="", flush=True)
    
    def update_team_display(self, team_name, team_number, tejos_remaining):
        print(f"\n>>> TURNO: EQUIPO {team_name} - Quedan {tejos_remaining} tejos")
    
    def update_score_display(self, score_a, score_b):
        print(f"MARCADOR - Equipo A: {score_a} | Equipo B: {score_b}")
    
    def show_launch_info(self, power, angle):
        print(f"\n\n¡Lanzado! F:{power}% A:{angle}°")
        print("-" * 40)
    
    def show_score_info(self, breakdown, team_scores, current_team):
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
        self.power = power
        self._print_status()
    
    def update_angle(self, angle):
        self.angle = angle
        self._print_status()
    
    def update(self, power, angle):
        self.power = power
        self.angle = angle
    
    def cleanup(self):
        print("\n")
