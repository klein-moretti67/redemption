import json
import os
from datetime import datetime

class SaveSystem:
    """Manages game saves with multiple slots."""
    
    def __init__(self, saves_dir):
        self.saves_dir = saves_dir
        self.max_slots = 5
        os.makedirs(saves_dir, exist_ok=True)
        
    def get_save_path(self, slot):
        return os.path.join(self.saves_dir, f"save_{slot}.json")
    
    def save_game(self, slot, game_state):
        """Save game state to slot."""
        save_data = {
            'timestamp': datetime.now().isoformat(),
            'player_positions': game_state['player_positions'],
            'current_character': game_state['current_character'],
            'unlocked_cheats': game_state.get('unlocked_cheats', []),
            'world_state': game_state.get('world_state', {})
        }
        
        with open(self.get_save_path(slot), 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    
    def load_game(self, slot):
        """Load game state from slot."""
        path = self.get_save_path(slot)
        if not os.path.exists(path):
            return None
            
        with open(path, 'r') as f:
            return json.load(f)
    
    def list_saves(self):
        """List all available saves."""
        saves = []
        for slot in range(self.max_slots):
            path = self.get_save_path(slot)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    saves.append({
                        'slot': slot,
                        'timestamp': data.get('timestamp', 'Unknown'),
                        'character': data.get('current_character', 0)
                    })
            else:
                saves.append({'slot': slot, 'empty': True})
        return saves
    
    def delete_save(self, slot):
        """Delete a save slot."""
        path = self.get_save_path(slot)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
