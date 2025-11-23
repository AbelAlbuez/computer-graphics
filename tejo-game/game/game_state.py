from enum import Enum
from .constants import *

class GamePhase(Enum):
    MENU = 0
    AIMING = 1
    LAUNCHING = 2
    SCORING = 3
    END_TURN = 4
    GAME_OVER = 5

class GameState:
    """Estado del juego - ABEL"""
    
    def __init__(self):
        self.current_phase = GamePhase.MENU
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
    
    def start_game(self):
        """Iniciar partida"""
        self.current_phase = GamePhase.AIMING
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
    
    def next_turn(self):
        """Siguiente turno"""
        # TODO Abel: Implementar
        pass
    
    def add_score(self, team, points):
        """Agregar puntos"""
        self.scores[team] += points
    
    def is_game_over(self):
        """Verificar fin del juego"""
        # TODO Abel: Implementar
        return False

