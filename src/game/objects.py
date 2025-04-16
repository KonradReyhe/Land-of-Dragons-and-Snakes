import pygame
from typing import Tuple, Optional
import random
import math
import time

class InteractiveObject:
    def __init__(self, name: str, position: Tuple[int, int], image_path: str):
        self.name = name
        self.position = position
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect(center=position)
        self.is_hovered = False
        self.original_image = self.image.copy()
        
    def draw(self, screen: pygame.Surface) -> None:
        if self.is_hovered:
            # Create a slightly larger version for hover effect
            hover_image = pygame.transform.scale(
                self.original_image,
                (int(self.rect.width * 1.1), int(self.rect.height * 1.1))
            )
            hover_rect = hover_image.get_rect(center=self.rect.center)
            screen.blit(hover_image, hover_rect)
            
            # Add glow effect
            glow_surface = pygame.Surface(hover_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 255, 50), 
                           glow_surface.get_rect(), border_radius=5)
            screen.blit(glow_surface, hover_rect)
        else:
            screen.blit(self.image, self.rect)
        
    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)
        
    def update_hover(self, mouse_pos: Tuple[int, int]) -> None:
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def scale(self, factor: float) -> None:
        """Scale the object by a given factor"""
        original_size = self.original_image.get_size()
        new_size = (int(original_size[0] * factor), 
                   int(original_size[1] * factor))
        self.image = pygame.transform.scale(self.original_image, new_size)
        self.rect = self.image.get_rect(center=self.position)

class FurnitureObject(InteractiveObject):
    def __init__(self, name: str, state: str, position: Tuple[int, int], image_path: str):
        super().__init__(name, position, image_path)
        self.state = state  # neutral, corrupted, cleansed/purified
        self.original_state_image = self.image.copy()
        
    def change_state(self, new_state: str, new_image_path: str) -> None:
        self.state = new_state
        self.image = pygame.image.load(new_image_path).convert_alpha()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=self.position)
        
    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.state == "cleansed" or self.state == "purified":
            # Add subtle glow effect for cleansed furniture
            glow_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 255, 200, 30), 
                           glow_surface.get_rect(), border_radius=5)
            screen.blit(glow_surface, self.rect)

