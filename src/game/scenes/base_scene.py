"""
Base Scene
Contains shared functionality for all game scenes.
"""

import pygame
from typing import Optional, Dict
from pathlib import Path

from src.game.core.scene_manager import Scene
from src.game.ui.components import TextBox, Inventory, UIStyle

class BaseScene(Scene):
    """Base class for all game scenes with shared UI components."""
    
    def __init__(self, game_state):
        """Initialize the base scene.
        
        Args:
            game_state: The game state manager instance.
        """
        super().__init__(game_state)  # Pass game_state to parent Scene class
        
        # Scene state
        self.background: Optional[pygame.Surface] = None
        self.foreground: Optional[pygame.Surface] = None
        self.interactive_areas: Dict[str, pygame.Rect] = {}
        
        # Visual effects
        self.fade_surface = pygame.Surface((1280, 720))
        self.fade_alpha = 0
        self.fade_speed = 5
        self.is_fading = False
        
        # Audio
        self.ambient_sound: Optional[pygame.mixer.Sound] = None
        self.voice_over: Optional[pygame.mixer.Sound] = None
        
        # Load UI assets
        self._load_ui_assets()
        
        # Initialize UI components
        self._init_ui()
        
    def _load_ui_assets(self) -> None:
        """Load UI-related assets."""
        try:
            # Load inventory background
            inv_bg_path = Path("assets/items/Inventory Full UI.png")
            if inv_bg_path.exists():
                self.inventory_bg = pygame.image.load(str(inv_bg_path)).convert_alpha()
            else:
                self.inventory_bg = None
                
            # Load dialogue box
            dialogue_path = Path("assets/items/Dialogue Box.png")
            if dialogue_path.exists():
                self.dialogue_bg = pygame.image.load(str(dialogue_path)).convert_alpha()
            else:
                self.dialogue_bg = None
                
        except Exception as e:
            print(f"Error loading UI assets: {e}")
            self.inventory_bg = None
            self.dialogue_bg = None
        
    def _init_ui(self) -> None:
        """Initialize shared UI components."""
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Create UI style
        self.ui_style = UIStyle(
            font_name="Arial",
            font_size=24,
            text_color=(255, 255, 255),
            background_color=(0, 0, 0, 128),
            border_color=(200, 200, 200),
            border_width=2,
            padding=10
        )
        
        # Initialize text box with dialogue background
        text_box_rect = pygame.Rect(
            screen_width // 4,
            screen_height - 150,
            screen_width // 2,
            120
        )
        self.text_box = TextBox(text_box_rect, self.ui_style)
        if self.dialogue_bg:
            self.text_box.set_background(self.dialogue_bg)
        
        # Initialize inventory with custom background
        inventory_rect = pygame.Rect(
            screen_width - 250,
            50,
            200,
            screen_height - 100
        )
        self.inventory = Inventory(inventory_rect, self.ui_style)
        if self.inventory_bg:
            self.inventory.set_background(self.inventory_bg)
        
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
        # Update fade effect if active
        if self.is_fading:
            if self.fade_alpha < 255:
                self.fade_alpha = min(255, self.fade_alpha + self.fade_speed)
        else:
                self.is_fading = False
            
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene.
        
        Args:
            screen: The pygame surface to render to.
        """
        # Render scene-specific content
        self._render_scene(screen)
        
        # Always render UI components on top
        self.inventory.render(screen)
        self.text_box.render(screen)
        
        # Render fade effect if active
        if self.fade_alpha > 0:
            self.fade_surface.fill((0, 0, 0))
            self.fade_surface.set_alpha(self.fade_alpha)
            screen.blit(self.fade_surface, (0, 0))
            
    def _render_scene(self, screen: pygame.Surface) -> None:
        """Render scene-specific content.
        
        Args:
            screen: The pygame surface to render to.
        """
        pass
        
    def start_fade(self, fade_in: bool = True) -> None:
        """Start a fade effect.
        
        Args:
            fade_in: If True, fade from black to scene. If False, fade to black.
        """
        self.is_fading = True
        self.fade_alpha = 0 if fade_in else 255
        self.fade_speed = 5 if fade_in else -5
        
    def cleanup(self) -> None:
        """Clean up scene resources."""
        if hasattr(self, 'ambient_sound') and self.ambient_sound:
            self.ambient_sound.stop()
        if hasattr(self, 'voice_over') and self.voice_over:
            self.voice_over.stop()
            
    def add_text(self, text: str) -> None:
        """Add text to the text box.
        
        Args:
            text: Text to add.
        """
        self.text_box.add_text(text)
        
    def clear_text(self) -> None:
        """Clear the text box."""
        self.text_box.clear()
        
    def add_item(self, item_id: str, image_path: str) -> bool:
        """Add an item to the inventory.
        
        Args:
            item_id: Unique identifier for the item.
            image_path: Path to the item's image.
            
        Returns:
            bool: True if item was added successfully.
        """
        return self.inventory.add_item(item_id, image_path)
        
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the inventory.
        
        Args:
            item_id: ID of the item to remove.
            
        Returns:
            bool: True if item was removed successfully.
        """
        return self.inventory.remove_item(item_id)
        
    def has_item(self, item_id: str) -> bool:
        """Check if an item is in the inventory.
        
        Args:
            item_id: ID of the item to check.
            
        Returns:
            bool: True if item is in inventory.
        """
        return self.inventory.has_item(item_id) 