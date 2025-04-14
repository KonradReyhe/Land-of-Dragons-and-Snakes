"""
Blind Marketplace Scene
A ruined city square where people live in spiritual blindness.
"""

import pygame
from typing import Dict, Optional, List, Tuple
from pathlib import Path

from ..core.scene_manager import Scene
from ..core.resource_manager import ResourceManager
from ..core.input_manager import InputManager
from .base_scene import BaseScene

class BlindMarketplace(BaseScene):
    """Scene representing a ruined marketplace where people live in spiritual blindness."""
    
    def __init__(self, game_state):
        """Initialize the blind marketplace scene.
        
        Args:
            game_state: The game state manager instance.
        """
        super().__init__(game_state)
        self.scene_name = "blind_marketplace"
        self.resource_manager = ResourceManager()
        self.input_manager = InputManager()
        
        # Scene state
        self.current_dialogue: Optional[str] = None
        self.text_messages: List[str] = []
        self.text_timer: float = 0.0
        self.text_duration: float = 5.0  # seconds
        
        # Colors with atmospheric effects
        self.colors = {
            'text': (255, 255, 255),
            'text_shadow': (0, 0, 0),
            'panel_background': (50, 50, 50, 200),
            'panel_border': (100, 100, 100, 255),
            'panel_border_highlight': (150, 150, 150, 255),
            'button_normal': (80, 80, 80),
            'button_hover': (100, 100, 100),
            'button_text': (255, 255, 255),
            'inventory_background': (30, 30, 30, 200),
            'inventory_border': (80, 80, 80, 255),
            'inventory_highlight': (120, 120, 120, 255),
            'highlight': (255, 223, 0, 50),  # Golden glow
            'glow': (255, 223, 0, 50),  # Golden glow
            'scripture': (184, 134, 11),  # Ancient text color
            'light_ray': (255, 255, 220, 30),  # Soft light color
            'water': (200, 220, 255, 128),  # Water droplet color
            'haze': (100, 100, 100, 50)  # Gray haze color
        }
        
        # Load and scale background
        self.background = self.resource_manager.load_image("backgrounds/background_markedplace.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        # Load and scale character
        self.character_image = self.resource_manager.load_image("characters/main_character.png")
        self.character_scale = 0.8
        char_size = (int(self.character_image.get_width() * self.character_scale),
                    int(self.character_image.get_height() * self.character_scale))
        self.character_image = pygame.transform.scale(self.character_image, char_size)
        
        # Load NPC portraits
        self.npc_images = {
            'justifier': self.resource_manager.load_image("characters/Justifier Portrait.png"),
            'mother': self.resource_manager.load_image("characters/Mother Portrait.png"),
            'performer': self.resource_manager.load_image("characters/Performer Portrait.png"),
            'mason': self.resource_manager.load_image("characters/Mason Portrait.png")
        }
        
        # Scale NPC images
        for key in self.npc_images:
            self.npc_images[key] = pygame.transform.scale(self.npc_images[key], (200, 300))
            
        # Load dragon images - only use Serpent.png for all dragons temporarily
        serpent_img = self.resource_manager.load_image("characters/Serpent.png")
        serpent_img = pygame.transform.scale(serpent_img, (100, 100))
        self.dragon_images = {
            'pride': serpent_img,
            'idolatry': serpent_img,
            'vanity': serpent_img,
            'despair': serpent_img
        }
            
        # NPC positions and states
        self.npcs = {
            'justifier': {
                'position': (200, 400),
                'rect': pygame.Rect(200, 400, 200, 300),
                'dragon': 'pride',
                'dialogue': [
                    "I am the keeper of truth in this marketplace.",
                    "My judgments are always just and righteous.",
                    "I see clearly what others cannot."
                ]
            },
            'mother': {
                'position': (400, 400),
                'rect': pygame.Rect(400, 400, 200, 300),
                'dragon': 'idolatry',
                'dialogue': [
                    "My child is my everything.",
                    "I must protect them from all harm.",
                    "I know what's best for them."
                ]
            },
            'performer': {
                'position': (600, 400),
                'rect': pygame.Rect(600, 400, 200, 300),
                'dragon': 'vanity',
                'dialogue': [
                    "Watch me, admire me!",
                    "I am the star of this marketplace.",
                    "My beauty is unmatched."
                ]
            },
            'mason': {
                'position': (800, 400),
                'rect': pygame.Rect(800, 400, 200, 300),
                'dragon': 'despair',
                'dialogue': [
                    "There's nothing left to build.",
                    "The towers are broken beyond repair.",
                    "The stones are silent now."
                ]
            }
        }
        
        # Character state
        self.character_min_x = 100
        self.character_max_x = 1100
        self.character_y = 400  # Character higher up
        self.character_pos = [640, self.character_y]
        self.character_speed = 300  # Pixels per second
        self.character_target = None  # Target position for mouse movement
        self.character_direction = 1  # 1 for right, -1 for left
        self.character_visible = True
        self.character_moving = False  # New flag to track movement state
        self.moving_left = False
        self.moving_right = False
        
        # Inventory system
        self.inventory_rect = pygame.Rect(10, 10, 250, 300)
        self.inventory_frame = pygame.Surface((270, 320), pygame.SRCALPHA)
        
        # Create gradient background for inventory
        for i in range(320):
            alpha = 128 + (i / 320) * 64
            pygame.draw.line(self.inventory_frame, (20, 20, 30, alpha), (0, i), (270, i))
        
        # Draw main panel
        pygame.draw.rect(self.inventory_frame, (30, 30, 40, 200), (10, 10, 250, 300))
        
        # Draw golden border
        pygame.draw.rect(self.inventory_frame, (218, 165, 32, 255), (10, 10, 250, 300), 2)
        
        # Draw corner decorations
        for x, y in [(10, 10), (250, 10), (10, 300), (250, 300)]:
            pygame.draw.circle(self.inventory_frame, (218, 165, 32, 255), (x, y), 5)
            pygame.draw.circle(self.inventory_frame, (255, 215, 0, 128), (x, y), 3)
            
        # Create slot frame template
        self.slot_frame = pygame.Surface((60, 60), pygame.SRCALPHA)
        # Gradient background for slot
        for i in range(60):
            alpha = 96 + (i / 60) * 32
            pygame.draw.line(self.slot_frame, (25, 25, 35, alpha), (0, i), (60, i))
        # Draw slot border
        pygame.draw.rect(self.slot_frame, (218, 165, 32, 200), (0, 0, 60, 60), 2)
        # Add inner highlight
        pygame.draw.rect(self.slot_frame, (255, 255, 255, 30), (2, 2, 56, 56), 1)
        # Add corner dots
        for x, y in [(2, 2), (57, 2), (2, 57), (57, 57)]:
            pygame.draw.circle(self.slot_frame, (218, 165, 32, 255), (x, y), 2)

        # Initialize inventory slots
        self.inventory_slots = []
        slot_size = 60
        slot_padding = 10
        slots_per_row = 3
        for i in range(5):  # 5 slots for items
            row = i // slots_per_row
            col = i % slots_per_row
            x = self.inventory_rect.x + col * (slot_size + slot_padding) + slot_padding
            y = self.inventory_rect.y + row * (slot_size + slot_padding) + slot_padding
            self.inventory_slots.append({
                'rect': pygame.Rect(x, y, slot_size, slot_size),
                'item': None,
                'highlighted': False
            })

        # Initialize drag state
        self.dragged_item = None
        self.drag_offset = (0, 0)
        
        # Load ambient sound
        sound_path = Path("assets/sounds/scene_marketplace_ambient.ogg")
        if sound_path.exists():
            self.ambient_sound = pygame.mixer.Sound(str(sound_path))
            self.ambient_sound.play(-1)  # Loop indefinitely
        else:
            self.ambient_sound = None
            
        # Welcome message
        self.welcome_messages = [
            "You enter a marketplace shrouded in gray mist...",
            "The air feels heavy with unspoken burdens.",
            "Four figures stand among the ruins, each bearing an invisible weight.",
            "Use arrow keys to move. Click on people to interact."
        ]
        self.current_welcome_index = 0
        self.show_welcome_message = True
        self.message_delay = 3.0  # seconds between messages
        self.message_timer = 0.0
        
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events.
        
        Args:
            event: The pygame event to handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.show_welcome_message:
                    # Skip to next welcome message on click
                    self._advance_welcome_message()
                else:
                    # Set character target position on click
                    self.character_target = list(event.pos)
                    # Update character direction based on target
                    if self.character_target[0] < self.character_pos[0]:
                        self.character_direction = -1
                    else:
                        self.character_direction = 1
                    self.character_moving = True
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
                self.character_direction = -1
                self.character_target = None  # Cancel mouse movement
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
                self.character_direction = 1
                self.character_target = None  # Cancel mouse movement
            elif event.key == pygame.K_SPACE:
                if self.show_welcome_message:
                    self._advance_welcome_message()
                    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
                
    def _handle_click(self, pos: tuple[int, int]) -> None:
        """Handle mouse click events.
        
        Args:
            pos: Mouse position (x, y)
        """
        # Check if click is on an NPC
        for npc_id, npc_data in self.npcs.items():
            if npc_data['rect'].collidepoint(pos):
                self._handle_npc_click(npc_id)
                return
                
    def _handle_npc_click(self, npc_id: str) -> None:
        """Handle clicking on an NPC.
        
        Args:
            npc_id: ID of the clicked NPC
        """
        if npc_id in self.npcs:
            npc = self.npcs[npc_id]
            # Show random dialogue from the NPC
            import random
            dialogue = random.choice(npc['dialogue'])
            self.add_text(f"{npc_id.title()}: {dialogue}")
            
    def _advance_welcome_message(self):
        """Advance to the next welcome message or end the welcome sequence."""
        self.current_welcome_index += 1
        if self.current_welcome_index >= len(self.welcome_messages):
            self.show_welcome_message = False
        self.message_timer = 0.0
                
    def update(self, dt: float) -> None:
        """Update scene state.
        
        Args:
            dt: Time elapsed since last update in seconds.
        """
        # Handle welcome message timing
        if self.show_welcome_message:
            self.message_timer += dt
            if self.message_timer >= self.message_delay:
                self._advance_welcome_message()
            return  # Don't process other updates during welcome sequence
            
        # Update character movement
        if self.character_target:
            # Calculate distance to target
            dx = self.character_target[0] - self.character_pos[0]
            dy = self.character_target[1] - self.character_pos[1]
            distance = (dx**2 + dy**2)**0.5
            
            # If we're close enough to the target, stop moving
            if distance < 5:
                self.character_pos[0] = self.character_target[0]
                self.character_pos[1] = self.character_target[1]
                self.character_target = None
                self.character_moving = False
            else:
                # Move towards target
                speed = self.character_speed * dt
                if distance > 0:
                    self.character_pos[0] += (dx / distance) * speed
                    self.character_pos[1] += (dy / distance) * speed
                
                # Update character direction based on movement
                if dx < 0:
                    self.character_direction = -1
                else:
                    self.character_direction = 1
                    
        elif self.moving_left:
            new_x = self.character_pos[0] - self.character_speed * dt
            self.character_pos[0] = max(self.character_min_x, new_x)
        elif self.moving_right:
            new_x = self.character_pos[0] + self.character_speed * dt
            self.character_pos[0] = min(self.character_max_x, new_x)
            
        # Update text messages
        if self.text_messages:
            self.text_timer += dt
            if self.text_timer >= self.text_duration:
                self.text_messages.pop(0)
                self.text_timer = 0.0
                
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene.
        
        Args:
            screen: The pygame surface to render to.
        """
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw character
        if self.character_visible:
            char_image = pygame.transform.flip(self.character_image, self.character_direction < 0, False)
            screen.blit(char_image, (self.character_pos[0] - char_image.get_width() // 2,
                                   self.character_pos[1] - char_image.get_height() // 2))
            
        # Draw NPCs and their dragons
        for npc_id, npc_data in self.npcs.items():
            screen.blit(self.npc_images[npc_id], npc_data['position'])
            if 'dragon' in npc_data and npc_data['dragon'] in self.dragon_images:
                dragon_pos = (npc_data['position'][0] + 50, npc_data['position'][1] - 50)
                screen.blit(self.dragon_images[npc_data['dragon']], dragon_pos)
            
        # Draw inventory
        screen.blit(self.inventory_frame, (self.inventory_rect.x - 10, self.inventory_rect.y - 10))
        
        # Draw welcome message or regular text messages
        if self.show_welcome_message and self.current_welcome_index < len(self.welcome_messages):
            self._draw_centered_text(screen, self.welcome_messages[self.current_welcome_index])
        elif self.text_messages:
            self._draw_text_message(screen, self.text_messages[0])
            
        # Draw haze overlay
        haze = pygame.Surface((1280, 720), pygame.SRCALPHA)
        haze.fill(self.colors['haze'])
        screen.blit(haze, (0, 0))
        
    def _draw_centered_text(self, screen: pygame.Surface, text: str) -> None:
        """Draw centered text with a semi-transparent background."""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, self.colors['text'])
        text_shadow = font.render(text, True, self.colors['text_shadow'])
        
        # Create background panel
        panel_width = text_surface.get_width() + 40
        panel_height = text_surface.get_height() + 20
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 180))  # Darker, more atmospheric background
        pygame.draw.rect(panel, self.colors['panel_border'], (0, 0, panel_width, panel_height), 2)
        
        # Position at center of screen
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = (screen.get_height() - panel_height) // 2
        
        # Draw panel and text
        screen.blit(panel, (panel_x, panel_y))
        screen.blit(text_shadow, (panel_x + 22, panel_y + 12))  # Offset shadow
        screen.blit(text_surface, (panel_x + 20, panel_y + 10))
        
    def _draw_text_message(self, screen: pygame.Surface, text: str) -> None:
        """Draw regular text message at the bottom of the screen."""
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, self.colors['text'])
        text_shadow = font.render(text, True, self.colors['text_shadow'])
        
        panel_width = text_surface.get_width() + 40
        panel_height = text_surface.get_height() + 20
        panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel.fill(self.colors['panel_background'])
        pygame.draw.rect(panel, self.colors['panel_border'], (0, 0, panel_width, panel_height), 2)
        
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = screen.get_height() - panel_height - 20
        
        screen.blit(panel, (panel_x, panel_y))
        screen.blit(text_shadow, (panel_x + 22, panel_y + 12))
        screen.blit(text_surface, (panel_x + 20, panel_y + 10))
        
    def cleanup(self) -> None:
        """Clean up scene resources."""
        if hasattr(self, 'ambient_sound') and self.ambient_sound:
            self.ambient_sound.stop()
        super().cleanup() 