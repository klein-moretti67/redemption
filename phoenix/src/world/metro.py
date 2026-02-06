import pyray as rl
import math

class Metro:
    """Metro system connecting cities."""
    
    def __init__(self, cities):
        self.stations = []
        for i, city in enumerate(cities):
            pos = city['metro_station']
            self.stations.append({
                'city_index': i,
                'city_name': city['name'],
                'position': rl.Vector3(pos[0], 0, pos[2])
            })
            
    def find_nearby_station(self, player_position, max_distance=8.0):
        """Find a metro station near the player."""
        for station in self.stations:
            dx = station['position'].x - player_position.x
            dz = station['position'].z - player_position.z
            distance = math.sqrt(dx*dx + dz*dz)
            if distance < max_distance:
                return station
        return None
    
    def get_destinations(self, current_station):
        """Get other stations as destinations."""
        return [s for s in self.stations if s['city_index'] != current_station['city_index']]
    
    def teleport_to(self, player, destination_station):
        """Teleport player to destination station."""
        player.position.x = destination_station['position'].x
        player.position.z = destination_station['position'].z + 3
        player.position.y = 1.0
        
    def draw_stations(self):
        """Draw metro station markers."""
        for station in self.stations:
            # Draw station platform
            rl.draw_cube(
                rl.Vector3(station['position'].x, 0.2, station['position'].z),
                6, 0.4, 6,
                rl.DARKBLUE
            )
            # Draw station pillar/marker
            rl.draw_cylinder(
                rl.Vector3(station['position'].x, 0, station['position'].z - 2),
                0.3, 0.3, 4.0, 8,
                rl.BLUE
            )
