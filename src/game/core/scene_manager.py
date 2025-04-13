"""
Scene Manager
Handles scene transitions, loading, and state management.
"""

from typing import Dict, Optional, Type
from abc import ABC, abstractmethod
import pygame

class Scene(ABC):
    """Abstract base class for all game scenes."""
    
    def __init__(self, game_state):
        self.game_state = game_state
        self.next_scene = None
        self.transition_time = 0
        self.transition_duration = 1.0  # seconds
        
    @abstractmethod
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events."""
        pass
        
    @abstractmethod
    def update(self, dt: float) -> None:
        """Update scene state."""
        pass
        
    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene."""
        pass
        
    def start_transition(self, next_scene: str) -> None:
        """Start transition to another scene."""
        self.next_scene = next_scene
        self.transition_time = 0

class SceneManager:
    def __init__(self, game_state):
        """Initialize the scene manager."""
        self.game_state = game_state
        self.current_scene: Optional[Scene] = None
        self.scenes: Dict[str, Type[Scene]] = {}
        self.transition_surface = pygame.Surface((1280, 720))  # Initialize with screen size
        self.transitioning = False
        self.transition_progress = 0.0
        
    def register_scene(self, name: str, scene_class: Type[Scene]) -> None:
        """Register a new scene type."""
        self.scenes[name] = scene_class
        
    def switch_scene(self, name: str) -> bool:
        """Switch to a new scene immediately."""
        if name not in self.scenes:
            print(f"Error: Scene '{name}' not found")
            return False
            
        if not self.game_state.can_access_scene(name):
            print(f"Error: Cannot access scene '{name}'")
            return False
            
        # Create new scene instance
        new_scene = self.scenes[name](self.game_state)
        
        # Clean up old scene if exists
        if self.current_scene:
            if hasattr(self.current_scene, 'cleanup'):
                self.current_scene.cleanup()
        
        self.current_scene = new_scene
        self.game_state.current_scene = name
        return True
        
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle events for the current scene."""
        if self.current_scene:
            self.current_scene.handle_events(event)
            
    def update(self, dt: float) -> None:
        """Update the current scene and handle transitions."""
        if not self.current_scene:
            return
            
        # Handle scene transitions first
        if self.current_scene.next_scene:
            self.current_scene.transition_time += dt
            progress = min(1.0, self.current_scene.transition_time / self.current_scene.transition_duration)
            
            if progress >= 1.0:
                # Immediate switch when transition is complete
                self.switch_scene(self.current_scene.next_scene)
                return
            else:
                # Update transition effect
                self.transitioning = True
                self.transition_progress = progress
        else:
            self.transitioning = False
            self.transition_progress = 0.0
            
        # Update current scene
        self.current_scene.update(dt)
        
    def render(self, screen: pygame.Surface) -> None:
        """Render the current scene with optimized transitions."""
        if not self.current_scene:
            return
            
        # Render current scene
        self.current_scene.render(screen)
        
        # Handle scene transition
        if self.transitioning:
            # Faster fade calculation
            alpha = int(255 * self.transition_progress)
            self.transition_surface.fill((0, 0, 0))
            if alpha > 0:  # Only set alpha and blit if visible
                self.transition_surface.set_alpha(alpha)
                screen.blit(self.transition_surface, (0, 0)) 