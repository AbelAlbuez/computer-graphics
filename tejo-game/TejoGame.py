import os, sys, random, math
cur_dir = os.path.dirname(os.path.abspath(__file__))
imp_dir = os.path.abspath(os.path.join(cur_dir, './lib'))
sys.path.append(imp_dir)
import pybullet, Ogre, PUJ_Ogre
import Ogre.Bites as OgreBites

import game
from game.physics_engine import PhysicsEngine
from game.game_state import GameState
from game.scoring_system import ScoringSystem
from game.ui_system import UISystem
from game.constants import *

class TejoInputListener(OgreBites.InputListener):
    def __init__(self, game):
        OgreBites.InputListener.__init__(self)
        self.game = game
    
    def keyPressed(self, evt):
        if evt.keysym.sym == 119:  # W
            self.game.launch_power = min(100, self.game.launch_power + 5)
            self.game.ui_system.update_power(self.game.launch_power)
        elif evt.keysym.sym == 115:  # S
            self.game.launch_power = max(50, self.game.launch_power - 5)
            self.game.ui_system.update_power(self.game.launch_power)
        elif evt.keysym.sym == OgreBites.SDLK_UP:
            self.game.launch_angle = min(70, self.game.launch_angle + 5)
            self.game.ui_system.update_angle(self.game.launch_angle)
        elif evt.keysym.sym == OgreBites.SDLK_DOWN:
            self.game.launch_angle = max(20, self.game.launch_angle - 5)
            self.game.ui_system.update_angle(self.game.launch_angle)
        elif evt.keysym.sym == 32:  # SPACE
            if self.game.tejo_ready:
                self.game._ejecutar_lanzamiento(self.game.launch_power, self.game.launch_angle)
        elif evt.keysym.sym == OgreBites.SDLK_ESCAPE:
            self.game.getRoot().queueEndRendering()
        
        return True

