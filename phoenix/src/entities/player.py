import pyray as rl

class Player:
    def __init__(self, name, start_pos_tuple, color):
        self.name = name
        self.position = rl.Vector3(start_pos_tuple[0], start_pos_tuple[1], start_pos_tuple[2])
        self.speed = 5.0
        self.size = rl.Vector3(1.0, 2.0, 1.0)
        self.color = color
        self.is_active = False
        
        # Vehicle state
        self.in_vehicle = False
        self.current_vehicle = None
        
    def update(self, dt):
        # Skip movement if in vehicle or not active
        if not self.is_active or self.in_vehicle:
            return
            
        # Basic Movement (Standard WSAD relative to world)
        if rl.is_key_down(rl.KEY_W):
            self.position.z -= self.speed * dt
        if rl.is_key_down(rl.KEY_S):
            self.position.z += self.speed * dt
        if rl.is_key_down(rl.KEY_A):
            self.position.x -= self.speed * dt
        if rl.is_key_down(rl.KEY_D):
            self.position.x += self.speed * dt
            
    def draw(self):
        # Don't draw if in vehicle
        if self.in_vehicle:
            return
            
        # Draw with reduced opacity if not active
        draw_color = self.color if self.is_active else rl.fade(self.color, 0.5)
        rl.draw_cube(self.position, self.size.x, self.size.y, self.size.z, draw_color)
        rl.draw_cube_wires(self.position, self.size.x, self.size.y, self.size.z, rl.BLACK)
