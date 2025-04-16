class SceneManager:
    def __init__(self):
        self.scenes = {}
        self.current_scene = None
        self.ui_manager = None  # Will be set by the game

    def set_ui_manager(self, ui_manager):
        self.ui_manager = ui_manager

    def add_scene(self, scene_name, scene):
        self.scenes[scene_name] = scene

    def change_scene(self, scene_name):
        if scene_name in self.scenes:
            # Hide UI before changing scene
            if self.ui_manager:
                self.ui_manager.set_scene("none")  # Hide all UI elements
            
            self.current_scene = self.scenes[scene_name]
            
            # Set UI manager for the new scene
            if hasattr(self.current_scene, 'ui_manager'):
                self.current_scene.ui_manager = self.ui_manager
                
            # Set proper UI visibility for the new scene
            if self.ui_manager:
                self.ui_manager.set_scene(scene_name)
                
            return True
        return False

    def handle_event(self, event):
        if self.current_scene:
            return self.current_scene.handle_event(event)
        return None

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen) 