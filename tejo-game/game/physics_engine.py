import pybullet
from .constants import *

class PhysicsEngine:
    """Motor de física - ABEL"""
    
    def __init__(self):
        self.tejo_bodies = {}
        self.mecha_bodies = []
        self.board_body = None
        # TODO Abel: Inicializar PyBullet
    
    def create_board(self):
        """Crear tablero inclinado"""
        # TODO Abel: Implementar
        pass
    
    def create_tejo(self, name, position):
        """Crear tejo con física"""
        # TODO Abel: Implementar
        pass
    
    def create_mecha(self, position):
        """Crear mecha"""
        # TODO Abel: Implementar
        pass
    
    def launch_tejo(self, name, force, angle):
        """Lanzar tejo"""
        # TODO Abel: Implementar
        pass
    
    def step_simulation(self, delta_time):
        """Avanzar física"""
        # TODO Abel: pybullet.stepSimulation()
        pass
    
    def get_tejo_transform(self, name):
        """Obtener posición y rotación"""
        # TODO Abel: Implementar
        return ([0, 0, 0], [1, 0, 0, 0])
    
    def check_mecha_collisions(self):
        """Detectar colisiones con mechas"""
        # TODO Abel: Implementar
        return []

