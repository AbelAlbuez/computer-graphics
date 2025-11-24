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
    def __init__(self):
        self.current_phase = GamePhase.MENU
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]  # Total de tejos lanzados por equipo
        self.round_number = 1
        self.winner = None
        self.current_turn_tejos = {}  # {team: (position, distance_to_disc)}
        self.current_round_throws = [0, 0]  # Lanzamientos en la ronda actual
        self.figura_achieved = False  # Si se logró mecha/embocinada/moñona
        self.team_with_figura = None  # Equipo que logró la figura
        self.players_pending = [list(range(6)), list(range(6))]  # Jugadores que faltan lanzar por equipo
    
    def start_game(self):
        self.current_phase = GamePhase.AIMING
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
        self.round_number = 1
        self.winner = None
        self.current_turn_tejos = {}
        self.current_round_throws = [0, 0]
        self.figura_achieved = False
        self.team_with_figura = None
        self.players_pending = [list(range(6)), list(range(6))]
    
    def next_turn(self):
        self.tejos_launched[self.current_team] += 1
        self.current_round_throws[self.current_team] += 1
        
        # Remover jugador que acaba de lanzar
        if self.players_pending[self.current_team]:
            self.players_pending[self.current_team].pop(0)
        
        # Si se logró una figura, terminar la ronda
        if self.figura_achieved:
            self._end_round_with_figura()
            return
        
        # Alternar entre equipos después de cada lanzamiento
        self.current_team = 1 - self.current_team
        
        # Verificar si la ronda terminó (ambos equipos lanzaron 6 tejos en esta ronda)
        if all(throws >= TEJOS_PER_TEAM for throws in self.current_round_throws):
            self._end_round()
        else:
            self.current_phase = GamePhase.AIMING
    
    def _end_round_with_figura(self):
        """Termina la ronda cuando se logra una figura"""
        print(f"\n¡FIGURA! Se suspenden los lanzamientos restantes de esta ronda.")
        print(f"Equipo {'A' if self.team_with_figura == 0 else 'B'} lanzará primero en la siguiente ronda.\n")
        self._start_new_round()
    
    def _end_round(self):
        """Termina una ronda normal"""
        self._start_new_round()
    
    def _start_new_round(self):
        """Inicia una nueva ronda"""
        # Verificar si algún equipo alcanzó 27 puntos
        if self.scores[0] >= WINNING_SCORE or self.scores[1] >= WINNING_SCORE:
            self.current_phase = GamePhase.GAME_OVER
            self._determine_winner()
            return
        
        self.round_number += 1
        self.current_round_throws = [0, 0]
        self.current_turn_tejos = {}
        
        # Resetear contador de tejos lanzados para la nueva ronda
        # pero mantener el total para saber qué jugador sigue
        # Los players_pending ya manejan el orden
        
        # Determinar quién empieza la siguiente ronda
        if self.team_with_figura is not None:
            self.current_team = self.team_with_figura
        # Si no hubo figura, mantener el equipo actual
        
        # Resetear estado de figura
        self.figura_achieved = False
        self.team_with_figura = None
        
        # Los jugadores que no lanzaron van primero, luego los que sí lanzaron
        for team in range(NUM_TEAMS):
            players_that_threw = TEJOS_PER_TEAM - len(self.players_pending[team])
            self.players_pending[team] = list(range(players_that_threw, TEJOS_PER_TEAM)) + list(range(players_that_threw))
        
        self.current_phase = GamePhase.AIMING
    
    def add_score(self, team, points):
        if 0 <= team < NUM_TEAMS:
            self.scores[team] += points
    
    def register_figura(self, team):
        """Registra que un equipo logró una figura (mecha, embocinada o moñona)"""
        self.figura_achieved = True
        self.team_with_figura = team
    
    def register_tejo_for_turn(self, team, position, distance_to_disc):
        """Registra el tejo lanzado en el turno actual"""
        self.current_turn_tejos[team] = (position, distance_to_disc)
    
    def is_game_over(self):
        # El juego solo termina cuando alguien alcanza 27 puntos
        return (self.scores[0] >= WINNING_SCORE or 
                self.scores[1] >= WINNING_SCORE or
                self.current_phase == GamePhase.GAME_OVER)
    
    def get_current_team_name(self):
        return self._get_team_name(self.current_team)
    
    def get_score(self, team):
        return self.scores[team] if 0 <= team < NUM_TEAMS else 0
    
    def get_tejos_remaining(self, team):
        # Usar current_round_throws en lugar de tejos_launched para contar por ronda
        return TEJOS_PER_TEAM - self.current_round_throws[team] if 0 <= team < NUM_TEAMS else 0
    
    def _get_team_name(self, team):
        return "A" if team == 0 else "B"
    
    def _determine_winner(self):
        if self.scores[0] > self.scores[1]:
            self.winner = 0
        elif self.scores[1] > self.scores[0]:
            self.winner = 1
        else:
            self.winner = None
    
    def get_winner_name(self):
        return "Empate" if self.winner is None else self._get_team_name(self.winner)
    
    def award_closest_tejo_point_for_turn(self):
        """Otorga 1 punto al equipo con el tejo más cercano en este turno"""
        if len(self.current_turn_tejos) < 2:
            return None
        
        # Comparar distancias de ambos tejos del turno
        team_0_data = self.current_turn_tejos.get(0)
        team_1_data = self.current_turn_tejos.get(1)
        
        if team_0_data and team_1_data:
            dist_0 = team_0_data[1]
            dist_1 = team_1_data[1]
            
            if dist_0 < dist_1:
                winning_team = 0
                winning_dist = dist_0
            else:
                winning_team = 1
                winning_dist = dist_1
            
            # Otorgar 1 punto
            self.scores[winning_team] += 1
            
            # Limpiar para el siguiente turno
            self.current_turn_tejos = {}
            
            return (winning_team, winning_dist)
        
        return None
    
    def reset(self):
        self.current_phase = GamePhase.MENU
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
        self.round_number = 1
        self.winner = None
        self.current_turn_tejos = {}
        self.current_round_throws = [0, 0]
        self.figura_achieved = False
        self.team_with_figura = None
        self.players_pending = [list(range(6)), list(range(6))]
    
    def get_game_status(self):
        return {
            'phase': self.current_phase.name,
            'current_team': self._get_team_name(self.current_team),
            'scores': {
                'A': self.scores[0],
                'B': self.scores[1]
            },
            'tejos_launched': {
                'A': self.tejos_launched[0],
                'B': self.tejos_launched[1]
            },
            'tejos_remaining': {
                'A': self.get_tejos_remaining(0),
                'B': self.get_tejos_remaining(1)
            },
            'is_over': self.is_game_over(),
            'winner': self.get_winner_name() if self.is_game_over() else None
        }
