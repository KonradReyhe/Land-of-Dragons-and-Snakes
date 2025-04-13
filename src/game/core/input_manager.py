"""
Input Manager
Handles user input and interactions.
"""

from typing import Dict, Callable, Optional
import pygame

class InputManager:
    def __init__(self):
        """Initialize the input manager."""
        self.key_bindings: Dict[int, Callable] = {}
        self.mouse_bindings: Dict[int, Callable] = {}
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.mouse_released = False
        self.hotspots: Dict[str, pygame.Rect] = {}
        self.active_hotspot: Optional[str] = None
        
    def bind_key(self, key: int, callback: Callable) -> None:
        """Bind a key to a callback function."""
        self.key_bindings[key] = callback
        
    def bind_mouse_button(self, button: int, callback: Callable) -> None:
        """Bind a mouse button to a callback function."""
        self.mouse_bindings[button] = callback
        
    def add_hotspot(self, name: str, rect: pygame.Rect) -> None:
        """Add an interactive hotspot."""
        self.hotspots[name] = rect
        
    def remove_hotspot(self, name: str) -> None:
        """Remove an interactive hotspot."""
        if name in self.hotspots:
            del self.hotspots[name]
            
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_bindings:
                self.key_bindings[event.key]()
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_clicked = True
            if event.button in self.mouse_bindings:
                self.mouse_bindings[event.button]()
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_released = True
            
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            self._update_active_hotspot()
            
    def _update_active_hotspot(self) -> None:
        """Update the currently active hotspot based on mouse position."""
        self.active_hotspot = None
        for name, rect in self.hotspots.items():
            if rect.collidepoint(self.mouse_pos):
                self.active_hotspot = name
                break
                
    def is_hotspot_active(self, name: str) -> bool:
        """Check if a hotspot is currently active."""
        return self.active_hotspot == name
        
    def get_active_hotspot(self) -> Optional[str]:
        """Get the name of the currently active hotspot."""
        return self.active_hotspot
        
    def reset_mouse_state(self) -> None:
        """Reset mouse state flags."""
        self.mouse_clicked = False
        self.mouse_released = False 