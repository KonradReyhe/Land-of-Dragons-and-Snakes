import pygame
from typing import Optional

class BackgroundManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.current_background: Optional[pygame.Surface] = None
        self.target_background: Optional[pygame.Surface] = None
        self.transition_alpha = 0
        self.is_transitioning = False
        self.transition_duration = 1.5  # seconds
        self.transition_progress = 0.0
        
    def set_background(self, scene: str, state: str) -> None:
        """Set new background with transition"""
        path = f"assets/images/backgrounds/bg_{scene}_{state}.png"
        try:
            new_bg = pygame.image.load(path).convert()
            
            # Calculate scaling to cover the full screen while maintaining aspect ratio
            bg_width, bg_height = new_bg.get_size()
            screen_ratio = self.screen_width / self.screen_height
            bg_ratio = bg_width / bg_height
            
            print(f"Debug: Background size: {bg_width}x{bg_height}")
            print(f"Debug: Screen size: {self.screen_width}x{self.screen_height}")
            print(f"Debug: Background ratio: {bg_ratio:.2f}")
            print(f"Debug: Screen ratio: {screen_ratio:.2f}")
            
            if screen_ratio > bg_ratio:
                # Screen is wider than background
                scale = self.screen_width / bg_width
            else:
                # Screen is taller than background
                scale = self.screen_height / bg_height
                
            print(f"Debug: Chosen scale factor: {scale:.2f}")
            
            # Scale up to cover the entire screen
            new_width = int(bg_width * scale)
            new_height = int(bg_height * scale)
            
            print(f"Debug: New background size: {new_width}x{new_height}")
            
            # Scale background
            new_bg = pygame.transform.scale(new_bg, (new_width, new_height))
            
            # Calculate position to center the background
            x = (self.screen_width - new_width) // 2
            y = (self.screen_height - new_height) // 2
            self.bg_offset = (x, y)
            
            print(f"Debug: Background offset: {self.bg_offset}")
            
            if self.current_background is None:
                # First background, no transition
                self.current_background = new_bg
            else:
                # Start transition
                self.target_background = new_bg
                self.is_transitioning = True
                self.transition_progress = 0.0
        except pygame.error as e:
            print(f"Error loading background: {e}")
            print(f"Attempted to load: {path}")
            
    def update(self, delta_time: float) -> None:
        """Update transition state"""
        if self.is_transitioning and self.target_background:
            self.transition_progress += delta_time / self.transition_duration
            if self.transition_progress >= 1.0:
                # Transition complete
                self.current_background = self.target_background
                self.target_background = None
                self.is_transitioning = False
                self.transition_progress = 0.0
                
    def draw(self, screen: pygame.Surface) -> None:
        """Draw current background with transition"""
        if self.current_background:
            # Draw current background centered
            screen.blit(self.current_background, self.bg_offset)
            
        if self.is_transitioning and self.target_background:
            # Calculate alpha based on progress
            alpha = int(255 * self.transition_progress)
            self.target_background.set_alpha(alpha)
            screen.blit(self.target_background, self.bg_offset)
            
    def get_current_state(self) -> str:
        """Get the current background state based on the file name"""
        if self.current_background is None:
            return "corrupted"
        # Extract state from the current background path
        # This is a placeholder - you'll need to track the state separately
        return "corrupted"  # Default state 