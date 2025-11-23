import pybullet
import math
from .constants import *

class PhysicsEngine:
    def __init__(self):
        self.tejo_bodies = {}
        self.mecha_bodies = []
        self.board_body = None
        self.initialized = False
    
    def initialize(self):
        if not self.initialized:
            pybullet.connect(pybullet.DIRECT)
            pybullet.setGravity(0, GRAVITY, 0)
            pybullet.setPhysicsEngineParameter(numSolverIterations=10)
            self.initialized = True
    
    def create_board(self):
        half_extents = [BOARD_LENGTH/2, 0.05, BOARD_WIDTH/2]
        
        board_shape = pybullet.createCollisionShape(
            pybullet.GEOM_BOX,
            halfExtents=half_extents
        )
        
        angle_rad = math.radians(BOARD_ANGLE)
        orientation = pybullet.getQuaternionFromEuler([0, 0, angle_rad])
        
        board_center_height = (BOARD_LENGTH/2) * math.sin(angle_rad)
        position = [0, board_center_height, 0]
        
        self.board_body = pybullet.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=board_shape,
            basePosition=position,
            baseOrientation=orientation
        )
        
        pybullet.changeDynamics(
            self.board_body,
            -1,
            restitution=0.1,
            lateralFriction=BOARD_FRICTION,
            spinningFriction=0.5,
            rollingFriction=0.3
        )
        
        return self.board_body
    
    def create_tejo(self, name, position):
        tejo_shape = pybullet.createCollisionShape(
            pybullet.GEOM_CYLINDER,
            radius=TEJO_RADIUS,
            height=TEJO_HEIGHT
        )
        
        tejo_body = pybullet.createMultiBody(
            baseMass=TEJO_MASS,
            baseCollisionShapeIndex=tejo_shape,
            basePosition=position,
            baseOrientation=[0, 0, 0, 1]
        )
        
        pybullet.changeDynamics(
            tejo_body,
            -1,
            restitution=TEJO_RESTITUTION,
            lateralFriction=TEJO_FRICTION,
            spinningFriction=0.3,
            rollingFriction=0.2
        )
        
        self.tejo_bodies[name] = tejo_body
        return tejo_body
    
    def create_mecha(self, position):
        mecha_shape = pybullet.createCollisionShape(
            pybullet.GEOM_SPHERE,
            radius=MECHA_RADIUS
        )
        
        mecha_body = pybullet.createMultiBody(
            baseMass=MECHA_MASS,
            baseCollisionShapeIndex=mecha_shape,
            basePosition=position
        )
        
        pybullet.changeDynamics(
            mecha_body,
            -1,
            restitution=0.2,
            lateralFriction=2.0
        )
        
        self.mecha_bodies.append(mecha_body)
        return mecha_body
    
    def launch_tejo(self, name, force, angle):
        if name not in self.tejo_bodies:
            return
        
        tejo_body = self.tejo_bodies[name]
        
        velocity_magnitude = (force / 100.0) * 20.0
        angle_rad = math.radians(angle)
        
        vx = velocity_magnitude * math.cos(angle_rad)
        vy = velocity_magnitude * math.sin(angle_rad)
        vz = 0
        
        pybullet.resetBaseVelocity(
            tejo_body,
            linearVelocity=[vx, vy, vz],
            angularVelocity=[0, 0, 0]
        )
    
    def step_simulation(self, delta_time):
        pybullet.setTimeStep(delta_time)
        pybullet.stepSimulation()
    
    def get_tejo_transform(self, name):
        if name not in self.tejo_bodies:
            return ([0, 0, 0], [0, 0, 0, 1])
        
        tejo_body = self.tejo_bodies[name]
        pos, orn = pybullet.getBasePositionAndOrientation(tejo_body)
        return (pos, orn)
    
    def get_mecha_transform(self, index):
        if index < 0 or index >= len(self.mecha_bodies):
            return ([0, 0, 0], [0, 0, 0, 1])
        
        pos, orn = pybullet.getBasePositionAndOrientation(self.mecha_bodies[index])
        return (pos, orn)
    
    def check_mecha_collisions(self):
        collisions = []
        
        for tejo_name, tejo_body in self.tejo_bodies.items():
            for mecha_idx, mecha_body in enumerate(self.mecha_bodies):
                contact_points = pybullet.getContactPoints(
                    bodyA=tejo_body,
                    bodyB=mecha_body
                )
                
                if len(contact_points) > 0:
                    collisions.append((tejo_name, mecha_idx))
        
        return collisions
    
    def get_tejo_velocity(self, name):
        if name not in self.tejo_bodies:
            return [0, 0, 0]
        
        linear_vel, _ = pybullet.getBaseVelocity(self.tejo_bodies[name])
        return linear_vel
    
    def is_tejo_stopped(self, name, threshold=0.1):
        velocity = self.get_tejo_velocity(name)
        speed = math.sqrt(velocity[0]**2 + velocity[1]**2 + velocity[2]**2)
        return speed < threshold
    
    def cleanup(self):
        if self.initialized:
            pybullet.disconnect()
            self.initialized = False
