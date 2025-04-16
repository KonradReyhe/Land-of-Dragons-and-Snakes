import pygame
from scenes.base_scene import BaseScene
from engine.resource_loader import ResourceLoader

class StartingScene(BaseScene):
    def __init__(self, ui_manager):
        super().__init__()
        self.title = "Land of Dragons and Snakes"
        self.font = pygame.font.Font(None, 48)
        
        # Get screen dimensions from UI manager
        self.screen_width = ui_manager.screen_width
        self.screen_height = ui_manager.screen_height
        
        # Adjust button position for new window size
        self.start_button = pygame.Rect(
            (self.screen_width - 200) // 2,  # Center horizontally
            (self.screen_height - 50) // 2,  # Center vertically
            200, 50
        )
        
        # Load background
        self.resource_loader = ResourceLoader()
        self.background = self.resource_loader.load_background("start_screen")
        
        # Scale background to window size
        if self.background:
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        
        # Hide all UI elements
        self.ui_manager = ui_manager
        self.ui_manager.set_ui_visibility(show_inventory=False, show_textbox=False, show_options=False)
        
    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return "scene1"  # Change to Scene 1
        return None

    def draw(self, screen):
        # Draw background if available
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((0, 0, 0))  # Fallback black background
        
        # Draw title
        title_text = self.font.render(self.title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title_text, title_rect)
        
        # Draw start button
        pygame.draw.rect(screen, (100, 100, 100), self.start_button)
        pygame.draw.rect(screen, (255, 255, 255), self.start_button, 2)
        
        start_text = self.font.render("Start Game", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect) 