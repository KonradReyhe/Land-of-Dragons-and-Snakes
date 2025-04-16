import pygame
import sys
from scenes.starting_scene import StartingScene
from scenes.scene1 import Scene1
from ui.ui_manager import UIManager

def main():
    # Initialize Pygame
    pygame.init()
    
    # Set up the display
    screen_width = 1920
    screen_height = 1080
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Land of Dragons and Snakes")
    
    # Create clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Initialize UI manager
    ui_manager = UIManager(screen_width, screen_height)
    
    # Initialize scenes
    starting_scene = StartingScene(ui_manager)
    scene1 = None  # Initialize Scene1 only when needed
    
    # Start with the starting scene
    current_scene = starting_scene
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle scene-specific events
            if current_scene == starting_scene:
                result = current_scene.handle_event(event)
                if result == "scene1":
                    # Clean up starting scene
                    starting_scene.cleanup()
                    # Initialize Scene1
                    scene1 = Scene1(screen)
                    current_scene = scene1
            else:
                current_scene.handle_event(event)
        
        # Update game state
        current_scene.update()
        
        # Clear screen at start of frame
        screen.fill((0, 0, 0))
        
        # Draw current scene
        if current_scene == starting_scene:
            current_scene.draw(screen)
        else:
            current_scene.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
    
    # Clean up
    if current_scene:
        current_scene.cleanup()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 