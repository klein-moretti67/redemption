import pyray as rl

class PauseMenu:
    """Pause menu with save/load and settings."""
    
    def __init__(self, save_system, on_save, on_load):
        self.is_open = False
        self.save_system = save_system
        self.on_save = on_save
        self.on_load = on_load
        
        self.selected_option = 0
        self.options = ['Resume', 'Save Game', 'Load Game', 'Settings', 'Quit']
        self.sub_menu = None  # 'save', 'load', 'settings'
        self.selected_slot = 0
        
        # Settings
        self.render_distance = 150
        
    def toggle(self):
        if self.sub_menu:
            self.sub_menu = None
        else:
            self.is_open = not self.is_open
            self.selected_option = 0
            
    def update(self):
        if not self.is_open:
            return None
            
        # Navigate options
        if rl.is_key_pressed(rl.KEY_UP):
            if self.sub_menu:
                self.selected_slot = max(0, self.selected_slot - 1)
            else:
                self.selected_option = (self.selected_option - 1) % len(self.options)
        if rl.is_key_pressed(rl.KEY_DOWN):
            if self.sub_menu:
                self.selected_slot = min(4, self.selected_slot + 1)
            else:
                self.selected_option = (self.selected_option + 1) % len(self.options)
                
        # Settings sliders
        if self.sub_menu == 'settings':
            if rl.is_key_pressed(rl.KEY_LEFT):
                self.render_distance = max(50, self.render_distance - 25)
            if rl.is_key_pressed(rl.KEY_RIGHT):
                self.render_distance = min(300, self.render_distance + 25)
                
        # Select option
        if rl.is_key_pressed(rl.KEY_ENTER):
            return self._handle_selection()
            
        return None
        
    def _handle_selection(self):
        if self.sub_menu == 'save':
            self.on_save(self.selected_slot)
            self.sub_menu = None
            return 'saved'
        elif self.sub_menu == 'load':
            self.on_load(self.selected_slot)
            self.sub_menu = None
            return 'loaded'
        elif self.sub_menu == 'settings':
            self.sub_menu = None
            return 'settings_applied'
        else:
            option = self.options[self.selected_option]
            if option == 'Resume':
                self.is_open = False
                return 'resume'
            elif option == 'Save Game':
                self.sub_menu = 'save'
            elif option == 'Load Game':
                self.sub_menu = 'load'
            elif option == 'Settings':
                self.sub_menu = 'settings'
            elif option == 'Quit':
                return 'quit'
        return None
        
    def draw(self):
        if not self.is_open:
            return
            
        sw, sh = rl.get_screen_width(), rl.get_screen_height()
        
        # Dim background
        rl.draw_rectangle(0, 0, sw, sh, rl.Color(0, 0, 0, 180))
        
        # Menu box
        box_w, box_h = 400, 300
        box_x, box_y = (sw - box_w) // 2, (sh - box_h) // 2
        rl.draw_rectangle(box_x, box_y, box_w, box_h, rl.Color(40, 40, 40, 255))
        rl.draw_rectangle_lines(box_x, box_y, box_w, box_h, rl.WHITE)
        
        rl.draw_text("PAUSED", box_x + 150, box_y + 20, 30, rl.WHITE)
        
        if self.sub_menu == 'save' or self.sub_menu == 'load':
            # Show save slots
            saves = self.save_system.list_saves()
            for i, save in enumerate(saves):
                y = box_y + 70 + i * 40
                color = rl.YELLOW if i == self.selected_slot else rl.GRAY
                if save.get('empty'):
                    text = f"Slot {i}: Empty"
                else:
                    text = f"Slot {i}: {save['timestamp'][:16]}"
                rl.draw_text(text, box_x + 30, y, 20, color)
        elif self.sub_menu == 'settings':
            rl.draw_text("SETTINGS", box_x + 140, box_y + 70, 24, rl.WHITE)
            rl.draw_text(f"Render Distance: {self.render_distance}", box_x + 30, box_y + 120, 20, rl.YELLOW)
            rl.draw_text("< LEFT / RIGHT >", box_x + 30, box_y + 150, 16, rl.GRAY)
            rl.draw_text("Press ENTER to apply", box_x + 30, box_y + 200, 18, rl.GREEN)
        else:
            # Main menu options
            for i, opt in enumerate(self.options):
                y = box_y + 70 + i * 40
                color = rl.YELLOW if i == self.selected_option else rl.GRAY
                rl.draw_text(opt, box_x + 30, y, 24, color)
