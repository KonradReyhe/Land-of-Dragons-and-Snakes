import pygame
from typing import Tuple, Optional

class Character:
    def __init__(self, x: int, y: int, screen_width: int, screen_height: int):
        self.position = pygame.math.Vector2(x, y)
        self.target_position = pygame.math.Vector2(x, y)
        self.speed = 3.0
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Load character sprite
        self.image = pygame.image.load("assets/images/characters/hooded_traveler.png").convert_alpha()
        
        # Scale character to appropriate size (about 1/5 of screen height)
        target_height = screen_height // 5  # Increased from 1/6 to 1/5
        scale_factor = target_height / self.image.get_height()
        self.image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale_factor),
             int(self.image.get_height() * scale_factor))
        )
        
        self.rect = self.image.get_rect(center=self.position)
        
        # Click indicator properties
        self.click_indicator = None
        self.click_indicator_timer = 0
        self.click_indicator_duration = 30  # frames to show indicator
        
        # Movement threshold to prevent vibrating
        self.movement_threshold = 2.0  # pixels
        
    def set_target(self, pos: Tuple[int, int]) -> None:
        """Set the target position for the character to move to"""
        # Always update target position, even if already moving
        self.target_position = pygame.math.Vector2(pos)
        
        # Create click indicator
        self.click_indicator = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.click_indicator, (255, 255, 255, 200), (10, 10), 10)
        pygame.draw.circle(self.click_indicator, (255, 255, 255, 100), (10, 10), 5)
        self.click_indicator_timer = self.click_indicator_duration
        
    def update(self, delta_time: float = 1/60) -> None:
        """Update character position"""
        # Update click indicator
        if self.click_indicator_timer > 0:
            self.click_indicator_timer -= 1
            if self.click_indicator_timer == 0:
                self.click_indicator = None
                
        # Calculate direction to target
        direction = self.target_position - self.position
        
        # If we're not at the target, move towards it
        if direction.length() > self.movement_threshold:
            # Normalize direction and scale by speed
            direction = direction.normalize() * self.speed * delta_time * 60  # Scale by delta_time and normalize to 60 FPS
            
            # Update position
            self.position += direction
            
            # Update rect for collision detection
            self.rect.center = self.position
        else:
            # Snap to target position when close enough
            self.position = self.target_position
            self.rect.center = self.position
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the character and click indicator"""
        # Draw click indicator if active
        if self.click_indicator and self.click_indicator_timer > 0:
            # Fade out the indicator
            alpha = int(255 * (self.click_indicator_timer / self.click_indicator_duration))
            self.click_indicator.set_alpha(alpha)
            screen.blit(self.click_indicator, 
                       (self.target_position.x - 10, self.target_position.y - 10))
            
        # Draw character
        screen.blit(self.image, self.rect) 