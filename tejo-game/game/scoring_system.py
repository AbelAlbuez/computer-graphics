from .constants import *
import math

class ScoringSystem:
    """Sistema de puntuación - ABEL"""
    
    def calculate_points(self, tejo_position, mecha_positions, mecha_hits, on_board):
        """Calcular puntos de un tejo"""
        points = 0
        
        # Mecha golpeada
        if len(mecha_hits) > 0:
            points += POINTS_MECHA * len(mecha_hits)
        
        # TODO Abel: Verificar cercanía a mecha
        # TODO Abel: Verificar si está en tablero
        
        return points
    
    def distance_to_mecha(self, tejo_pos, mecha_pos):
        """Distancia entre tejo y mecha"""
        dx = tejo_pos[0] - mecha_pos[0]
        dy = tejo_pos[1] - mecha_pos[1]
        dz = tejo_pos[2] - mecha_pos[2]
        return math.sqrt(dx*dx + dy*dy + dz*dz)

