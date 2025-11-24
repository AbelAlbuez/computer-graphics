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
        self.tejos_launched = [0, 0]
        self.round_number = 1
        self.winner = None
    
    def start_game(self):
        self.current_phase = GamePhase.AIMING
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
        self.round_number = 1
        self.winner = None
    
    def next_turn(self):
        self.tejos_launched[self.current_team] += 1
        
        if self.tejos_launched[self.current_team] >= TEJOS_PER_TEAM:
            self.current_team = 1 - self.current_team
            
            if self.tejos_launched[self.current_team] >= TEJOS_PER_TEAM:
                self.current_phase = GamePhase.GAME_OVER
                self._determine_winner()
            else:
                self.current_phase = GamePhase.AIMING
        else:
            self.current_phase = GamePhase.AIMING
    
    def add_score(self, team, points):
        if 0 <= team < NUM_TEAMS:
            self.scores[team] += points
    
    def is_game_over(self):
        return (all(launched >= TEJOS_PER_TEAM for launched in self.tejos_launched) or
                self.current_phase == GamePhase.GAME_OVER)
    
    def get_current_team_name(self):
        return self._get_team_name(self.current_team)
    
    def get_score(self, team):
        return self.scores[team] if 0 <= team < NUM_TEAMS else 0
    
    def get_tejos_remaining(self, team):
        return TEJOS_PER_TEAM - self.tejos_launched[team] if 0 <= team < NUM_TEAMS else 0
    
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
    
    def reset(self):
        self.current_phase = GamePhase.MENU
        self.current_team = 0
        self.scores = [0, 0]
        self.tejos_launched = [0, 0]
        self.round_number = 1
        self.winner = None
    
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
