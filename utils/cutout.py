"""
Cutout module for Land of Dragons and Snakes.
This will handle interactive objects in the game scenes.
"""

import pygame
import os

class Cutout:
    def __init__(self, name, image_path, x, y):
        self.name = name
        self.image = None
        self.rect = None
        self.is_visible = True
        self.load_image(image_path)
        self.set_position(x, y)

    def load_image(self, image_path):
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.rect = self.image.get_rect()
        except pygame.error as e:
            print(f"Couldn't load image: {image_path}")
            print(e)
            raise

    def set_position(self, x, y):
        if self.rect:
            self.rect.x = x
            self.rect.y = y

    def is_clicked(self, pos):
        if not self.is_visible:
            return False
        return self.rect.collidepoint(pos)

    def handle_click(self):
        if self.is_visible:
            self.is_visible = False
            return True
        return False

    def render(self, screen):
        if self.is_visible and self.image:
            screen.blit(self.image, self.rect) 