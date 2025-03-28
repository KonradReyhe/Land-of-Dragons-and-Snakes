import pygame
import os
from scene1 import Scene1
from start_screen import StartScreen

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
ASSETS_DIR = "assets/"

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Land of Dragons and Snakes")

# Main game loop
def main():
    # Create screens
    start_screen = StartScreen()
    scene = Scene1()
    
    # Game state
    current_screen = "start"
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if current_screen == "start":
                if start_screen.handle_event(event):
                    current_screen = "game"
            elif current_screen == "game":
                scene.handle_event(event)

        # Update current screen
        if current_screen == "game":
            scene.update()

        # Render current screen
        if current_screen == "start":
            start_screen.render(screen)
        elif current_screen == "game":
            scene.render(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Cap the framerate at 60 FPS
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main() 