#!/usr/bin/env python3
"""
Land of Dragons and Snakes - Main Game File
A spiritually symbolic point-and-click adventure game.
"""

import sys
import logging
import pygame
from pygame.locals import *
from typing import NoReturn
from pathlib import Path

from src.game.scenes.starting_screen import StartingScreen
from src.game.scenes.mirror_chamber import MirrorChamber
from src.game.scenes.blind_marketplace import BlindMarketplace
from src.game.core.scene_manager import SceneManager
from src.game.core.game_state import GameState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('game.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Game Configuration
class GameConfig:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    FPS = 60
    TITLE = "Land of Dragons and Snakes"
    ASSETS_PATH = Path("assets")
    SAVES_PATH = Path("saves")

def initialize_pygame() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize Pygame and return screen and clock objects."""
    try:
        pygame.init()
        pygame.mixer.init()
        
        screen = pygame.display.set_mode((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        pygame.display.set_caption(GameConfig.TITLE)
        
        clock = pygame.time.Clock()
        return screen, clock
    except pygame.error as e:
        logger.error(f"Failed to initialize Pygame: {e}")
        sys.exit(1)

def main() -> NoReturn:
    """Entry point of the game."""
    try:
        # Initialize game components
        screen, clock = initialize_pygame()
        game_state = GameState()
        scene_manager = SceneManager(game_state)
        
        # Register scenes
        scene_manager.register_scene("starting_screen", StartingScreen)
        scene_manager.register_scene("mirror_chamber", MirrorChamber)
        scene_manager.register_scene("blind_marketplace", BlindMarketplace)
        
        # Start with the starting screen
        if not scene_manager.switch_scene("starting_screen"):
            logger.error("Failed to load starting screen")
            sys.exit(1)
        
        # Game loop
        running = True
        while running:
            try:
                # Calculate delta time
                dt = clock.tick(GameConfig.FPS) / 1000.0
                
                # Handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    scene_manager.handle_events(event)
                    
                # Update and render
                scene_manager.update(dt)
                screen.fill((0, 0, 0))
                scene_manager.render(screen)
                pygame.display.flip()
                
            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                running = False
                
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main() 