class GameState:
    def __init__(self):
        self.inventory = []
        self.current_text = ""
        self.variables = {}  # For game progress tracking
        self.current_scene = "start"  # Default starting scene

    def add_to_inventory(self, item):
        if item not in self.inventory:
            self.inventory.append(item)

    def remove_from_inventory(self, item):
        if item in self.inventory:
            self.inventory.remove(item)

    def set_text(self, text):
        self.current_text = text

    def get_text(self):
        return self.current_text

    def set_variable(self, key, value):
        self.variables[key] = value

    def get_variable(self, key, default=None):
        return self.variables.get(key, default)

    def set_scene(self, scene_name):
        self.current_scene = scene_name

    def get_scene(self):
        return self.current_scene 