import pyray as rl

class CheatConsole:
    """In-game cheat console with text input."""
    
    def __init__(self, game_commands):
        self.is_open = False
        self.input_text = ""
        self.max_length = 50
        self.history = []
        self.message = ""
        self.message_timer = 0
        self.game_commands = game_commands  # Reference to command handler
        
        # Available commands
        self.commands = {
            'KIG_ME_OUT': self.cmd_teleport,
            'GIVE_CAR': self.cmd_give_car,
            'GOD_MODE': self.cmd_god_mode,
            'HELP': self.cmd_help,
        }
        
    def toggle(self):
        self.is_open = not self.is_open
        self.input_text = ""
        
    def cmd_teleport(self, args):
        """Teleport: KIG_ME_OUT x y z"""
        if len(args) >= 3:
            try:
                x, y, z = float(args[0]), float(args[1]), float(args[2])
                self.game_commands.teleport_player(x, y, z)
                return f"Teleported to ({x}, {y}, {z})"
            except ValueError:
                return "Invalid coordinates"
        return "Usage: KIG_ME_OUT x y z"
    
    def cmd_give_car(self, args):
        """Spawn a car near player."""
        self.game_commands.spawn_vehicle()
        return "Vehicle spawned!"
    
    def cmd_god_mode(self, args):
        """Toggle god mode."""
        enabled = self.game_commands.toggle_god_mode()
        return f"God Mode: {'ON' if enabled else 'OFF'}"
    
    def cmd_help(self, args):
        return "Commands: KIG_ME_OUT, GIVE_CAR, GOD_MODE"
        
    def execute(self, command_str):
        """Parse and execute a command."""
        parts = command_str.strip().upper().split()
        if not parts:
            return
            
        cmd = parts[0]
        args = parts[1:]
        
        if cmd in self.commands:
            result = self.commands[cmd](args)
            self.message = result
            self.message_timer = 3.0
            self.history.append(command_str)
        else:
            self.message = f"Unknown command: {cmd}"
            self.message_timer = 2.0
            
    def update(self, dt):
        if not self.is_open:
            return
            
        # Decrease message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            
        # Handle text input
        key = rl.get_char_pressed()
        while key > 0:
            # Ignore backtick (`) which might be used to toggle console
            if key != 96 and 32 <= key <= 126 and len(self.input_text) < self.max_length:
                self.input_text += chr(key)
            key = rl.get_char_pressed()
            
        # Backspace
        if rl.is_key_pressed(rl.KEY_BACKSPACE) and len(self.input_text) > 0:
            self.input_text = self.input_text[:-1]
            
        # Enter to execute
        if rl.is_key_pressed(rl.KEY_ENTER):
            self.execute(self.input_text)
            self.input_text = ""
            
    def draw(self):
        if not self.is_open:
            return
            
        screen_width = rl.get_screen_width()
        
        # Console background
        rl.draw_rectangle(0, 0, screen_width, 80, rl.Color(0, 0, 0, 200))
        
        # Input line
        rl.draw_text("> " + self.input_text + "_", 10, 50, 20, rl.GREEN)
        
        # Message
        if self.message_timer > 0:
            rl.draw_text(self.message, 10, 20, 18, rl.YELLOW)
