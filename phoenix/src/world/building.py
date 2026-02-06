import pyray as rl

class Building:
    """A building with LOD support."""
    
    def __init__(self, position, size, color_rgb):
        self.position = rl.Vector3(position[0], position[1], position[2])
        self.size = rl.Vector3(size[0], size[1], size[2])
        self.color = rl.Color(color_rgb[0], color_rgb[1], color_rgb[2], 255)
        
    def draw(self, camera_position, lod_distances=(50, 150)):
        """Draw building with LOD based on distance."""
        dx = self.position.x - camera_position.x
        dz = self.position.z - camera_position.z
        distance = (dx*dx + dz*dz) ** 0.5
        
        near_dist, far_dist = lod_distances
        
        if distance < near_dist:
            # Full detail
            rl.draw_cube_v(self.position, self.size, self.color)
            rl.draw_cube_wires_v(self.position, self.size, rl.BLACK)
        elif distance < far_dist:
            # Simplified (no wires)
            rl.draw_cube_v(self.position, self.size, self.color)
        else:
            # Billboard/very simple - just a flat plane facing camera
            rl.draw_cube_v(self.position, rl.Vector3(self.size.x, self.size.y, 0.5), self.color)
