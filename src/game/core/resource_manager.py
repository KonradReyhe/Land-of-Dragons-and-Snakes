"""
Resource Manager
Handles loading and caching of game assets.
"""

import os
from typing import Dict, Optional, Tuple
import pygame

class ResourceManager:
    def __init__(self):
        """Initialize the resource manager."""
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music: Dict[str, str] = {}
        self.fonts: Dict[Tuple[str, int], pygame.font.Font] = {}
        
        # Base paths for different asset types
        self.base_paths = {
            'images': 'assets/images',
            'backgrounds': 'assets/backgrounds',
            'characters': 'assets/characters',
            'sounds': 'assets/sounds',
            'music': 'assets/music',
            'fonts': 'assets/fonts'
        }
        
        # Create asset directories if they don't exist
        for path in self.base_paths.values():
            os.makedirs(path, exist_ok=True)
            
    def load_image(self, filename: str, scale: Optional[float] = None) -> pygame.Surface:
        """Load and cache an image."""
        if filename in self.images:
            return self.images[filename]
            
        try:
            # Determine the correct base path based on the filename
            base_path = self.base_paths['images']  # default
            if filename.startswith('backgrounds/'):
                base_path = 'assets'  # backgrounds are directly in assets/backgrounds
            elif filename.startswith('characters/'):
                base_path = 'assets'  # characters are directly in assets/characters
                
            image = pygame.image.load(os.path.join(base_path, filename))
            if scale:
                new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
                image = pygame.transform.scale(image, new_size)
            self.images[filename] = image
            return image
        except pygame.error as e:
            print(f"Error loading image {filename}: {e}")
            return self._get_error_surface()
            
    def load_sound(self, filename: str) -> pygame.mixer.Sound:
        """Load and cache a sound effect."""
        if filename in self.sounds:
            return self.sounds[filename]
            
        try:
            sound = pygame.mixer.Sound(os.path.join(self.base_paths['sounds'], filename))
            self.sounds[filename] = sound
            return sound
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading sound {filename}: {e}")
            return self._get_error_sound()
            
    def load_music(self, filename: str) -> None:
        """Load a music track."""
        try:
            pygame.mixer.music.load(os.path.join(self.base_paths['music'], filename))
            self.music[filename] = os.path.join(self.base_paths['music'], filename)
        except pygame.error as e:
            print(f"Error loading music {filename}: {e}")
            
    def get_font(self, name: str, size: int) -> pygame.font.Font:
        """Get a font with specified name and size."""
        key = (name, size)
        if key in self.fonts:
            return self.fonts[key]
            
        try:
            font = pygame.font.Font(os.path.join(self.base_paths['fonts'], name), size)
            self.fonts[key] = font
            return font
        except pygame.error as e:
            print(f"Error loading font {name}: {e}")
            return pygame.font.SysFont('Arial', size)
            
    def clear_cache(self) -> None:
        """Clear all cached resources."""
        self.images.clear()
        self.sounds.clear()
        self.music.clear()
        self.fonts.clear()
        
    def _get_error_surface(self) -> pygame.Surface:
        """Create a placeholder surface for missing images."""
        surface = pygame.Surface((32, 32))
        surface.fill((255, 0, 255))  # Magenta color for error
        return surface
        
    def _get_error_sound(self) -> pygame.mixer.Sound:
        """Create a placeholder sound for missing sounds."""
        # Create a silent sound
        sound = pygame.mixer.Sound(buffer=bytes([0] * 1000))
        return sound 