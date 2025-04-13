"""
Starting Screen Scene
The initial screen players see when launching the game.
"""

import pygame
import math
from typing import Optional, Tuple
from ..core.scene_manager import Scene
from ..core.resource_manager import ResourceManager
from ..core.input_manager import InputManager

class StartingScreen(Scene):
    def __init__(self, game_state):
        """Initialize the starting screen."""
        super().__init__(game_state)
        self.scene_name = "starting_screen"
        self.resource_manager = ResourceManager()
        self.input_manager = InputManager()
        
        # Set shorter transition duration for responsiveness
        self.transition_duration = 0.3  # Reduced from 1.0 second
        
        # Colors
        self.colors = {
            'bg': (15, 15, 30),  # Dark blue
            'title': (218, 165, 32),  # Gold
            'subtitle': (184, 134, 11),  # Darker gold
            'button': {
                'normal': (218, 165, 32),  # Gold
                'hover': (255, 215, 0),  # Bright gold
                'text': (255, 246, 208)  # Warm white
            },
            'glow': (255, 223, 0, 50)  # Golden glow with alpha
        }
        
        # Load background
        self.background = self.resource_manager.load_image("backgrounds/background_startingscreen.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        # Create fade surface
        self.fade_surface = pygame.Surface((1280, 720))
        self.fade_surface.fill((0, 0, 0))
        self.fade_surface.set_alpha(100)
        
        # Load fonts
        self.title_font = pygame.font.SysFont('Arial', 72)
        self.subtitle_font = pygame.font.SysFont('Arial', 36)
        self.button_font = pygame.font.SysFont('Arial', 48)
        
        # Create UI elements
        self.title_text = "Land of Dragons and Snakes"
        self.subtitle_text = "A Mystical Journey Awaits"
        self.button_text = "Start Journey"
        
        # Button dimensions and position
        button_width = 300
        button_height = 80
        self.button_rect = pygame.Rect(
            (1280 - button_width) // 2,
            500,
            button_width,
            button_height
        )
        
        # Animation state
        self.glow_alpha = 0
        self.glow_direction = 1
        self.button_hovered = False
        
    def handle_events(self, event):
        """Handle events with optimized button response."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Direct hit test without checking hover state first
            if self.button_rect.collidepoint(event.pos):
                self.start_transition("mirror_chamber")
                return  # Exit early after transition starts
                
        # Only update hover state if not transitioning
        if event.type == pygame.MOUSEMOTION and not self.next_scene:
            self.button_hovered = self.button_rect.collidepoint(event.pos)
            
    def update(self, dt):
        """Update with optimized animations."""
        # Only update effects if not transitioning
        if not self.next_scene:
            # Update glow effect with faster speed
            self.glow_alpha += self.glow_direction * 4  # Doubled speed
            if self.glow_alpha >= 100:
                self.glow_direction = -1
            elif self.glow_alpha <= 0:
                self.glow_direction = 1
                
    def _draw_decorative_line(self, surface, start_pos, end_pos, color):
        """Draw a decorative line with medieval styling."""
        pygame.draw.line(surface, color, start_pos, end_pos, 3)
        # Add decorative dots at the ends
        pygame.draw.circle(surface, color, start_pos, 5)
        pygame.draw.circle(surface, color, end_pos, 5)
        
    def render(self, screen):
        """Render with optimized effects."""
        # Draw background with fade
        screen.blit(self.background, (0, 0))
        screen.blit(self.fade_surface, (0, 0))
        
        # Skip glow effect if transitioning
        if not self.next_scene:
            # Draw title with glow effect
            if self.glow_alpha > 0:
                glow_surface = pygame.Surface((1280, 200), pygame.SRCALPHA)
                glow_color = (*self.colors['title'][:3], self.glow_alpha)
                title_glow = self.title_font.render(self.title_text, True, glow_color)
                glow_rect = title_glow.get_rect(center=(640, 200))
                glow_surface.blit(title_glow, glow_rect)
                screen.blit(glow_surface, (0, 0))
        
        # Draw main title
        title_surface = self.title_font.render(self.title_text, True, self.colors['title'])
        title_rect = title_surface.get_rect(center=(640, 200))
        screen.blit(title_surface, title_rect)
        
        # Draw decorative lines around title
        line_padding = 20
        left_line_start = (title_rect.left - line_padding, title_rect.centery)
        left_line_end = (title_rect.left - 150, title_rect.centery)
        right_line_start = (title_rect.right + line_padding, title_rect.centery)
        right_line_end = (title_rect.right + 150, title_rect.centery)
        
        self._draw_decorative_line(screen, left_line_start, left_line_end, self.colors['title'])
        self._draw_decorative_line(screen, right_line_start, right_line_end, self.colors['title'])
        
        # Draw subtitle
        subtitle_surface = self.subtitle_font.render(self.subtitle_text, True, self.colors['subtitle'])
        subtitle_rect = subtitle_surface.get_rect(center=(640, 280))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Skip hover effects if transitioning
        button_color = self.colors['button']['hover'] if (self.button_hovered and not self.next_scene) else self.colors['button']['normal']
        
        # Button background
        pygame.draw.rect(screen, button_color, self.button_rect, border_radius=10)
        pygame.draw.rect(screen, self.colors['button']['text'], self.button_rect, 3, border_radius=10)
        
        # Button text
        button_text_surface = self.button_font.render(self.button_text, True, self.colors['button']['text'])
        button_text_rect = button_text_surface.get_rect(center=self.button_rect.center)
        screen.blit(button_text_surface, button_text_rect)
        
        # Only add glow effect if hovered and not transitioning
        if self.button_hovered and not self.next_scene:
            glow_surface = pygame.Surface(self.button_rect.size, pygame.SRCALPHA)
            glow_surface.fill(self.colors['glow'])
            screen.blit(glow_surface, self.button_rect) 