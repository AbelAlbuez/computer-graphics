from .constants import *
import math

class ScoringSystem:
    def __init__(self):
        pass
    
    def calculate_points(self, tejo_position, mecha_positions, mecha_hits, on_board):
        points = 0
        
        if len(mecha_hits) > 0:
            points += POINTS_MECHA * len(mecha_hits)
        elif self._is_close_to_any_mecha(tejo_position, mecha_positions):
            points += POINTS_CLOSE
        
        if on_board:
            points += POINTS_BOARD
        
        return points
    
    def _is_close_to_any_mecha(self, tejo_pos, mecha_positions):
        for mecha_pos in mecha_positions:
            distance = self.distance_to_mecha(tejo_pos, mecha_pos)
            if distance <= MECHA_CLOSE_DISTANCE:
                return True
        return False
    
    def distance_to_mecha(self, tejo_pos, mecha_pos):
        dx = tejo_pos[0] - mecha_pos[0]
        dy = tejo_pos[1] - mecha_pos[1]
        dz = tejo_pos[2] - mecha_pos[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)
    
    def is_on_board(self, tejo_position, board_bounds):
        x, y, z = tejo_position
        
        in_x = board_bounds['x_min'] <= x <= board_bounds['x_max']
        in_y = board_bounds['y_min'] <= y <= board_bounds['y_max']
        in_z = board_bounds['z_min'] <= z <= board_bounds['z_max']
        
        return in_x and in_y and in_z
    
    def get_board_bounds_from_angle(self, board_length, board_width, board_angle):
        angle_rad = math.radians(board_angle)
        
        x_projection = board_length * math.cos(angle_rad)
        y_projection = board_length * math.sin(angle_rad)
        
        bounds = {
            'x_min': -0.2,
            'x_max': x_projection + 0.2,
            'y_min': 0,
            'y_max': y_projection + 0.5,
            'z_min': -board_width/2 - 0.1,
            'z_max': board_width/2 + 0.1
        }
        
        return bounds
    
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
    
    def get_score_breakdown(self, tejo_position, mecha_positions, mecha_hits, on_board):
        breakdown = {
            'mecha_hits': 0,
            'close_to_mecha': 0,
            'on_board': 0,
            'total': 0,
            'details': []
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
        
        breakdown['total'] = (
            breakdown['mecha_hits'] + 
            breakdown['close_to_mecha'] + 
            breakdown['on_board']
        )
        
        return breakdown
