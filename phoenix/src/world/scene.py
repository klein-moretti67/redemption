import pyray as rl
import os
from src.world.city_loader import CityLoader
from src.world.metro import Metro

class Scene:
    """Manages the game world including cities and metro."""
    
    def __init__(self):
        # Get the path to assets relative to main.py
        self.cities_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'cities')
        self.cities = CityLoader.load_all_cities(self.cities_dir)
        self.metro = Metro(self.cities) if self.cities else None
        self.camera_position = rl.Vector3(0, 0, 0)
        
        # LOD settings
        self.lod_near = 50
        self.lod_far = 150
        
    def update(self, dt, camera_position=None):
        if camera_position:
            self.camera_position = camera_position
        
    def draw(self):
        # Draw ground planes for each city
        for city in self.cities:
            center = city['center']
            rl.draw_plane(
                rl.Vector3(center[0], 0, center[2]),
                rl.Vector2(80, 80),
                rl.DARKGRAY
            )
        
        # Draw main connecting ground
        rl.draw_plane(rl.Vector3(0, -0.1, 0), rl.Vector2(300, 100), rl.GRAY)
        
        # Draw buildings with LOD
        for city in self.cities:
            for building in city['buildings']:
                building.draw(self.camera_position, (self.lod_near, self.lod_far))
                
        # Draw metro stations
        if self.metro:
            self.metro.draw_stations()
            
        # Draw grid for reference
        rl.draw_grid(100, 5.0)