class CreatureObject(InteractiveObject):
    def __init__(self, name: str, position: Tuple[int, int], image_path: str, screen_width: int = 1920, screen_height: int = 1080):
        self.name = name
        self.position = list(position)
        self.start_pos = list(position)
        print(f"\nDEBUG: === Initializing {name} ===")
        print(f"DEBUG: Loading image from: {image_path}")
        
        try:
            # Load image and convert with alpha in one step
            self.image = pygame.image.load(image_path).convert_alpha()
            print(f"DEBUG: Image loaded for {name}")
            print(f"  - Size: {self.image.get_size()}")
            print(f"  - Has alpha: {self.image.get_alpha() is not None}")
            print(f"  - Format: {self.image.get_bitsize()}-bit")
            
            # Create a copy for manipulation
            temp = self.image.copy()
            
            # Get color of top-left pixel (usually background)
            bg_color = temp.get_at((0, 0))
            print(f"DEBUG: Background color detected: {bg_color}")
            
            # Set this color as transparent
            temp.set_colorkey(bg_color, pygame.RLEACCEL)
            
            # Convert again to ensure proper alpha handling
            self.image = temp.convert_alpha()
            
            print(f"DEBUG: Transparency applied for {name}")
            print(f"  - Colorkey: {self.image.get_colorkey()}")
            print(f"  - Alpha: {self.image.get_alpha()}")
            
        except pygame.error as e:
            print(f"ERROR: Failed to load creature image: {e}")
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (255, 0, 0, 128), (25, 25), 25)
        
        self.rect = self.image.get_rect(center=position)
        self.is_hovered = False
        self.original_image = self.image.copy()
        
        # Initialize movement and visibility properties
        self.opacity = 255
        self.fade_speed = random.randint(3, 7)
        self.is_fading = False
        self.is_appearing = False
        self.visible = True
        
        # Screen bounds
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Movement properties
        self.speed = random.uniform(10, 20)
        self.movement_timer = 0
        self.movement_interval = random.randint(120, 240)
        self.movement_range = random.randint(40, 80)
        self.angle = 0
        
        # Appearance timing
        self.appearance_timer = 0
        self.appearance_duration = random.randint(90, 180)
        self.appearance_interval = random.randint(240, 720)
        
        # Movement pattern
        self.movement_pattern = random.choice(['random', 'circular', 'zigzag'])
        self.movement_radius = random.randint(30, 60)
        self.zigzag_direction = 1
        print(f"DEBUG: === Initialization complete for {name} ===\n")
        
    def update(self, delta_time: float) -> None:
        """Update creature position and state"""
        if not self.visible:
            return
            
        # Store original position for debug
        original_pos = self.position.copy()
        
        # Update movement based on pattern
        if self.movement_pattern == 'random':
            # Random movement within bounds, reduced speed
            self.position[0] += random.uniform(-1, 1) * self.speed * delta_time
            self.position[1] += random.uniform(-1, 1) * self.speed * delta_time
            
        elif self.movement_pattern == 'circular':
            # Circular movement, reduced angular velocity
            self.angle += self.speed * 0.2 * delta_time  # Reduced angular speed
            center_x = self.start_pos[0]
            center_y = self.start_pos[1]
            self.position[0] = center_x + math.cos(self.angle) * self.movement_radius
            self.position[1] = center_y + math.sin(self.angle) * self.movement_radius
            
        elif self.movement_pattern == 'zigzag':
            # Zigzag movement, reduced speed
            self.position[0] += self.speed * delta_time
            self.position[1] += self.zigzag_direction * self.speed * delta_time
            
            # Change direction at bounds
            if abs(self.position[1] - self.start_pos[1]) > self.movement_radius:
                self.zigzag_direction *= -1
                
        # Keep within screen bounds
        self.position[0] = max(0, min(self.screen_width - self.rect.width, self.position[0]))
        self.position[1] = max(0, min(self.screen_height - self.rect.height, self.position[1]))
        
        # Update rect position
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
        # Debug output for significant position changes
        if (abs(self.position[0] - original_pos[0]) > 1 or 
            abs(self.position[1] - original_pos[1]) > 1):
            print(f"DEBUG: {self.name} moved:")
            print(f"  - Pattern: {self.movement_pattern}")
            print(f"  - From: {original_pos}")
            print(f"  - To: {self.position}")
            print(f"  - Speed: {self.speed}")
            if self.movement_pattern == 'circular':
                print(f"  - Angle: {self.angle}")
                print(f"  - Radius: {self.movement_radius}")
            elif self.movement_pattern == 'zigzag':
                print(f"  - Direction: {self.zigzag_direction}")
                
        # Occasional state check
        if random.random() < 0.01:
            print(f"DEBUG: {self.name} state:")
            print(f"  - Visible: {self.visible}")
            print(f"  - Position: {self.position}")
            print(f"  - Pattern: {self.movement_pattern}")
            print(f"  - Speed: {self.speed}")
            print(f"  - Start pos: {self.start_pos}")
            print(f"  - Screen bounds: {self.screen_width}x{self.screen_height}")
            print(f"  - Image alpha: {self.image.get_alpha()}")
            print(f"  - Image colorkey: {self.image.get_colorkey()}")
            print(f"  - Opacity: {self.opacity}")
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the creature on the screen"""
        if not self.visible:
            return
            
        # Handle fading with variable speed
        if self.is_fading:
            self.opacity = max(0, self.opacity - self.fade_speed)
            print(f"DEBUG: {self.name} fading - opacity: {self.opacity}")
            if self.opacity <= 0:
                print(f"DEBUG: {self.name} finished fading out")
                self.visible = False
                self.is_fading = False
                self.fade_speed = random.randint(3, 7)
                
        elif self.is_appearing:
            self.opacity = min(255, self.opacity + self.fade_speed)
            print(f"DEBUG: {self.name} appearing - opacity: {self.opacity}")
            if self.opacity >= 255:
                print(f"DEBUG: {self.name} finished appearing")
                self.is_appearing = False
                
        # Create a copy of the image for opacity
        if self.opacity < 255:
            temp = self.image.copy()
            temp.fill((255, 255, 255, self.opacity), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(temp, self.rect)
        else:
            screen.blit(self.image, self.rect)
            
        if self.is_hovered:
            # Draw hover effect
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
            
        # Debug: Draw position indicator
        pygame.draw.circle(screen, (255, 0, 0), (int(self.position[0]), int(self.position[1])), 3)
            
    def fade_out(self) -> None:
        """Start fading out the creature"""
        print(f"DEBUG: {self.name} starting fade out from opacity {self.opacity}")
        self.is_fading = True
        
    def appear(self) -> None:
        """Make the creature appear"""
        print(f"DEBUG: {self.name} starting to appear at opacity {self.opacity}")
        self.visible = True
        self.is_appearing = True

    def set_movement_pattern(self, pattern: str) -> None:
        """Set the movement pattern for the creature"""
        valid_patterns = ['random', 'circular', 'zigzag']
        if pattern not in valid_patterns:
            print(f"ERROR: Invalid movement pattern '{pattern}'. Using 'random'")
            pattern = 'random'
            
        print(f"DEBUG: {self.name} changing movement pattern to {pattern}")
        self.movement_pattern = pattern
        
        # Reset movement properties
        self.start_pos = self.position.copy()
        self.angle = 0
        self.zigzag_direction = 1
        self.movement_radius = random.randint(30, 60)
        print(f"  - Start pos: {self.start_pos}")
        print(f"  - Radius: {self.movement_radius}")
        
    def teleport(self, x: float, y: float) -> None:
        """Instantly move the creature to a new position"""
        print(f"DEBUG: {self.name} teleporting from {self.position} to ({x}, {y})")
        self.position = [x, y]
        self.start_pos = self.position.copy()
        self.rect.x = x
        self.rect.y = y

class ItemObject(InteractiveObject):
    def __init__(self, name: str, position: Tuple[int, int], image_path: str, visible: bool = True):
        super().__init__(name, position, image_path)
        self.collected = False
        self.rotation = 0  # For items that should be slightly rotated
        self.visible = visible
        
    def draw(self, screen: pygame.Surface) -> None:
        if not self.collected and self.visible:
            if self.rotation != 0:
                # Rotate the image if needed
                rotated_image = pygame.transform.rotate(self.image, self.rotation)
                rotated_rect = rotated_image.get_rect(center=self.rect.center)
                screen.blit(rotated_image, rotated_rect)
            else:
                super().draw(screen)
        
    def collect(self) -> None:
        self.collected = True 