import pyray as rl
import os
from src.core.camera import CameraController
from src.core.save_system import SaveSystem
from src.entities.character_manager import CharacterManager
from src.entities.vehicle import Vehicle
from src.world.scene import Scene
from src.ui.console import CheatConsole
from src.ui.pause_menu import PauseMenu

class GameCommands:
    """Handler for cheat console commands."""
    def __init__(self, character_manager):
        self.character_manager = character_manager
        self.god_mode = False
        
    def teleport_player(self, x, y, z):
        player = self.character_manager.get_active()
        player.position.x = x
        player.position.y = y
        player.position.z = z
        
    def spawn_vehicle(self):
        player = self.character_manager.get_active()
        new_vehicle = Vehicle(
            (player.position.x + 3, 0.75, player.position.z),
            rl.GOLD
        )
        self.character_manager.vehicles.append(new_vehicle)
        
    def toggle_god_mode(self):
        self.god_mode = not self.god_mode
        return self.god_mode

def main():
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    
    rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Phoenix - Pre-Alpha")
    rl.set_exit_key(0)  # Disable default ESC exit to allow pause menu
    rl.set_target_fps(60)
    
    # Initialize systems
    camera_controller = CameraController()
    character_manager = CharacterManager()
    scene = Scene()
    
    saves_dir = os.path.join(os.path.dirname(__file__), 'saves')
    save_system = SaveSystem(saves_dir)
    
    game_commands = GameCommands(character_manager)
    console = CheatConsole(game_commands)
    
    def save_game(slot):
        game_state = {
            'player_positions': [
                [c.position.x, c.position.y, c.position.z]
                for c in character_manager.characters
            ],
            'current_character': character_manager.current_index,
            'unlocked_cheats': [],
            'world_state': {}
        }
        save_system.save_game(slot, game_state)
        
    def load_game(slot):
        data = save_system.load_game(slot)
        if data:
            for i, pos in enumerate(data['player_positions']):
                character_manager.characters[i].position.x = pos[0]
                character_manager.characters[i].position.y = pos[1]
                character_manager.characters[i].position.z = pos[2]
            character_manager.switch_to(data['current_character'])
    
    pause_menu = PauseMenu(save_system, save_game, load_game)
    
    while not rl.window_should_close():
        dt = rl.get_frame_time()
        
        # Toggle console (grave/tilde key)
        if rl.is_key_pressed(rl.KEY_GRAVE):
            console.toggle()
            
        # Toggle pause (ESC)
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            pause_menu.toggle()
            
        # Update based on state
        if pause_menu.is_open:
            result = pause_menu.update()
            if result == 'quit':
                break
            # Apply render distance
            scene.lod_far = pause_menu.render_distance
        elif console.is_open:
            console.update(dt)
        else:
            # Normal game update
            character_manager.update(dt)
            active_player = character_manager.get_active()
            camera_controller.set_driving_mode(active_player.in_vehicle)
            camera_controller.update(active_player.position)
            
            # Check metro
            nearby_station = None
            if scene.metro and not active_player.in_vehicle:
                nearby_station = scene.metro.find_nearby_station(active_player.position)
                if nearby_station and rl.is_key_pressed(rl.KEY_M):
                    destinations = scene.metro.get_destinations(nearby_station)
                    if destinations:
                        scene.metro.teleport_to(active_player, destinations[0])
        
        scene.update(dt, camera_controller.camera.position)
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.SKYBLUE)
        
        rl.begin_mode_3d(camera_controller.camera)
        scene.draw()
        character_manager.draw()
        rl.end_mode_3d()
        
        # UI
        active_player = character_manager.get_active()
        if not console.is_open and not pause_menu.is_open:
            rl.draw_text("Phoenix | ESC=Menu | `=Console", 10, 10, 18, rl.DARKGRAY)
            
            if active_player.in_vehicle:
                rl.draw_text(f"{active_player.name} DRIVING | WASD | E=exit", 10, 35, 18, rl.MAROON)
            else:
                rl.draw_text(f"{active_player.name} | WASD | E=vehicle | 1/2/3=switch", 10, 35, 18, rl.DARKGRAY)
                
                # Metro prompt
                if scene.metro:
                    station = scene.metro.find_nearby_station(active_player.position)
                    if station:
                        rl.draw_text(f"METRO: {station['city_name']} | M=travel", 10, 60, 20, rl.BLUE)
        
        # Draw overlays
        console.draw()
        pause_menu.draw()
        
        # Coordinate System Display (Top Right)
        if not console.is_open:
            pos = active_player.position
            coord_text = f"X: {pos.x:.1f}  Y: {pos.y:.1f}  Z: {pos.z:.1f}"
            font_size = 20
            text_width = rl.measure_text(coord_text, font_size)
            rl.draw_text(coord_text, SCREEN_WIDTH - text_width - 20, 10, font_size, rl.BLACK)
        
        rl.draw_fps(10, SCREEN_HEIGHT - 25)
        rl.end_drawing()
        
    rl.close_window()

if __name__ == "__main__":
    main()
