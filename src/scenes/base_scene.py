import pygame
from typing import List, Optional, Any

class BaseScene:
    """Base class for all game scenes.
    
    Provides core functionality for scene management, including:
    - Object management
    - Event handling
    - Drawing
    - UI management
    - Resource cleanup
    """
    
    def __init__(self):
        # Core scene properties
        self.objects: List[Any] = []  # Game objects in the scene
        self.background = None  # Scene background
        self.ui_manager = None  # UI manager for the scene
        self.is_initialized = False
        
        # Layer management (for drawing order)
        self.layers = {
            0: [],  # Background objects
            1: [],  # Main game objects
            2: [],  # Foreground objects
            3: []   # UI elements
        }
        
    def initialize(self) -> None:
        """Initialize the scene. Called once when the scene is first created."""
        if not self.is_initialized:
            self._load_resources()
            self._setup_ui()
            self.is_initialized = True
    
    def _load_resources(self) -> None:
        """Load scene-specific resources (images, sounds, etc.)"""
        pass
        
    def _setup_ui(self) -> None:
        """Setup UI elements for the scene"""
        pass
        
    def add_object(self, obj: Any, layer: int = 1) -> None:
        """Add an object to the scene in the specified layer."""
        self.objects.append(obj)
        self.layers[layer].append(obj)
        
    def remove_object(self, obj: Any) -> None:
        """Remove an object from the scene and all layers."""
        if obj in self.objects:
            self.objects.remove(obj)
            for layer in self.layers.values():
                if obj in layer:
                    layer.remove(obj)
                    
    def handle_event(self, event: pygame.event.Event) -> Optional[str]:
        """Handle pygame events. Returns next scene name if scene should change."""
        # Handle UI events first
        if self.ui_manager:
            self.ui_manager.handle_event(event)
            
        # Then handle game object events
        for obj in self.objects:
            if hasattr(obj, 'handle_event'):
                obj.handle_event(event)
                
        return None
        
    def update(self, delta_time: float = 1.0/60.0) -> None:
        """Update scene state. Default is 60 FPS timing."""
        # Update UI
        if self.ui_manager:
            self.ui_manager.update(delta_time)
            
        # Update game objects
        for obj in self.objects:
            if hasattr(obj, 'update'):
                obj.update(delta_time)
                
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the scene and all its objects."""
        # Clear screen
        screen.fill((0, 0, 0))
        
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
            
        # Draw objects by layer
        for layer_id in sorted(self.layers.keys()):
            for obj in self.layers[layer_id]:
                if hasattr(obj, 'draw'):
                    obj.draw(screen)
                    
        # Draw UI last
        if self.ui_manager:
            self.ui_manager.draw(screen)
            
    def cleanup(self) -> None:
        """Clean up resources when transitioning away from scene."""
        # Clear all objects
        self.objects.clear()
        for layer in self.layers.values():
            layer.clear()
            
        # Clear background
        self.background = None
        
        # Cleanup UI
        if self.ui_manager:
            self.ui_manager.cleanup()
            self.ui_manager = None
            
        self.is_initialized = False
        
    def get_objects_at_position(self, pos: tuple[int, int]) -> List[Any]:
        """Get all objects that contain the given position."""
        clicked_objects = []
        for obj in self.objects:
            if hasattr(obj, 'rect') and obj.rect.collidepoint(pos):
                clicked_objects.append(obj)
        return clicked_objects 