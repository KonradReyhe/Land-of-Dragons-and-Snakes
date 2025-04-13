"""
Base Scene Class
Defines common functionality for all game scenes.
"""

from typing import Dict, List, Optional, Tuple
import pygame
from ..core.scene_manager import Scene
from ..core.resource_manager import ResourceManager
from ..core.input_manager import InputManager

class BaseScene(Scene):
    def __init__(self, scene_name: str):
        """Initialize the base scene."""
        super().__init__()
        self.scene_name = scene_name
        self.resource_manager = ResourceManager()
        self.input_manager = InputManager()
        
        # Scene state
        self.background: Optional[pygame.Surface] = None
        self.foreground: Optional[pygame.Surface] = None
        self.interactive_areas: Dict[str, pygame.Rect] = {}
        self.collectible_items: Dict[str, bool] = {}  # Track collected items
        self.puzzle_state: Dict[str, bool] = {}  # Track puzzle progress
        
        # Visual effects
        self.fade_surface = pygame.Surface((1920, 1080))
        self.fade_alpha = 0
        self.fade_speed = 5
        self.is_fading = False
        
        # Audio
        self.ambient_sound: Optional[pygame.mixer.Sound] = None
        self.voice_over: Optional[pygame.mixer.Sound] = None
        
    def load_resources(self) -> None:
        """Load scene-specific resources."""
        # Load background
        self.background = self.resource_manager.load_image(
            f"scene_{self.scene_name}_base.png"
        )
        
        # Load foreground if exists
        try:
            self.foreground = self.resource_manager.load_image(
                f"scene_{self.scene_name}_foreground.png"
            )
        except pygame.error:
            self.foreground = None
            
        # Load ambient sound if exists
        try:
            self.ambient_sound = self.resource_manager.load_sound(
                f"scene_{self.scene_name}_ambient.ogg"
            )
            self.ambient_sound.play(-1)  # Loop ambient sound
        except pygame.error:
            self.ambient_sound = None
            
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events."""
        self.input_manager.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_click(event.pos)
                
    def _handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle click interactions."""
        # Check interactive areas
        for name, rect in self.interactive_areas.items():
            if rect.collidepoint(pos):
                self._on_interaction(name)
                break
                
    def _on_interaction(self, area_name: str) -> None:
        """Handle interaction with a specific area."""
        pass  # To be implemented by child classes
        
    def update(self, dt: float) -> None:
        """Update scene state."""
        # Handle fade effects
        if self.is_fading:
            self.fade_alpha += self.fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.is_fading = False
            self.fade_surface.set_alpha(self.fade_alpha)
            
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene."""
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
            
        # Draw interactive elements
        self._render_interactive_elements(screen)
        
        # Draw foreground
        if self.foreground:
            screen.blit(self.foreground, (0, 0))
            
        # Draw fade effect if active
        if self.fade_alpha > 0:
            screen.blit(self.fade_surface, (0, 0))
            
    def _render_interactive_elements(self, screen: pygame.Surface) -> None:
        """Render interactive elements of the scene."""
        pass  # To be implemented by child classes
        
    def start_fade(self, fade_in: bool = True) -> None:
        """Start a fade effect."""
        self.is_fading = True
        self.fade_alpha = 0 if fade_in else 255
        self.fade_speed = 5 if fade_in else -5
        self.fade_surface.fill((0, 0, 0))
        
    def cleanup(self) -> None:
        """Clean up scene resources."""
        if self.ambient_sound:
            self.ambient_sound.stop()
        if self.voice_over:
            self.voice_over.stop() 