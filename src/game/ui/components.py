"""
Shared UI Components
Contains reusable UI elements like inventory and text boxes.
"""

import pygame
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class UIStyle:
    """Style configuration for UI components."""
    font_name: str = "Arial"
    font_size: int = 24
    text_color: Tuple[int, int, int] = (255, 255, 255)
    background_color: Tuple[int, int, int] = (0, 0, 0, 128)
    border_color: Tuple[int, int, int] = (200, 200, 200)
    border_width: int = 2
    padding: int = 10

class TextBox:
    """A reusable text box component for displaying messages."""
    
    def __init__(
        self,
        rect: pygame.Rect,
        style: Optional[UIStyle] = None,
        max_lines: int = 4
    ):
        """Initialize the text box.
        
        Args:
            rect: Position and size of the text box
            style: Optional custom style configuration
            max_lines: Maximum number of lines to display
        """
        self.rect = rect
        self.style = style or UIStyle()
        self.max_lines = max_lines
        self.lines: List[str] = []
        self.font = pygame.font.SysFont(self.style.font_name, self.style.font_size)
        self.background: Optional[pygame.Surface] = None
        
    def set_background(self, image: pygame.Surface) -> None:
        """Set a custom background image for the text box.
        
        Args:
            image: The background image to use
        """
        self.background = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        
    def add_text(self, text: str) -> None:
        """Add text to the text box.
        
        Args:
            text: Text to add
        """
        words = text.split()
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.font.size(test_line)[0] <= self.rect.width - 2 * self.style.padding:
                current_line = test_line
            else:
                self.lines.append(current_line)
                current_line = word
                
        if current_line:
            self.lines.append(current_line)
            
        # Keep only the last max_lines
        if len(self.lines) > self.max_lines:
            self.lines = self.lines[-self.max_lines:]
            
    def clear(self) -> None:
        """Clear all text from the text box."""
        self.lines = []
        
    def render(self, surface: pygame.Surface) -> None:
        """Render the text box.
        
        Args:
            surface: Surface to render to
        """
        # Draw background
        if self.background:
            surface.blit(self.background, self.rect)
        else:
            background = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            background.fill(self.style.background_color)
            surface.blit(background, self.rect)
        
        # Draw border
        pygame.draw.rect(
            surface,
            self.style.border_color,
            self.rect,
            self.style.border_width
        )
        
        # Draw text
        y = self.rect.top + self.style.padding
        for line in self.lines:
            text_surface = self.font.render(line, True, self.style.text_color)
            surface.blit(
                text_surface,
                (self.rect.left + self.style.padding, y)
            )
            y += self.font.get_linesize()

class Inventory:
    """A reusable inventory component for displaying collected items."""
    
    def __init__(
        self,
        rect: pygame.Rect,
        style: Optional[UIStyle] = None,
        columns: int = 3,
        item_size: int = 64
    ):
        """Initialize the inventory.
        
        Args:
            rect: Position and size of the inventory
            style: Optional custom style configuration
            columns: Number of columns in the inventory grid
            item_size: Size of each inventory slot in pixels
        """
        self.rect = rect
        self.style = style or UIStyle()
        self.columns = columns
        self.item_size = item_size
        self.items: Dict[str, pygame.Surface] = {}
        self.font = pygame.font.SysFont(self.style.font_name, self.style.font_size)
        self.background: Optional[pygame.Surface] = None
        
    def set_background(self, image: pygame.Surface) -> None:
        """Set a custom background image for the inventory.
        
        Args:
            image: The background image to use
        """
        self.background = pygame.transform.scale(image, (self.rect.width, self.rect.height))
        
    def add_item(self, item_id: str, image_path: str) -> bool:
        """Add an item to the inventory.
        
        Args:
            item_id: Unique identifier for the item
            image_path: Path to the item's image
            
        Returns:
            bool: True if item was added successfully
        """
        try:
            image = pygame.image.load(image_path).convert_alpha()
            image = pygame.transform.scale(image, (self.item_size, self.item_size))
            self.items[item_id] = image
            return True
        except Exception as e:
            print(f"Error loading item image: {e}")
            return False
            
    def remove_item(self, item_id: str) -> bool:
        """Remove an item from the inventory.
        
        Args:
            item_id: ID of the item to remove
            
        Returns:
            bool: True if item was removed successfully
        """
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False
        
    def has_item(self, item_id: str) -> bool:
        """Check if an item is in the inventory.
        
        Args:
            item_id: ID of the item to check
            
        Returns:
            bool: True if item is in inventory
        """
        return item_id in self.items
        
    def render(self, surface: pygame.Surface) -> None:
        """Render the inventory.
        
        Args:
            surface: Surface to render to
        """
        # Draw background
        if self.background:
            surface.blit(self.background, self.rect)
        else:
            background = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            background.fill(self.style.background_color)
            surface.blit(background, self.rect)
        
        # Draw border
        pygame.draw.rect(
            surface,
            self.style.border_color,
            self.rect,
            self.style.border_width
        )
        
        # Draw items
        for i, (item_id, image) in enumerate(self.items.items()):
            row = i // self.columns
            col = i % self.columns
            
            x = self.rect.left + col * (self.item_size + self.style.padding) + self.style.padding
            y = self.rect.top + row * (self.item_size + self.style.padding) + self.style.padding
            
            # Draw item slot
            slot_rect = pygame.Rect(x, y, self.item_size, self.item_size)
            pygame.draw.rect(
                surface,
                self.style.border_color,
                slot_rect,
                1
            )
            
            # Draw item
            surface.blit(image, slot_rect)
            
            # Draw item name
            name_surface = self.font.render(item_id, True, self.style.text_color)
            name_rect = name_surface.get_rect(
                midtop=(slot_rect.centerx, slot_rect.bottom + 5)
            )
            surface.blit(name_surface, name_rect) 