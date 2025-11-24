from .constants import *
import math
import random

class ScoringSystem:
    def __init__(self):
        pass
    
    def calculate_points(self, tejo_position, disc_position, tejo_orientation, disc_hit, disc_exploded):
        """
        Calcula puntos basado en:
        - Si golpeó el disco: 20% de mecha (explosión)
        - Si estalló la mecha: 3 puntos
        - Si quedó parado dentro del bocín (embocinada): 6 puntos (requiere disc_hit)
        - Si hubo mecha Y embocinada (moñona): 9 puntos
        """
        points = 0
        details = []
        
        # Verificar si el tejo quedó parado (parte angosta hacia arriba)
        is_standing = self._check_tejo_standing(tejo_orientation)
        
        # Moñona: mecha + embocinada (tejo parado dentro del bocín)
        if disc_hit and disc_exploded and is_standing:
            points = 9
            details.append("¡MOÑONA! (Embocinada + Mecha) = 9 puntos")
        # Embocinada: tejo parado dentro del bocín (sin mecha)
        elif disc_hit and is_standing:
            points = 6
            details.append("¡EMBOCINADA! (Tejo parado) = 6 puntos")
        # Mecha: explosión sin quedar parado
        elif disc_hit and disc_exploded:
            points = 3
            details.append("¡MECHA! (Explosión) = 3 puntos")
        # Golpeó el bocín pero no logró figura
        elif disc_hit:
            details.append("Golpeó el bocín pero sin figura")
        else:
            details.append("No golpeó el bocín")
        
        return points, details
    
    def _check_tejo_standing(self, orientation):
        """
        Verifica si el tejo quedó con su parte angosta hacia arriba.
        El tejo está parado si su eje Y apunta hacia arriba.
        """
        # Convertir quaternion a vector up
        x, y, z, w = orientation
        
        # El vector "up" del tejo en su orientación local
        up_x = 2 * (x*y + w*z)
        up_y = 1 - 2 * (x*x + z*z)
        up_z = 2 * (y*z - w*x)
        
        # Si up_y es cercano a 1, el tejo está parado correctamente
        # Si up_y es cercano a -1, está parado pero al revés
        return up_y > 0.7  # Tolerancia para considerar que está "parado"
    
    def check_disc_collision(self, tejo_position, disc_position, threshold=0.1):
        """
        Verifica si el tejo golpeó el bocín (disco central).
        """
        dx = tejo_position[0] - disc_position[0]
        dz = tejo_position[2] - disc_position[2]
        distance = math.sqrt(dx*dx + dz*dz)
        
        return distance <= threshold
    
    def roll_explosion(self):
        """
        Determina si la mecha estalla (20% de probabilidad).
        """
        return random.random() < 0.2
    
    # Métodos heredados del sistema anterior (por compatibilidad)
    def _is_close_to_any_mecha(self, tejo_pos, mecha_positions):
        return any(self.distance_to_mecha(tejo_pos, mecha_pos) <= MECHA_CLOSE_DISTANCE 
                  for mecha_pos in mecha_positions)
    
    def distance_to_mecha(self, tejo_pos, mecha_pos):
        dx = tejo_pos[0] - mecha_pos[0]
        dy = tejo_pos[1] - mecha_pos[1]
        dz = tejo_pos[2] - mecha_pos[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def is_on_board(self, tejo_position, board_bounds):
        x, y, z = tejo_position
        return (board_bounds['x_min'] <= x <= board_bounds['x_max'] and
                board_bounds['y_min'] <= y <= board_bounds['y_max'] and
                board_bounds['z_min'] <= z <= board_bounds['z_max'])
    
    def get_board_bounds_from_angle(self, board_length, board_width, board_angle):
        angle_rad = math.radians(board_angle)
        
        x_projection = board_length * math.cos(angle_rad)
        y_projection = board_length * math.sin(angle_rad)
        
        return {
            'x_min': -0.2,
            'x_max': x_projection + 0.2,
            'y_min': 0,
            'y_max': y_projection + 0.5,
            'z_min': -board_width/2 - 0.1,
            'z_max': board_width/2 + 0.1
        }
    
    def find_closest_mecha(self, tejo_pos, mecha_positions):
        if not mecha_positions:
            return None, float('inf')
        
        closest_idx = 0
        closest_dist = self.distance_to_mecha(tejo_pos, mecha_positions[0])
        
        for i, mecha_pos in enumerate(mecha_positions[1:], start=1):
            dist = self.distance_to_mecha(tejo_pos, mecha_pos)
            if dist < closest_dist:
                closest_dist = dist
                closest_idx = i
        
        return closest_idx, closest_dist
    
    def get_score_breakdown(self, tejo_position, mecha_positions, mecha_hits, on_board, launch_force=75):
        breakdown = {
            'mecha_hits': 0,
            'close_to_mecha': 0,
            'on_board': 0,
            'base_total': 0,
            'multiplier': 1.0,
            'final_total': 0,
            'details': [],
            'launch_force': launch_force
        }
        
        if len(mecha_hits) > 0:
            breakdown['mecha_hits'] = POINTS_MECHA * len(mecha_hits)
            breakdown['details'].append(f"Golpeó {len(mecha_hits)} mecha(s)")
        elif self._is_close_to_any_mecha(tejo_position, mecha_positions):
            breakdown['close_to_mecha'] = POINTS_CLOSE
            closest_idx, dist = self.find_closest_mecha(tejo_position, mecha_positions)
            breakdown['details'].append(f"Cerca de mecha {closest_idx} ({dist:.2f}m)")
        
        if on_board:
            breakdown['on_board'] = POINTS_BOARD
            breakdown['details'].append("En el tablero")
        else:
            breakdown['details'].append("Fuera del tablero")
        
        breakdown['base_total'] = (
            breakdown['mecha_hits'] + 
            breakdown['close_to_mecha'] + 
            breakdown['on_board']
        )
        
        breakdown['multiplier'] = 1.0 + ((launch_force - 50) / 100.0)
        
        if breakdown['base_total'] > 0:
            breakdown['final_total'] = int(breakdown['base_total'] * breakdown['multiplier'])
        else:
            breakdown['final_total'] = 0
        
        if launch_force >= 85:
            breakdown['details'].insert(0, "Lanzamiento potente con excelente rotación")
        elif launch_force >= 70:
            breakdown['details'].insert(0, "Lanzamiento balanceado")
        else:
            breakdown['details'].insert(0, "Lanzamiento suave")
        
        return breakdown
