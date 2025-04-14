"""
Scene Manager
Handles scene transitions, loading, and state management.
"""

import logging
from typing import Dict, Optional, Type, Protocol, runtime_checkable
import pygame
from pygame.surface import Surface

logger = logging.getLogger(__name__)

@runtime_checkable
class SceneProtocol(Protocol):
    """Protocol defining the interface for game scenes."""
    
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events."""
        ...
        
    def update(self, dt: float) -> None:
        """Update scene state."""
        ...
        
    def render(self, screen: Surface) -> None:
        """Render the scene."""
        ...
        
    def cleanup(self) -> None:
        """Clean up scene resources."""
        ...

class Scene:
    """Base class for all game scenes."""
    
    def __init__(self, game_state) -> None:
        """Initialize the scene.
        
        Args:
            game_state: The game state manager instance.
        """
        self.game_state = game_state
        self.next_scene: Optional[str] = None
        self.transition_time: float = 0.0
        self.transition_duration: float = 1.0  # seconds
        
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events.
        
        Args:
            event: The pygame event to handle.
        """
        pass
        
    def update(self, dt: float) -> None:
        """Update scene state.
        
        Args:
            dt: Time elapsed since last update in seconds.
        """
        pass
        
    def render(self, screen: Surface) -> None:
        """Render the scene.
        
        Args:
            screen: The pygame surface to render to.
        """
        pass
        
    def cleanup(self) -> None:
        """Clean up scene resources."""
        pass
        
    def start_transition(self, next_scene: str) -> None:
        """Start transition to another scene.
        
        Args:
            next_scene: Name of the scene to transition to.
        """
        self.next_scene = next_scene
        self.transition_time = 0.0

class SceneManager:
    """Manages scene transitions and state."""
    
    def __init__(self, game_state) -> None:
        """Initialize the scene manager.
        
        Args:
            game_state: The game state manager instance.
        """
        self.game_state = game_state
        self.current_scene: Optional[Scene] = None
        self.scenes: Dict[str, Type[Scene]] = {}
        self.transition_surface = Surface((1280, 720))  # Initialize with screen size
        self.transitioning: bool = False
        self.transition_progress: float = 0.0
        
    def register_scene(self, name: str, scene_class: Type[Scene]) -> None:
        """Register a new scene type.
        
        Args:
            name: Unique identifier for the scene.
            scene_class: The scene class to register.
            
        Raises:
            ValueError: If scene name is already registered.
        """
        if name in self.scenes:
            raise ValueError(f"Scene '{name}' is already registered")
        self.scenes[name] = scene_class
        logger.info(f"Registered scene: {name}")
        
    def switch_scene(self, name: str) -> bool:
        """Switch to a new scene immediately.
        
        Args:
            name: Name of the scene to switch to.
            
        Returns:
            bool: True if scene switch was successful, False otherwise.
        """
        if name not in self.scenes:
            logger.error(f"Scene '{name}' not found")
            return False
            
        if not self.game_state.can_access_scene(name):
            logger.error(f"Cannot access scene '{name}'")
            return False
            
        try:
            # Create new scene instance
            new_scene = self.scenes[name](self.game_state)
            
            # Clean up old scene if exists
            if self.current_scene:
                self.current_scene.cleanup()
            
            self.current_scene = new_scene
            self.game_state.current_scene = name
            logger.info(f"Switched to scene: {name}")
            return True
        except Exception as e:
            logger.error(f"Error switching to scene '{name}': {e}")
            return False
            
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle events for the current scene.
        
        Args:
            event: The pygame event to handle.
        """
        if self.current_scene:
            self.current_scene.handle_events(event)
            
    def update(self, dt: float) -> None:
        """Update the current scene and handle transitions.
        
        Args:
            dt: Time elapsed since last update in seconds.
        """
        if not self.current_scene:
            return
            
        try:
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
        except Exception as e:
            logger.error(f"Error updating scene: {e}")
            
    def render(self, screen: Surface) -> None:
        """Render the current scene with transition effects.
        
        Args:
            screen: The pygame surface to render to.
        """
        if not self.current_scene:
            return
            
        try:
            # Render current scene
            self.current_scene.render(screen)
            
            # Apply transition effect if transitioning
            if self.transitioning:
                alpha = int(self.transition_progress * 255)
                self.transition_surface.fill((0, 0, 0))
                self.transition_surface.set_alpha(alpha)
                screen.blit(self.transition_surface, (0, 0))
        except Exception as e:
            logger.error(f"Error rendering scene: {e}") 