class TejoGame(PUJ_Ogre.BaseApplicationWithVTK):
    def __init__(self):
        super(TejoGame, self).__init__('Juego de Tejo - Deporte Colombiano', '')
        self.m_ResourcesFile = os.path.join(cur_dir, 'resources.cfg')
        
        self.physics = PhysicsEngine()
        self.game_state = GameState()
        self.scoring = ScoringSystem()
        self.ui_system = None
        
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
        self.launch_power = 75
        self.launch_angle = 45
        self.last_launch_force = 75
        
        self.mecha_positions = []
        self.auto_launch = False
        
        self.ui_power_input = None
        self.ui_angle_input = None
        self.ui_launch_button = None
        self.ui_tray = None

    def _cone(self, base_radius, height, segments, top_radius=0.0):
        P, N, T, C = [], [], [], []

        for i in range(segments):
            angle = 2 * math.pi * i / segments
            P.append([base_radius * math.cos(angle), 0, base_radius * math.sin(angle)])
            N.append([0, -1, 0])
            T.append([i / segments, 0])

        for i in range(segments):
            angle = 2 * math.pi * i / segments
            nx = math.cos(angle)
            nz = math.sin(angle)
            ny = (base_radius - top_radius) / height
            length = math.sqrt(nx*nx + ny*ny + nz*nz)
            P.append([top_radius * math.cos(angle), height, top_radius * math.sin(angle)])
            N.append([nx/length, ny/length, nz/length])
            T.append([i / segments, 1])

        center_bottom = len(P)
        P.append([0, 0, 0])
        N.append([0, -1, 0])
        T.append([0.5, 0.5])

        center_top = len(P)
        P.append([0, height, 0])
        N.append([0, 1, 0])
        T.append([0.5, 0.5])

        for i in range(segments):
            next_i = (i + 1) % segments
            C.append([center_bottom, next_i, i])
            C.append([center_top, segments + i, segments + next_i])
            C.append([i, next_i, segments + i])
            C.append([next_i, segments + next_i, segments + i])

        return (P, N, T, C)

    def _loadScene(self):
        self.physics.initialize()
        
        root_node = self.m_SceneMgr.getRootSceneNode()
        
        angle_rad = math.radians(BOARD_ANGLE)
        board_center_height = (BOARD_LENGTH/2) * math.sin(angle_rad)
        board_center_x = (BOARD_LENGTH/2) * math.cos(angle_rad)
        camera_distance = 15.0
        camera_height = 1.5

        self._createCamera(
            top_speed=3,
            position=[board_center_x - camera_distance, camera_height, 0.0],
            look_at=[board_center_x, camera_height, 0],
            background=[0.53, 0.81, 0.98],
            cam_style=OgreBites.CS_MANUAL
        )
        
        self.main_camera = self.m_SceneMgr.getCamera('MainCamera')
        
        light = self.m_SceneMgr.createLight('MainLight')
        light.setType(Ogre.Light.LT_DIRECTIONAL)
        light.setDiffuseColour(1.0, 1.0, 0.95)
        lightNode = root_node.createChildSceneNode()
        lightNode.setDirection([0.3, -1, -0.2])
        lightNode.attachObject(light)
        
        self.m_SceneMgr.setAmbientLight([0.6, 0.6, 0.6])
        
        self.physics.create_board()
        
        ground_limits = [-50.0, 50.0, -50.0, 50.0]
        ground_node = self._ground('ground', ground_limits)
        ground_node.setPosition([0, -0.05, 0])
        
        self._create_board_visual()
        self._create_mechas()

        self.game_state.start_game()
        
        self.ui_system = UISystem(self.m_SceneMgr, self.main_camera)
        self.ui_system.initialize()
        self.ui_system.update(self.launch_power, self.launch_angle)
        
        self.ui_system.update_team_display("A", 0, TEJOS_PER_TEAM)
        self.ui_system.update_score_display(0, 0)
        
        self._crear_tejo_para_lanzar()
        
        self.input_listener = TejoInputListener(self)
        self.addInputListener(self.input_listener)

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
        e.setMaterialName('arcilla_material')
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
    
    def _crear_tejo_para_lanzar(self):
        if self.game_state.is_game_over():
            self._mostrar_resultado_final()
            return
        
        status = self.game_state.get_game_status()
        current_team = self.game_state.current_team
        team_name = status['current_team']
        tejo_number = self.game_state.tejos_launched[current_team]
        
        tejos_remaining = status['tejos_remaining'][team_name]
        self.ui_system.update_team_display(team_name, current_team, tejos_remaining)
        self.ui_system.update_score_display(
            self.game_state.scores[0], 
            self.game_state.scores[1]
        )
        
        self.current_tejo_name = f"tejo_{team_name}_{tejo_number}"

        angle_rad = math.radians(BOARD_ANGLE)
        board_center_x = (BOARD_LENGTH / 2) * math.cos(angle_rad)
        board_start_x = board_center_x - (BOARD_LENGTH / 2) * math.cos(angle_rad)
        start_position = [board_start_x - 15, TEJO_HEIGHT * 0.5, 0.0]

        self.physics.create_tejo(self.current_tejo_name, start_position)

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
    
    def _ejecutar_lanzamiento(self, power, angle):
        if not self.tejo_ready or not self.current_tejo_name:
            return
        
        self.last_launch_force = power
        self.ui_system.show_launch_info(power, angle)
        
        self.physics.launch_tejo(self.current_tejo_name, power, angle)
        
        self.tejo_ready = False
        self.waiting_for_stop = True
        self.wait_counter = 0
    
    def mousePressed(self, evt):
        if self.tejo_ready and evt.button == OgreBites.BUTTON_LEFT:
            self.dragging = True
            self.drag_start_x = evt.x
        return True
    
    def mouseReleased(self, evt):
        if self.dragging and self.tejo_ready:
            drag_distance = self.drag_start_x - evt.x
            
            if drag_distance > 10:
                power = min(100, max(50, drag_distance * 0.5))
                angle = 45
                self._ejecutar_lanzamiento(power, angle)
            
            self.dragging = False
        return True
    
    def buttonHit(self, button):
        if button.getName() == 'LaunchButton' and self.tejo_ready:
            power = self.ui_power_input.getValue()
            angle = self.ui_angle_input.getValue()
            self._ejecutar_lanzamiento(power, angle)
        return True
    
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
            on_board,
            self.last_launch_force
        )
        
        breakdown = self.scoring.get_score_breakdown(
            pos,
            self.mecha_positions,
            mecha_hits,
            on_board,
            self.last_launch_force
        )
        
        current_team = self.game_state.current_team
        self.game_state.add_score(current_team, points)
        
        team_scores = [self.game_state.scores[0], self.game_state.scores[1]]
        self.ui_system.show_score_info(breakdown, team_scores, current_team)
        
        self.game_state.next_turn()
    
    def _mostrar_resultado_final(self):
        status = self.game_state.get_game_status()
        print("\n" + "="*50)
        print("¡¡¡ PARTIDA FINALIZADA !!!")
        print("="*50)
        print(f"Equipo A: {status['scores']['A']} puntos")
        print(f"Equipo B: {status['scores']['B']} puntos")
        print("-"*50)
        
        if status['winner'] == "Empate":
            print(f"RESULTADO: ¡EMPATE!")
        else:
            print(f"GANADOR: ¡¡¡EQUIPO {status['winner']}!!!")
        
        print("="*50)
        
        self.ui_system.update_score_display(
            status['scores']['A'], 
            status['scores']['B']
        )
    
    def frameRenderingQueued(self, evt):
        r = super(PUJ_Ogre.BaseApplicationWithVTK, self).frameRenderingQueued(evt)
        
        self.physics.step_simulation(evt.timeSinceLastFrame)
        
        for tejo_name, tejo_node in self.tejo_nodes.items():
            pos, orn = self.physics.get_tejo_transform(tejo_name)
            tejo_node.setPosition(pos)
            tejo_node.setOrientation(
                Ogre.Quaternion(orn[3], orn[0], orn[1], orn[2])
            )
        
        if self.waiting_for_stop and self.current_tejo_name:
            if self.physics.is_tejo_stopped(self.current_tejo_name):
                self.wait_counter += 1
                
                if self.wait_counter >= self.wait_frames:
                    self._procesar_puntuacion()
                    
                    self.waiting_for_stop = False
                    self.wait_counter = 0
                    
                    self._crear_tejo_para_lanzar()
        
        return r


def main(argv):
    app = TejoGame()
    app.go()


if __name__ == '__main__':
    main(sys.argv)
