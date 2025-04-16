import pygame
import os

class ResourceLoader:
    def __init__(self):
        self.assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        self.images_path = os.path.join(self.assets_path, 'images')
        self.backgrounds_path = os.path.join(self.images_path, 'backgrounds')
        
        # Cache for loaded images
        self._image_cache = {}
        
    def load_background(self, background_name):
        """Load a background image from the backgrounds directory."""
        if background_name in self._image_cache:
            return self._image_cache[background_name]
            
        file_path = os.path.join(self.backgrounds_path, f"{background_name}.png")
        try:
            image = pygame.image.load(file_path).convert()
            self._image_cache[background_name] = image
            return image
        except pygame.error as e:
            print(f"Error loading background {background_name}: {e}")
            return None 