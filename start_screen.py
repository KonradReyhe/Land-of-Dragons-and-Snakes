"""
Start screen module for Land of Dragons and Snakes.
"""

import pygame
import os
import math
import time

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
ASSETS_DIR = "assets/ui/"

# UI Constants
TITLE_FONT_SIZE = 92
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 80
BUTTON_FONT_SIZE = 48
SEAL_SIZE = 300

# Visual Style
TITLE_COLOR = (255, 255, 255)
BUTTON_BG_COLOR = (40, 35, 45, 180)
BUTTON_BORDER_COLOR = (120, 110, 130)
BUTTON_HOVER_COLOR = (60, 55, 65, 180)
BUTTON_TEXT_COLOR = (220, 215, 230)
SEAL_COLOR = (180, 170, 190, 160)

class StartScreen:
    def __init__(self):
        # Load and scale background
        self.background = pygame.image.load(os.path.join(ASSETS_DIR, "background.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create title with custom font (or fallback to default)
        try:
            self.font = pygame.font.Font(os.path.join(ASSETS_DIR, "medieval.ttf"), TITLE_FONT_SIZE)
        except:
            self.font = pygame.font.Font(None, TITLE_FONT_SIZE)
        
        # Create title with shadow effect
        self.title_shadow = self.font.render("Land of Dragons and Snakes", True, (0, 0, 0))
        self.title = self.font.render("Land of Dragons and Snakes", True, TITLE_COLOR)
        self.title_rect = self.title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.title_shadow_rect = self.title_shadow.get_rect(center=(self.title_rect.centerx + 4, self.title_rect.centery + 4))
        
        # Create button with custom font
        try:
            self.button_font = pygame.font.Font(os.path.join(ASSETS_DIR, "medieval.ttf"), BUTTON_FONT_SIZE)
        except:
            self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
        
        # Create semi-transparent button surface
        self.button = pygame.Surface((BUTTON_WIDTH, BUTTON_HEIGHT), pygame.SRCALPHA)
        self.button_rect = self.button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3))
        self.button_hover = False
        
        # Create seal surface
        self.seal = pygame.Surface((SEAL_SIZE, SEAL_SIZE), pygame.SRCALPHA)
        self.seal_rect = self.seal.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # Animation variables
        self.start_time = time.time()
        self.seal_rotation = 0
        self.pulse_value = 0
        
    def _draw_button(self, hover=False):
        # Clear button surface
        self.button.fill((0, 0, 0, 0))
        
        # Draw button background
        color = BUTTON_HOVER_COLOR if hover else BUTTON_BG_COLOR
        pygame.draw.rect(self.button, color, (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT))
        
        # Draw decorative borders
        pygame.draw.rect(self.button, BUTTON_BORDER_COLOR, (0, 0, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        pygame.draw.line(self.button, BUTTON_BORDER_COLOR, 
                        (10, 10), (BUTTON_WIDTH - 10, 10), 1)
        pygame.draw.line(self.button, BUTTON_BORDER_COLOR,
                        (10, BUTTON_HEIGHT - 10), (BUTTON_WIDTH - 10, BUTTON_HEIGHT - 10), 1)
        
        # Draw button text with shadow
        text = self.button_font.render("Start Game", True, (0, 0, 0))
        text_hover = self.button_font.render("Start Game", True, BUTTON_TEXT_COLOR)
        
        # Center the text
        text_rect = text.get_rect(center=(BUTTON_WIDTH // 2 + 2, BUTTON_HEIGHT // 2 + 2))
        text_hover_rect = text_hover.get_rect(center=(BUTTON_WIDTH // 2, BUTTON_HEIGHT // 2))
        
        self.button.blit(text, text_rect)
        self.button.blit(text_hover, text_hover_rect)

    def _draw_seal(self):
        # Clear seal surface
        self.seal.fill((0, 0, 0, 0))
        
        # Calculate animation values
        current_time = time.time() - self.start_time
        self.seal_rotation = current_time * 20  # Rotate 20 degrees per second
        self.pulse_value = math.sin(current_time * 2) * 0.1 + 1  # Pulse between 0.9 and 1.1 size
        
        # Draw outer circle
        radius = SEAL_SIZE // 2 - 10
        center = (SEAL_SIZE // 2, SEAL_SIZE // 2)
        
        # Draw rotating magical circles
        for i in range(3):
            angle = math.radians(self.seal_rotation + i * 120)
            pygame.draw.circle(self.seal, SEAL_COLOR,
                             (center[0] + math.cos(angle) * 20,
                              center[1] + math.sin(angle) * 20),
                             radius * self.pulse_value, 4)
        
        # Draw center circle
        pygame.draw.circle(self.seal, SEAL_COLOR, center, radius * 0.7, 3)
        
        # Draw decorative lines
        for i in range(8):
            angle = math.radians(self.seal_rotation + i * 45)
            start_pos = (center[0] + math.cos(angle) * (radius * 0.4),
                        center[1] + math.sin(angle) * (radius * 0.4))
            end_pos = (center[0] + math.cos(angle) * (radius * 0.9),
                      center[1] + math.sin(angle) * (radius * 0.9))
            pygame.draw.line(self.seal, SEAL_COLOR, start_pos, end_pos, 2)

    def render(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw animated seal
        self._draw_seal()
        screen.blit(self.seal, self.seal_rect)
        
        # Draw title with shadow
        screen.blit(self.title_shadow, self.title_shadow_rect)
        screen.blit(self.title, self.title_rect)
        
        # Draw button
        self._draw_button(self.button_hover)
        screen.blit(self.button, self.button_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            # Check button hover
            self.button_hover = self.button_rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.button_hover:  # Left click on button
                return True
        return False 