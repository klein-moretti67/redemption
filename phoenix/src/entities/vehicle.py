import pyray as rl
import math

class Vehicle:
    """Arcade-style vehicle with simple physics."""
    
    def __init__(self, position_tuple, color=rl.ORANGE):
        self.position = rl.Vector3(position_tuple[0], position_tuple[1], position_tuple[2])
        self.rotation = 0.0  # Y-axis rotation in radians
        self.speed = 0.0
        self.color = color
        
        # Physics parameters
        self.max_speed = 20.0
        self.acceleration = 15.0
        self.brake_power = 25.0
        self.friction = 5.0
        self.turn_speed = 2.5
        
        # Dimensions
        self.length = 4.0
        self.width = 2.0
        self.height = 1.5
        
        # State
        self.driver = None
        
    @property
    def is_occupied(self):
        return self.driver is not None
        
    def enter(self, player):
        """Player enters the vehicle."""
        self.driver = player
        player.in_vehicle = True
        player.current_vehicle = self
        
    def exit(self):
        """Player exits the vehicle."""
        if self.driver:
            # Position player next to vehicle
            exit_offset_x = math.sin(self.rotation + math.pi/2) * 2.5
            exit_offset_z = math.cos(self.rotation + math.pi/2) * 2.5
            self.driver.position.x = self.position.x + exit_offset_x
            self.driver.position.z = self.position.z + exit_offset_z
            self.driver.position.y = 1.0
            
            self.driver.in_vehicle = False
            self.driver.current_vehicle = None
            self.driver = None
            
    def update(self, dt):
        """Update vehicle physics."""
        if not self.is_occupied:
            # Apply friction when unoccupied
            if abs(self.speed) > 0.1:
                self.speed -= self.friction * dt * (1 if self.speed > 0 else -1)
            else:
                self.speed = 0
            return
            
        # Driving controls
        if rl.is_key_down(rl.KEY_W):
            self.speed += self.acceleration * dt
        elif rl.is_key_down(rl.KEY_S):
            self.speed -= self.brake_power * dt
        else:
            # Natural friction
            if abs(self.speed) > 0.1:
                self.speed -= self.friction * dt * (1 if self.speed > 0 else -1)
            else:
                self.speed = 0
                
        # Clamp speed
        self.speed = max(-self.max_speed * 0.3, min(self.speed, self.max_speed))
        
        # Steering (only when moving)
        if abs(self.speed) > 0.5:
            turn_factor = self.speed / self.max_speed  # Tighter turns at lower speeds
            if rl.is_key_down(rl.KEY_A):
                self.rotation += self.turn_speed * dt * (0.5 + 0.5 * abs(turn_factor))
            if rl.is_key_down(rl.KEY_D):
                self.rotation -= self.turn_speed * dt * (0.5 + 0.5 * abs(turn_factor))
                
        # Move vehicle
        self.position.x += math.sin(self.rotation) * self.speed * dt
        self.position.z += math.cos(self.rotation) * self.speed * dt
        
        # Update driver position to follow vehicle
        if self.driver:
            self.driver.position.x = self.position.x
            self.driver.position.z = self.position.z
            self.driver.position.y = self.position.y + 0.5
            
    def draw(self):
        """Draw the vehicle as a box."""
        rl.draw_cube_v(
            self.position,
            rl.Vector3(self.width, self.height, self.length),
            self.color
        )
        rl.draw_cube_wires_v(
            self.position,
            rl.Vector3(self.width, self.height, self.length),
            rl.BLACK
        )
        
        # Draw direction indicator
        front_x = self.position.x + math.sin(self.rotation) * self.length * 0.6
        front_z = self.position.z + math.cos(self.rotation) * self.length * 0.6
        rl.draw_sphere(
            rl.Vector3(front_x, self.position.y + 0.5, front_z),
            0.3,
            rl.YELLOW
        )
        
    def get_bounding_box(self):
        """Get AABB for collision detection."""
        half_w = self.width / 2
        half_l = self.length / 2
        half_h = self.height / 2
        return rl.BoundingBox(
            rl.Vector3(self.position.x - half_w, self.position.y - half_h, self.position.z - half_l),
            rl.Vector3(self.position.x + half_w, self.position.y + half_h, self.position.z + half_l)
        )
