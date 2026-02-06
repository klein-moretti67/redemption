import pyray as rl
import math

class CameraController:
    def __init__(self):
        self.camera = rl.Camera3D()
        self.camera.position = rl.Vector3(0.0, 10.0, 10.0)
        self.camera.target = rl.Vector3(0.0, 0.0, 0.0)
        self.camera.up = rl.Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 45.0
        self.camera.projection = rl.CAMERA_PERSPECTIVE
        
        # Camera control parameters
        self.distance = 10.0
        self.target_distance = 10.0
        self.angle_x = 0.0
        self.angle_y = 0.3
        self.sensitivity = 0.003
        
        # Mode settings
        self.on_foot_distance = 10.0
        self.driving_distance = 18.0
        self.is_driving = False
        
    def set_driving_mode(self, driving):
        """Switch camera mode for driving."""
        self.is_driving = driving
        self.target_distance = self.driving_distance if driving else self.on_foot_distance
        
    def update(self, target_position):
        # Smooth distance transition
        self.distance += (self.target_distance - self.distance) * 0.1
        
        # Update target to follow player
        self.camera.target = target_position
        
        # Mouse input for orbit
        mouse_delta = rl.get_mouse_delta()
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_RIGHT):
            self.angle_x -= mouse_delta.x * self.sensitivity
            self.angle_y -= mouse_delta.y * self.sensitivity
            
            # Clamp vertical angle
            self.angle_y = max(min(self.angle_y, 1.5), -0.1)
            
        # Calculate new camera position (spherical coordinates)
        horiz_dist = self.distance * math.cos(self.angle_y)
        vert_dist = self.distance * math.sin(self.angle_y)
        
        self.camera.position.x = target_position.x - horiz_dist * math.sin(self.angle_x)
        self.camera.position.z = target_position.z - horiz_dist * math.cos(self.angle_x)
        self.camera.position.y = target_position.y + vert_dist + (3.0 if self.is_driving else 0)
