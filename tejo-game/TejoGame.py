import os, sys, random
cur_dir = os.path.dirname( os.path.abspath( __file__ ) )
imp_dir = os.path.abspath( os.path.join( cur_dir, './lib' ) )
sys.path.append( imp_dir )
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites
import math

import game
from game.physics_engine import PhysicsEngine
from game.game_state import GameState
from game.scoring_system import ScoringSystem
from game.constants import *

class TejoGame(PUJ_Ogre.BaseApplicationWithVTK):
    def __init__(self):
        super(TejoGame, self).__init__('Juego de Tejo - Deporte Colombiano', '')
        self.m_ResourcesFile = os.path.join(cur_dir, 'resources.cfg')
        
        self.physics = PhysicsEngine()
        self.game_state = GameState()
        self.scoring = ScoringSystem()
        
        self.tejo_nodes = {}
        self.mecha_nodes = []
        self.board_node = None
        
        self.current_tejo_name = None
        self.waiting_for_stop = False
        self.wait_counter = 0
        self.wait_frames = 60
        
        self.tejo_ready = False
        self.dragging = False
        self.drag_start_x = 0
        self.launch_power = 0
        self.launch_angle = 45
        
        self.mecha_positions = []
        self.auto_launch = True
    # end def

    def _cone(self, base_radius, height, segments, top_radius=0.0):
        """Crea un cono truncado (o cono completo si top_radius=0)"""
        P = []  # Posiciones
        N = []  # Normales
        T = []  # Coordenadas de textura
        C = []  # Conectividad (triángulos)

        # Vértices de la base inferior (y = 0)
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = base_radius * math.cos(angle)
            z = base_radius * math.sin(angle)
            P.append([x, 0, z])
            N.append([0, -1, 0])  # Normal hacia abajo
            T.append([i / segments, 0])
        # end for

        # Vértices de la parte superior (y = height)
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            x = top_radius * math.cos(angle)
            z = top_radius * math.sin(angle)
            P.append([x, height, z])
            # Normal calculada para el lado del cono
            nx = math.cos(angle)
            nz = math.sin(angle)
            ny = (base_radius - top_radius) / height
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            N.append([nx/length, ny/length, nz/length])
            T.append([i / segments, 1])
        # end for

        # Centro de la base inferior
        center_bottom = len(P)
        P.append([0, 0, 0])
        N.append([0, -1, 0])
        T.append([0.5, 0.5])

        # Centro de la parte superior
        center_top = len(P)
        P.append([0, height, 0])
        N.append([0, 1, 0])
        T.append([0.5, 0.5])

        # Triángulos de la base inferior
        for i in range(segments):
            next_i = (i + 1) % segments
            C.append([center_bottom, next_i, i])
        # end for

        # Triángulos de la parte superior
        for i in range(segments):
            next_i = (i + 1) % segments
            C.append([center_top, segments + i, segments + next_i])
        # end for

        # Triángulos de los lados
        for i in range(segments):
            next_i = (i + 1) % segments
            # Dos triángulos por segmento lateral
            C.append([i, next_i, segments + i])
            C.append([next_i, segments + next_i, segments + i])
        # end for

        return (P, N, T, C)
    # end def

    def _loadScene(self):
        self.physics.initialize()
        
        root_node = self.m_SceneMgr.getRootSceneNode()
        
        self._createCamera(
            top_speed=3,
            position=[-2.5, 1.5, 6.0],
            look_at=[1.5, 0.8, 0],
            background=[0.53, 0.81, 0.98],
            cam_style=OgreBites.CS_MANUAL
        )
        
        light = self.m_SceneMgr.createLight('MainLight')
        light.setType(Ogre.Light.LT_DIRECTIONAL)
        light.setDiffuseColour(1.0, 1.0, 0.95)
        lightNode = root_node.createChildSceneNode()
        lightNode.setDirection([0.3, -1, -0.2])
        lightNode.attachObject(light)
        
        self.m_SceneMgr.setAmbientLight([0.6, 0.6, 0.6])
        
        self.physics.create_board()
        
        ground_limits = [-3.0, 6.0, -2.0, 2.0]
        ground_node = self._ground('terrain', ground_limits)
        ground_node.setPosition([0, -0.05, 0])
        
        self._create_board_visual()

        self.game_state.start_game()
        self._crear_tejo_para_lanzar()
    # end def

    def _create_board_visual(self):
        limites = [
            -BOARD_LENGTH/2, BOARD_LENGTH/2,
            -BOARD_WIDTH/2, BOARD_WIDTH/2
        ]
        
        c = [(limites[1] + limites[0]) * 0.5, 0.0, (limites[3] + limites[2]) * 0.5]
        p = Ogre.Plane(0, 1, 0, 0)
        m = Ogre.MeshManager.getSingleton().createPlane(
            'board_mesh', 'General', p,
            limites[1] - limites[0],
            limites[3] - limites[2],
            20, 20, True, 1, 5, 5, [0, 0, 1]
        )
        e = self.m_SceneMgr.createEntity('board_entity', 'board_mesh')
        e.setMaterialName('wood')
        self.board_node = self.m_SceneMgr.getRootSceneNode().createChildSceneNode()
        self.board_node.attachObject(e)
        
        angle_rad = math.radians(BOARD_ANGLE)
        board_center_height = (BOARD_LENGTH/2) * math.sin(angle_rad)
        board_center_x = (BOARD_LENGTH/2) * math.cos(angle_rad)
        
        self.board_node.setPosition([board_center_x, board_center_height, 0])
        
        rotation = Ogre.Quaternion(
            math.cos(angle_rad/2), 
            0, 
            0, 
            math.sin(angle_rad/2)
        )
        self.board_node.setOrientation(rotation)
    # end def
    
    def _create_mechas(self):
        mecha_positions_local = [
            [1.0, 0.5, -0.25],
            [1.0, 0.5, 0.25],
            [1.6, 0.9, -0.25],
            [1.6, 0.9, 0.25]
        ]
        
        for i, pos in enumerate(mecha_positions_local):
            self.physics.create_mecha(pos)
            self.mecha_positions.append(pos)
            
            mecha_visual_radius = MECHA_RADIUS * 4
            mecha_data = self._sphere(mecha_visual_radius, 20, 20)
            mecha_node = self._createManualObject(
                mecha_data, 
                f'mecha_{i}', 
                'yellow_material'
            )
            mecha_node.setPosition(pos)
            
            self.mecha_nodes.append(mecha_node)
        # end for
    # end def
    
    def _crear_tejo_para_lanzar(self):
        if self.game_state.is_game_over():
            self._mostrar_resultado_final()
            return
        # end if
        
        status = self.game_state.get_game_status()
        current_team = self.game_state.current_team
        team_name = status['current_team']
        tejo_number = self.game_state.tejos_launched[current_team]
        
        self.current_tejo_name = f"tejo_{team_name}_{tejo_number}"

        # Posición inicial más alta para ver las colisiones
        start_position = [1.5, 3.0, 0.0]

        self.physics.create_tejo(self.current_tejo_name, start_position)

        # Crear visual de cono truncado
        tejo_visual_radius = TEJO_RADIUS * 3.0
        tejo_visual_height = TEJO_HEIGHT * 3.0
        tejo_data = self._cone(tejo_visual_radius, tejo_visual_height, 30, top_radius=tejo_visual_radius * 0.3)

        material = 'red_material' if current_team == 0 else 'green_material'

        tejo_node = self._createManualObject(
            tejo_data,
            self.current_tejo_name,
            material
        )
        tejo_node.setPosition(start_position)
        
        self.tejo_nodes[self.current_tejo_name] = tejo_node
        self.tejo_ready = True
    # end def
    
    def _ejecutar_lanzamiento(self, power, angle):
        if not self.tejo_ready or not self.current_tejo_name:
            return
        # end if
        
        self.physics.launch_tejo(self.current_tejo_name, power, angle)
        
        self.tejo_ready = False
        self.waiting_for_stop = True
        self.wait_counter = 0
    # end def
    
    def mousePressed(self, evt):
        if self.tejo_ready and evt.button == OgreBites.BUTTON_LEFT:
            self.dragging = True
            self.drag_start_x = evt.x
        # end if
        return True
    # end def
    
    def mouseReleased(self, evt):
        if self.dragging and self.tejo_ready:
            drag_distance = self.drag_start_x - evt.x
            
            if drag_distance > 10:
                power = min(100, max(50, drag_distance * 0.5))
                angle = 45
                
                self._ejecutar_lanzamiento(power, angle)
            # end if
            
            self.dragging = False
        # end if
        return True
    # end def
    
    def _procesar_puntuacion(self):
        pos, _ = self.physics.get_tejo_transform(self.current_tejo_name)
        
        collisions = self.physics.check_mecha_collisions()
        mecha_hits = [idx for (name, idx) in collisions if name == self.current_tejo_name]
        
        board_bounds = self.scoring.get_board_bounds_from_angle(
            BOARD_LENGTH, 
            BOARD_WIDTH, 
            BOARD_ANGLE
        )
        
        on_board = self.scoring.is_on_board(pos, board_bounds)
        
        points = self.scoring.calculate_points(
            pos, 
            self.mecha_positions, 
            mecha_hits, 
            on_board
        )
        
        breakdown = self.scoring.get_score_breakdown(
            pos,
            self.mecha_positions,
            mecha_hits,
            on_board
        )
        
        current_team = self.game_state.current_team
        self.game_state.add_score(current_team, points)
        
        self.game_state.next_turn()
    # end def
    
    def _mostrar_resultado_final(self):
        status = self.game_state.get_game_status()
        print(f"\nPartida Finalizada")
        print(f"Equipo A: {status['scores']['A']} puntos")
        print(f"Equipo B: {status['scores']['B']} puntos")
        print(f"Ganador: {status['winner']}")
    # end def
    
    def frameRenderingQueued(self, evt):
        r = super(PUJ_Ogre.BaseApplicationWithVTK, self).frameRenderingQueued(evt)
        
        self.physics.step_simulation(evt.timeSinceLastFrame)
        
        for tejo_name, tejo_node in self.tejo_nodes.items():
            pos, orn = self.physics.get_tejo_transform(tejo_name)
            tejo_node.setPosition(pos)
            tejo_node.setOrientation(
                Ogre.Quaternion(orn[3], orn[0], orn[1], orn[2])
            )
        # end for
        
        if self.waiting_for_stop and self.current_tejo_name:
            if self.physics.is_tejo_stopped(self.current_tejo_name):
                self.wait_counter += 1
                
                if self.wait_counter >= self.wait_frames:
                    self._procesar_puntuacion()
                    
                    self.waiting_for_stop = False
                    self.wait_counter = 0
                    
                    self._crear_tejo_para_lanzar()
                # end if
            # end if
        # end if
        return r
    # end def


def main(argv):
    app = TejoGame()
    app.go()
    # end def


if __name__ == '__main__':
    main(sys.argv)
    # end if
