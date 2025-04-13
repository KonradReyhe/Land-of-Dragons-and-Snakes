#!/usr/bin/env python3
"""
Land of Dragons and Snakes - Main Game File
A spiritually symbolic point-and-click adventure game.
"""

import sys
import pygame
from pygame.locals import *
from src.game.scenes.starting_screen import StartingScreen
from src.game.scenes.mirror_chamber import MirrorChamber
from src.game.core.scene_manager import SceneManager
from src.game.core.game_state import GameState

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 1280  # Reduced from 1920
SCREEN_HEIGHT = 720  # Reduced from 1080
FPS = 60
TITLE = "Land of Dragons and Snakes"

def main():
    """Entry point of the game."""
    # Set up display in windowed mode
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    # Create game state and scene manager
    game_state = GameState()
    scene_manager = SceneManager(game_state)
    
    # Register scenes
    scene_manager.register_scene("starting_screen", StartingScreen)
    scene_manager.register_scene("mirror_chamber", MirrorChamber)
    
    # Start with the starting screen
    scene_manager.switch_scene("starting_screen")
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        # Calculate delta time
        dt = clock.tick(FPS) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            scene_manager.handle_events(event)
            
        # Update
        scene_manager.update(dt)
        
        # Render
        screen.fill((0, 0, 0))
        scene_manager.render(screen)
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 