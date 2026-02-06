import pyray as rl
from src.entities.player import Player
from src.entities.vehicle import Vehicle
import math

class CharacterManager:
    """Manages the three protagonists, vehicles, and handles switching."""
    
    def __init__(self):
        # Create the trio with different spawn points
        self.characters = [
            Player("Michael", (0, 1, 0), rl.RED),
            Player("Franklin", (20, 1, -20), rl.GREEN),
            Player("Trevor", (-20, 1, 20), rl.BLUE),
        ]
        self.current_index = 0
        self.characters[0].is_active = True
        
        # Spawn vehicles near each character
        self.vehicles = [
            Vehicle((5, 0.75, 0), rl.ORANGE),
            Vehicle((25, 0.75, -20), rl.PURPLE),
            Vehicle((-15, 0.75, 20), rl.BROWN),
        ]
        
    def switch_to(self, index):
        """Switch to character at given index (0-2)."""
        active = self.get_active()
        # Don't switch if in vehicle
        if active.in_vehicle:
            return
            
        if 0 <= index < len(self.characters):
            self.characters[self.current_index].is_active = False
            self.current_index = index
            self.characters[self.current_index].is_active = True
            
    def get_active(self):
        return self.characters[self.current_index]
    
    def find_nearby_vehicle(self, player):
        """Find a vehicle close enough to enter."""
        for vehicle in self.vehicles:
            if vehicle.is_occupied:
                continue
            dx = vehicle.position.x - player.position.x
            dz = vehicle.position.z - player.position.z
            distance = math.sqrt(dx*dx + dz*dz)
            if distance < 4.0:
                return vehicle
        return None
    
    def handle_input(self):
        """Handle character switch and vehicle interaction."""
        active = self.get_active()
        
        # Vehicle enter/exit (E key)
        if rl.is_key_pressed(rl.KEY_E):
            if active.in_vehicle:
                active.current_vehicle.exit()
            else:
                nearby = self.find_nearby_vehicle(active)
                if nearby:
                    nearby.enter(active)
        
        # Character switching (only when on foot)
        if not active.in_vehicle:
            if rl.is_key_pressed(rl.KEY_ONE):
                self.switch_to(0)
            elif rl.is_key_pressed(rl.KEY_TWO):
                self.switch_to(1)
            elif rl.is_key_pressed(rl.KEY_THREE):
                self.switch_to(2)
    
    def update(self, dt):
        self.handle_input()
        for character in self.characters:
            character.update(dt)
        for vehicle in self.vehicles:
            vehicle.update(dt)
            
    def draw(self):
        for vehicle in self.vehicles:
            vehicle.draw()
        for character in self.characters:
            character.draw()
