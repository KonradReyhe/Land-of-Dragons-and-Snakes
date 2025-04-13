"""
Mirror Chamber Scene
A mystical chamber where the player must collect and place mirror shards.
"""

from typing import Dict, List, Optional, Tuple
import pygame
import math
import random
from ..core.scene_manager import Scene
from ..core.resource_manager import ResourceManager
from ..core.input_manager import InputManager

class MirrorChamber(Scene):
    def __init__(self, game_state):
        """Initialize the Mirror Chamber scene."""
        super().__init__(game_state)
        self.scene_name = "mirror_chamber"
        self.resource_manager = ResourceManager()
        self.input_manager = InputManager()
        
        # Scene state
        self.all_shards_collected = False
        self.mirror_complete = False
        self.serpent_defeated = False
        self.can_exit = False
        self.door_rect = pygame.Rect(1150, 300, 80, 120)  # Door position
        
        # Visual effects state
        self.light_flicker_intensity = 0.0
        self.light_flicker_speed = 2.0
        self.water_drip_timer = 0.0
        self.water_drip_interval = 3.0  # Seconds between drips
        self.water_drips = []  # List of active water drip animations
        
        # Colors with new atmospheric effects
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
            'water': (200, 220, 255, 128)  # Water droplet color
        }
        
        # Load and scale background
        self.background = self.resource_manager.load_image("backgrounds/background_home.png")
        self.background = pygame.transform.scale(self.background, (1280, 720))
        
        # Load and scale character
        self.character_image = self.resource_manager.load_image("characters/main_character.png")
        self.character_scale = 0.8
        char_size = (int(self.character_image.get_width() * self.character_scale),
                    int(self.character_image.get_height() * self.character_scale))
        self.character_image = pygame.transform.scale(self.character_image, char_size)
        
        # Load serpent image
        self.serpent_image = self.resource_manager.load_image("characters/Serpent.png")
        self.serpent_scale = 0.5
        serpent_size = (int(self.serpent_image.get_width() * self.serpent_scale),
                       int(self.serpent_image.get_height() * self.serpent_scale))
        self.serpent_image = pygame.transform.scale(self.serpent_image, serpent_size)
        self.serpent_visible = False
        self.serpent_position = [640, 360]  # Center of the screen
        self.serpent_rect = pygame.Rect(self.serpent_position[0], self.serpent_position[1],
                                      serpent_size[0], serpent_size[1])
        self.serpent_frames = [self.serpent_image]  # Use actual image instead of placeholder frames
        
        # Character state
        ground_y = 600  # Shards moved lower
        self.mirror_shards: List[Dict[str, any]] = [
            {
                "collected": False,
                "position": (180, ground_y),
                "rect": pygame.Rect(180, ground_y, 50, 50),
                "image": None,
                "symbol": "ichthys",  # Fish symbol
                "whisper": "Now we see through a glass, darkly...",
                "glow_alpha": 0
            },
            {
                "collected": False,
                "position": (420, ground_y - 30),
                "rect": pygame.Rect(420, ground_y - 30, 50, 50),
                "image": None,
                "symbol": "cross",  # Cross symbol
                "whisper": "You shall know the truth...",
                "glow_alpha": 0
            },
            {
                "collected": False,
                "position": (650, ground_y + 20),
                "rect": pygame.Rect(650, ground_y + 20, 50, 50),
                "image": None,
                "symbol": "triangle",  # Trinity triangle
                "whisper": "Who told you that you were naked?",
                "glow_alpha": 0
            },
            {
                "collected": False,
                "position": (850, ground_y - 15),
                "rect": pygame.Rect(850, ground_y - 15, 50, 50),
                "image": None,
                "symbol": "serpent",  # Serpent symbol
                "whisper": "The serpent was more crafty than any other...",
                "glow_alpha": 0
            },
            {
                "collected": False,
                "position": (1050, ground_y + 10),
                "rect": pygame.Rect(1050, ground_y + 10, 50, 50),
                "image": None,
                "symbol": "dove",  # Dove symbol
                "whisper": "The Spirit of truth will guide you...",
                "glow_alpha": 0
            }
        ]
        
        # Character boundaries and movement
        self.character_min_x = 100
        self.character_max_x = 1100
        self.character_y = 400  # Character higher up
        self.character_pos = [640, self.character_y]
        self.character_speed = 300  # Pixels per second
        self.character_target = None
        self.character_direction = 1  # 1 for right, -1 for left
        self.character_visible = True
        self.character_moving = False  # New flag to track movement state
        
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
        for i in range(5):  # 5 slots for 5 shards
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
        
        # Mirror frame for shard placement (moved further right and up)
        self.mirror_frame_rect = pygame.Rect(1050, 30, 200, 350)  # Moved further right and made slightly smaller
        self.mirror_frame = pygame.Surface((200, 350), pygame.SRCALPHA)
        # Add gradient background to mirror frame
        for y in range(350):
            alpha = max(180, int(200 * (1 - y/350)))
            pygame.draw.line(self.mirror_frame, (40, 35, 45, alpha), (0, y), (200, y))
        # Add frame border
        pygame.draw.rect(self.mirror_frame, (139, 105, 20), pygame.Rect(0, 0, 200, 350), 3)
        self.mirror_slots = []
        self._setup_mirror_frame()
        
        # UI Elements - Move dialogue to top middle
        self.dialogue_rect = pygame.Rect(280, 20, 720, 80)  # Moved to top
        self.dialogue_frame_rect = pygame.Rect(270, 10, 740, 100)  # Moved to top
        self.dialogue_frame = pygame.Surface((740, 100), pygame.SRCALPHA)
        
        # Create gradient background for dialogue
        for y in range(100):
            alpha = max(180, int(200 * (1 - y/100)))
            pygame.draw.line(self.dialogue_frame, (30, 25, 35, alpha), 
                           (0, y), (740, y))
        
        # Main panel
        pygame.draw.rect(self.dialogue_frame, (45, 40, 50, 230), pygame.Rect(10, 10, 720, 80))
        # Golden border
        pygame.draw.rect(self.dialogue_frame, (139, 105, 20), pygame.Rect(10, 10, 720, 80), 3)
        
        # Corner decorations
        corner_size = 20
        for x, y in [(10, 10), (710, 10), (10, 70), (710, 70)]:
            # Outer corner
            pygame.draw.rect(self.dialogue_frame, (184, 134, 11), (x, y, corner_size, corner_size), 2)
            # Inner corner
            pygame.draw.rect(self.dialogue_frame, (218, 165, 32), (x+3, y+3, corner_size-6, corner_size-6), 1)
            # Corner dot
            pygame.draw.circle(self.dialogue_frame, (218, 165, 32), (x + corner_size//2, y + corner_size//2), 2)
        
        # Add decorative lines along the border
        line_length = 20
        spacing = 40
        for i in range(30, 700, spacing):
            # Top border
            pygame.draw.line(self.dialogue_frame, (184, 134, 11), 
                           (i, 10), (i + line_length, 10), 2)
            # Bottom border
            pygame.draw.line(self.dialogue_frame, (184, 134, 11),
                           (i, 90), (i + line_length, 90), 2)
        
        # Side decorations
        for y in range(30, 70, spacing):
            # Left border
            pygame.draw.line(self.dialogue_frame, (184, 134, 11),
                           (10, y), (10, y + line_length), 2)
            # Right border
            pygame.draw.line(self.dialogue_frame, (184, 134, 11),
                           (730, y), (730, y + line_length), 2)
        
        self.dialogue_text = ""
        self.dialogue_timer = 0
        
        # Load fonts
        self.font = pygame.font.SysFont('Arial', 32)
        self.title_font = pygame.font.SysFont('Arial', 40)
        
        # Dialogue state
        self.dialogues = [
            "Welcome to the Mirror Chamber. Collect the mirror shards to reveal your true self.",
            "You found a mirror shard! Place it in the mirror frame.",
            "You need to collect mirror shards first!",
            "Shard placed! {}/{} shards collected.",
            "The mirror is complete! Something is emerging...",
            "The serpent is trying to control you! Click on it to break free!",
            "You have broken free from the serpent's influence!"
        ]
        self.current_dialogue_index = 0
        self.current_dialogue = self.dialogues[0]
        self.dialogue_timer = 0
        self.typing_speed = 0.05  # seconds per character
        self.typing_timer = 0
        self.displayed_text = ""
        
        # Sound effects
        self.sounds = {}
        self._load_sounds()
        
        # Character state
        self.character_position = (400, 500)
        self.character_rect = pygame.Rect(400, 500, 100, 100)
        
        # Cutscene state
        self.cutscene_active = False
        self.cutscene_timer = 0
        self.cutscene_phase = 0
        
        # Create placeholder images
        self._create_placeholder_images()
        
        # Initialize dialogue state
        self.dialogue_active = True  # Set to True to show initial dialogue
        self.dialogue_text = self.dialogues[0]  # Set initial dialogue
        self.displayed_text = ""  # Text that is currently displayed
        self.typing_index = 0  # Index for typing effect
        self.last_type_time = 0  # Time since last character was typed
        
        # Load and create visual elements
        self._create_visual_elements()
        
        # Add test button
        self.test_button = pygame.Rect(10, 10, 150, 40)
        self.test_button_text = "Fill All Shards"
        self.test_button_font = pygame.font.Font(None, 24)
        
        # Initialize serpent animation
        self.serpent_animation_frame = 0
        self.serpent_animation_speed = 0.2
        
    def _setup_inventory(self):
        """Setup inventory slots with medieval styling."""
        slot_size = 50
        padding = 15  # Increased padding for better spacing
        slots_per_row = 3  # Changed to 3 slots per row for better symmetry
        
        # Calculate total width needed for slots
        total_width = (slot_size * slots_per_row) + (padding * (slots_per_row - 1))
        start_x = self.inventory_rect.x + (self.inventory_rect.width - total_width) // 2
        
        for i in range(9):  # Changed to 9 slots (3x3 grid)
            row = i // slots_per_row
            col = i % slots_per_row
            x = start_x + col * (slot_size + padding)
            y = self.inventory_rect.y + 80 + row * (slot_size + padding)  # More space for title
            self.inventory_slots.append({
                'rect': pygame.Rect(x, y, slot_size, slot_size),
                'item': None,
                'highlighted': False
            })
            
    def _setup_mirror_frame(self):
        """Setup mirror frame slots for shard placement."""
        # Create a mirror shape formation for the slots
        slot_positions = [
            (125, 50),   # Top center
            (75, 150),   # Middle left
            (175, 150),  # Middle right
            (50, 250),   # Bottom left
            (200, 250),  # Bottom right
        ]
        
        for pos in slot_positions:
            x = self.mirror_frame_rect.x + pos[0] - 25  # Center the 50x50 slot
            y = self.mirror_frame_rect.y + pos[1] - 25
            slot_rect = pygame.Rect(x, y, 50, 50)
            self.mirror_slots.append({
                'rect': slot_rect,
                'shard': None,
                'highlighted': False
            })
            
    def _load_sounds(self) -> None:
        """Load sound effects."""
        try:
            self.sounds["shard_collect"] = self.resource_manager.load_sound("shard_collect.wav")
            self.sounds["shard_place"] = self.resource_manager.load_sound("shard_place.wav")
            self.sounds["serpent_appear"] = self.resource_manager.load_sound("serpent_appear.wav")
            self.sounds["serpent_defeat"] = self.resource_manager.load_sound("serpent_defeat.wav")
        except pygame.error as e:
            print(f"Warning: Could not load some sounds: {e}")
            
    def _play_sound(self, sound_name: str) -> None:
        """Play a sound effect if available."""
        if self.sounds.get(sound_name):
            self.sounds[sound_name].play()
            
    def _set_dialogue(self, message):
        """Set the current dialogue message."""
        self.current_dialogue = message
        self.dialogue_timer = 0
        
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle scene events."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check test button
            if self.test_button.collidepoint(event.pos):
                # Fill all shards
                for shard in self.mirror_shards:
                    if not shard["collected"]:
                        shard["collected"] = True
                        # Add to inventory
                        for slot in self.inventory_slots:
                            if not slot["item"]:
                                slot["item"] = shard
                                break
                
                # Place all shards in mirror slots
                for slot in self.mirror_slots:
                    if not slot["shard"]:
                        # Find a shard in inventory
                        for inv_slot in self.inventory_slots:
                            if inv_slot["item"]:
                                slot["shard"] = inv_slot["item"]
                                inv_slot["item"] = None
                                break
                
                # Check if mirror is complete
                placed_count = sum(1 for s in self.mirror_slots if s["shard"])
                if placed_count == len(self.mirror_slots):
                    self._check_puzzle_completion()
                
                return

            # Check for door click when available
            if self.can_exit and self.door_rect.collidepoint(event.pos):
                self.start_transition("blind_marketplace")
                return
            
            # Check for serpent defeat when all shards are placed
            if self.mirror_complete and self.serpent_visible:
                if self.serpent_rect.collidepoint(event.pos):
                    self._break_free_from_serpent()
                    return
            
            # Check for shard collection
            for shard in self.mirror_shards:
                if not shard["collected"] and shard["rect"].collidepoint(event.pos):
                    self._collect_shard(shard)
                    return
            
            # Check for inventory interaction
            for slot in self.inventory_slots:
                if slot["rect"].collidepoint(event.pos) and slot["item"]:
                    self.dragged_item = slot["item"]
                    slot["item"] = None
                    self.drag_offset = (
                        slot["rect"].x - event.pos[0],
                        slot["rect"].y - event.pos[1]
                    )
                    return
            
            # Check for mirror slot interaction
            if self.dragged_item:
                for slot in self.mirror_slots:
                    if slot["rect"].collidepoint(event.pos) and not slot["shard"]:
                        self._place_shard(slot)
                        return
            
            # Handle character movement
            if not self.mirror_frame_rect.collidepoint(event.pos):
                # Move character to click position if within reasonable height
                if event.pos[1] >= 200:  # Allow clicking anywhere below y=200
                    target_x = min(max(event.pos[0], self.character_min_x), self.character_max_x)
                    self.character_target = target_x
                    self.character_direction = 1 if target_x > self.character_pos[0] else -1
                    self.character_moving = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragged_item:
                # Try to place in mirror slots first
                mouse_pos = pygame.mouse.get_pos()
                placed = False
                
                for slot in self.mirror_slots:
                    if slot["rect"].collidepoint(mouse_pos) and not slot["shard"]:
                        self._place_shard(slot)
                        placed = True
                        break
                
                # If not placed in mirror, try inventory slots
                if not placed:
                    for slot in self.inventory_slots:
                        if slot["rect"].collidepoint(mouse_pos) and not slot["item"]:
                            slot["item"] = self.dragged_item
                            placed = True
                            break
                
                # If still not placed, return to original slot
                if not placed:
                    for slot in self.inventory_slots:
                        if not slot["item"]:
                            slot["item"] = self.dragged_item
                            break
                
                self.dragged_item = None
                self.drag_offset = (0, 0)
        
        elif event.type == pygame.MOUSEMOTION:
            # Update highlighted states
            mouse_pos = pygame.mouse.get_pos()
            
            # Update inventory slot highlights
            for slot in self.inventory_slots:
                slot["highlighted"] = slot["rect"].collidepoint(mouse_pos)
            
            # Update mirror slot highlights
            for slot in self.mirror_slots:
                slot["highlighted"] = (
                    slot["rect"].collidepoint(mouse_pos) and 
                    self.dragged_item and 
                    not slot["shard"]
                )

    def update(self, dt: float) -> None:
        """Update game state."""
        super().update(dt)
        
        # Check if all shards are collected
        self.all_shards_collected = all(shard["collected"] for shard in self.mirror_shards)
        
        # Check if mirror is complete
        placed_shards = sum(1 for slot in self.mirror_slots if slot["shard"] is not None)
        if placed_shards == len(self.mirror_slots) and not self.mirror_complete:
            self.mirror_complete = True
            self._start_cutscene()
        
        # Update serpent position if visible
        if self.serpent_visible:
            # Make serpent move in a figure-8 pattern
            time = pygame.time.get_ticks() / 1000.0  # Convert to seconds
            self.serpent_position[0] = 640 + math.sin(time) * 200
            self.serpent_position[1] = 360 + math.cos(time * 0.5) * 100
            self.serpent_rect.x = self.serpent_position[0] - self.serpent_rect.width // 2
            self.serpent_rect.y = self.serpent_position[1] - self.serpent_rect.height // 2
        
        # Update light flicker
        self.light_flicker_intensity = (math.sin(pygame.time.get_ticks() * 0.001 * self.light_flicker_speed) + 1) * 0.5
        
        # Update water drips
        self.water_drip_timer += dt
        if self.water_drip_timer >= self.water_drip_interval:
            self.water_drip_timer = 0
            # Add new water drip
            self.water_drips.append({
                'x': random.randint(100, 1180),
                'y': 0,
                'speed': random.uniform(100, 150),
                'size': random.uniform(2, 4),
                'alpha': 255
            })
        
        # Update existing water drips
        for drip in self.water_drips[:]:
            drip['y'] += drip['speed'] * dt
            if drip['y'] > 720:
                self.water_drips.remove(drip)
            elif drip['y'] > 600:  # Start fading out near bottom
                drip['alpha'] = max(0, drip['alpha'] - 300 * dt)
        
        # Update character movement with proper boundaries
        if self.character_target is not None and self.character_moving:
            # Calculate direction and distance
            direction = 1 if self.character_target > self.character_pos[0] else -1
            distance = abs(self.character_target - self.character_pos[0])
            
            # Move character
            move_amount = min(self.character_speed * dt, distance)
            new_x = self.character_pos[0] + move_amount * direction
            
            # Keep character within screen bounds
            self.character_pos[0] = max(self.character_min_x, min(new_x, self.character_max_x))
            
            # Update character direction
            self.character_direction = direction
            
            # Update character rect (maintain fixed Y position)
            self.character_rect.x = self.character_pos[0] - self.character_image.get_width() // 2
            self.character_rect.y = self.character_y
            
            # Check if reached target
            if distance <= 5:  # Increased threshold for better stopping
                self.character_target = None
                self.character_moving = False
        
        # Update dialogue typing effect
        if self.dialogue_active and self.dialogue_text:
            current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
            if current_time - self.last_type_time >= self.typing_speed:
                if self.typing_index < len(self.dialogue_text):
                    self.displayed_text = self.dialogue_text[:self.typing_index + 1]
                    self.typing_index += 1
                    self.last_type_time = current_time
        
        # Update serpent animation if visible
        if self.serpent_visible:
            self.serpent_animation_frame += self.serpent_animation_speed * dt
            if self.serpent_animation_frame >= len(self.serpent_frames):
                self.serpent_animation_frame = 0
            self.serpent_image = self.serpent_frames[int(self.serpent_animation_frame)]
        
        if self.cutscene_active:
            self.cutscene_timer += dt
            
            # Update cutscene phases
            if self.cutscene_timer >= 5.0 and self.cutscene_phase == 0:
                self.cutscene_phase = 1
                self._set_dialogue(5)  # "The serpent is trying to control you!"
            elif self.cutscene_timer >= 10.0 and self.cutscene_phase == 1:
                self.cutscene_phase = 2
                
        # Update shard glow effects
        mouse_pos = pygame.mouse.get_pos()
        for shard in self.mirror_shards:
            if not shard["collected"]:
                # Increase glow when mouse is near
                distance = math.sqrt(
                    (mouse_pos[0] - shard["rect"].centerx)**2 +
                    (mouse_pos[1] - shard["rect"].centery)**2
                )
                if distance < 100:
                    shard["glow_alpha"] = min(shard["glow_alpha"] + 300 * dt, 255)
                else:
                    shard["glow_alpha"] = max(shard["glow_alpha"] - 300 * dt, 0)

    def _draw_decorative_panel(self, surface: pygame.Surface, rect: pygame.Rect, title: str = None):
        """Draw a decorative panel with medieval styling."""
        # Background
        pygame.draw.rect(surface, self.colors['panel_background'], rect)
        
        # Ornate border
        border_width = 4
        pygame.draw.rect(surface, self.colors['panel_border'], rect, border_width)
        
        # Corner decorations
        corner_size = 20
        for x, y in [(rect.x, rect.y), (rect.right-corner_size, rect.y),
                     (rect.x, rect.bottom-corner_size), (rect.right-corner_size, rect.bottom-corner_size)]:
            pygame.draw.rect(surface, self.colors['panel_border_highlight'], 
                           pyg.Rect(x, y, corner_size, corner_size), 2)
            
        # Title if provided
        if title:
            # Shadow
            text_surface = self.title_font.render(title, True, self.colors['text_shadow'])
            text_rect = text_surface.get_rect(midtop=(rect.centerx + 2, rect.y + 12))
            surface.blit(text_surface, text_rect)
            # Text
            text_surface = self.title_font.render(title, True, self.colors['panel_border_highlight'])
            text_rect = text_surface.get_rect(midtop=(rect.centerx, rect.y + 10))
            surface.blit(text_surface, text_rect)
            
    def render(self, screen: pygame.Surface) -> None:
        """Render the scene."""
        # Draw background and existing elements
        screen.blit(self.background, (0, 0))
        
        # Draw door if player can exit
        if self.can_exit:
            door_color = (139, 69, 19)  # Brown
            pygame.draw.rect(screen, door_color, self.door_rect)
            # Door handle
            handle_pos = (self.door_rect.right - 20, self.door_rect.centery)
            pygame.draw.circle(screen, (218, 165, 32), handle_pos, 5)
            # Door frame
            pygame.draw.rect(screen, (101, 67, 33), self.door_rect, 3)
        
        # Draw scripture on walls
        screen.blit(self.scripture_surface, (0, 0))
        
        # Draw stained glass dome with flicker effect
        flicker_surface = self.dome_surface.copy()
        flicker_surface.set_alpha(int(128 + 64 * self.light_flicker_intensity))
        screen.blit(flicker_surface, (0, 0))
        
        # Draw light rays with flicker
        ray_alpha = int(40 + 20 * self.light_flicker_intensity)
        for ray in self.light_rays:
            ray_surface = pygame.Surface((ray['width'], 720), pygame.SRCALPHA)
            for y in range(0, 720, 2):
                alpha = int(ray['alpha'] * (1 - y/720) * self.light_flicker_intensity)
                pygame.draw.line(ray_surface, (*self.colors['light_ray'][:3], alpha),
                               (ray['width']//2, y), (ray['width']//2, y+1), ray['width'])
            screen.blit(ray_surface, (ray['x'] - ray['width']//2, 0))
        
        # Draw water drips
        for drip in self.water_drips:
            pygame.draw.circle(screen, (*self.colors['water'][:3], int(drip['alpha'])),
                             (int(drip['x']), int(drip['y'])), drip['size'])
        
        # Draw mirror frame and slots
        screen.blit(self.mirror_frame, self.mirror_frame_rect)
        for slot in self.mirror_slots:
            if slot['highlighted']:
                pygame.draw.rect(screen, (255, 223, 0, 50), slot['rect'], 2)  # Highlight available slots
            if slot['shard']:
                screen.blit(slot['shard']['image'], slot['rect'])
        
        # Draw mirror shards with glow effects
        for shard in self.mirror_shards:
            if not shard["collected"]:
                if shard["glow_alpha"] > 0:
                    glow = shard["glow_surface"].copy()
                    glow.set_alpha(int(shard["glow_alpha"]))
                    screen.blit(glow, (shard["rect"].x - 10, shard["rect"].y - 10))
                screen.blit(shard["image"], shard["rect"])
        
        # Draw character
        if self.character_visible:
            screen.blit(self.character_image, self.character_rect)
        
        # Draw serpent if visible
        if self.serpent_visible:
            screen.blit(self.serpent_image, self.serpent_rect)
        
        # Draw dragged item if any
        if self.dragged_item:
            pos = pygame.mouse.get_pos()
            screen.blit(self.dragged_item['image'], 
                       (pos[0] + self.drag_offset[0], 
                        pos[1] + self.drag_offset[1]))
        
        # Draw UI frames
        screen.blit(self.inventory_frame, (self.inventory_rect.x - 20, self.inventory_rect.y - 20))
        
        # Draw inventory slots with improved styling and centered items
        for slot in self.inventory_slots:
            screen.blit(self.slot_frame, slot['rect'])
            if slot['item']:
                # Center the item in the slot
                item_x = slot['rect'].centerx - slot['item']['image'].get_width() // 2
                item_y = slot['rect'].centery - slot['item']['image'].get_height() // 2
                screen.blit(slot['item']['image'], (item_x, item_y))
            if slot['highlighted']:
                # Golden highlight effect
                pygame.draw.rect(screen, (218, 165, 32, 100), slot['rect'], 3)
                # Inner glow
                pygame.draw.rect(screen, (255, 223, 0, 50), slot['rect'].inflate(-4, -4), 2)
        
        # Draw dialogue if active
        if self.dialogue_active and self.dialogue_text:
            # Draw dialogue frame with gradient background
            screen.blit(self.dialogue_frame, self.dialogue_frame_rect)
            
            # Calculate text dimensions for proper wrapping
            max_width = self.dialogue_rect.width - 40
            words = self.displayed_text.split()
            lines = []
            current_line = []
            current_width = 0
            
            # Word wrap
            for word in words:
                word_surface = self.font.render(word + " ", True, (255, 246, 208))
                word_width = word_surface.get_width()
                
                if current_width + word_width <= max_width:
                    current_line.append(word)
                    current_width += word_width
                else:
                    lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
            
            if current_line:
                lines.append(" ".join(current_line))
            
            # Draw text lines
            line_height = self.font.get_linesize()
            start_y = self.dialogue_rect.centery - (len(lines) * line_height) // 2
            
            for i, line in enumerate(lines):
                # Draw text shadow for depth
                shadow_surface = self.font.render(line, True, (0, 0, 0))
                shadow_rect = shadow_surface.get_rect(
                    centerx=self.dialogue_rect.centerx + 2,
                    y=start_y + i * line_height + 2
                )
                screen.blit(shadow_surface, shadow_rect)
                
                # Draw main text with golden tint
                text_surface = self.font.render(line, True, (255, 246, 208))
                text_rect = text_surface.get_rect(
                    centerx=self.dialogue_rect.centerx,
                    y=start_y + i * line_height
                )
                screen.blit(text_surface, text_rect)
        
        # Draw test button
        pygame.draw.rect(screen, (100, 100, 100), self.test_button)
        pygame.draw.rect(screen, (200, 200, 200), self.test_button, 2)
        text_surface = self.test_button_font.render(self.test_button_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.test_button.center)
        screen.blit(text_surface, text_rect)
        
    def _check_puzzle_completion(self):
        """Check if all mirror shards are placed correctly."""
        all_placed = all(slot['shard'] for slot in self.mirror_slots)
        if all_placed:
            self.dialogue_text = "The mirror is complete! The path is revealed..."
            self.dialogue_timer = 3.0
            # Start the cutscene instead of transitioning immediately
            self._start_cutscene()
            
    def _create_placeholder_images(self) -> None:
        """Create placeholder images for UI elements."""
        # Define symbol shapes and colors
        symbol_shapes = {
            "ichthys": [  # Fish shape
                [(0, 25), (15, 10), (35, 10), (50, 25), (35, 40), (15, 40)]
            ],
            "cross": [  # Cross shape
                [(20, 5), (30, 5), (30, 20), (45, 20), (45, 30), (30, 30), (30, 45), (20, 45), (20, 30), (5, 30), (5, 20), (20, 20)]
            ],
            "triangle": [  # Trinity triangle
                [(25, 5), (45, 40), (5, 40)],  # Outer triangle
                [(25, 15), (35, 35), (15, 35)]  # Inner triangle
            ],
            "serpent": [  # Serpent shape
                [(10, 25), (20, 15), (30, 25), (40, 15), (45, 25), (40, 35), (30, 25), (20, 35)]
            ],
            "dove": [  # Dove shape
                [(25, 10), (40, 20), (45, 30), (25, 40), (5, 30), (10, 20)]
            ]
        }
        
        # Create shard images with embedded symbols
        shard_colors = [
            (200, 220, 255, 180),  # Blue tint
            (220, 200, 255, 180),  # Purple tint
            (255, 220, 200, 180),  # Orange tint
            (200, 255, 220, 180),  # Green tint
            (255, 255, 200, 180)   # Yellow tint
        ]
        
        for i, shard in enumerate(self.mirror_shards):
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            
            # Create unique shard shapes
            if i == 0:  # Top piece
                points = [(25, 0), (50, 25), (25, 50), (0, 25)]  # Diamond shape
            elif i == 1:  # Left piece
                points = [(0, 0), (50, 15), (50, 35), (0, 50)]  # Left-pointing
            elif i == 2:  # Right piece
                points = [(0, 15), (50, 0), (50, 50), (0, 35)]  # Right-pointing
            elif i == 3:  # Bottom left
                points = [(0, 0), (50, 0), (25, 50), (0, 35)]  # Triangle variant
            else:  # Bottom right
                points = [(0, 0), (50, 0), (50, 35), (25, 50)]  # Triangle variant
            
            # Draw base shard with glass texture
            pygame.draw.polygon(surface, shard_colors[i], points)
            
            # Add symbol
            symbol = symbol_shapes[shard["symbol"]]
            for shape in symbol:
                pygame.draw.polygon(surface, (255, 255, 255, 100), shape, 1)
            
            # Add highlights and reflections
            highlight_points = [
                (points[0][0] + 5, points[0][1] + 5),
                (points[1][0] - 5, points[1][1] + 5),
                (points[2][0] - 5, points[2][1] - 5)
            ]
            pygame.draw.polygon(surface, (255, 255, 255, 80), highlight_points)
            
            # Add border
            pygame.draw.polygon(surface, (255, 255, 255, 150), points, 2)
            
            shard["image"] = surface
            
            # Create glow surface
            glow_surface = pygame.Surface((70, 70), pygame.SRCALPHA)
            glow_rect = pygame.Rect(10, 10, 50, 50)
            for radius in range(5, 0, -1):
                pygame.draw.rect(glow_surface, (*self.colors['glow'][:3], 10),
                               glow_rect.inflate(radius*2, radius*2), border_radius=radius)
            shard["glow_surface"] = glow_surface
        
        # Create mirror frame with more detail
        self.mirror_frame_surface = pygame.Surface((200, 300), pygame.SRCALPHA)
        # Frame border
        pygame.draw.rect(self.mirror_frame_surface, (150, 150, 150), (0, 0, 200, 300), 5)
        # Frame details
        pygame.draw.rect(self.mirror_frame_surface, (100, 100, 100), (10, 10, 180, 280))
        # Frame decorations
        for i in range(4):
            pygame.draw.circle(self.mirror_frame_surface, (180, 180, 180), 
                             (20 + i*60, 20), 10)
            pygame.draw.circle(self.mirror_frame_surface, (180, 180, 180), 
                             (20 + i*60, 280), 10)
            
    def _start_cutscene(self) -> None:
        """Start the serpent cutscene."""
        self.cutscene_active = True
        self.cutscene_timer = 0
        self.cutscene_phase = 0
        self.serpent_visible = True
        self._set_dialogue("The mirror is complete! But wait... the serpent appears! Click on it to break free!")
        self._play_sound("serpent_appear")
            
    def _break_free_from_serpent(self) -> None:
        """Break free from the serpent's influence."""
        self.serpent_visible = False
        self.serpent_defeated = True
        self.can_exit = True
        self._set_dialogue("You have broken free from the serpent's influence! The door is now open.")
        self._play_sound("serpent_defeat")
        
    def _complete_scene(self) -> None:
        """Complete the scene and prepare for transition."""
        # Update game state if needed
        if hasattr(self.game_state, 'armor_pieces'):
            self.game_state.armor_pieces["belt_of_truth"] = True
        # For now, just restart the scene
        self.start_transition("mirror_chamber")
        
    def _create_decorative_frame(self, size) -> pygame.Surface:
        """Create a decorative medieval-style frame."""
        surface = pygame.Surface(size, pygame.SRCALPHA)
        width, height = size
        
        # Fill with semi-transparent background
        pygame.draw.rect(surface, self.colors['panel_background'], (0, 0, width, height))
        
        # Draw ornate border
        border_width = 4
        pygame.draw.rect(surface, self.colors['panel_border'], (0, 0, width, height), border_width)
        
        # Add corner decorations
        corner_size = 20
        for x, y in [(0, 0), (width-corner_size, 0), 
                     (0, height-corner_size), (width-corner_size, height-corner_size)]:
            # Outer corner
            pygame.draw.rect(surface, self.colors['panel_border_highlight'], 
                           (x, y, corner_size, corner_size), 2)
            # Inner corner
            pygame.draw.rect(surface, self.colors['panel_border_highlight'], 
                           (x+4, y+4, corner_size-8, corner_size-8), 1)
            
        # Add decorative lines
        line_length = 40
        for x in range(20, width-20, line_length*2):
            pygame.draw.line(surface, self.colors['panel_border_highlight'], 
                           (x, 0), (x+line_length, 0), 2)
            pygame.draw.line(surface, self.colors['panel_border_highlight'], 
                           (x, height-2), (x+line_length, height-2), 2)
            
        return surface 

    def set_dialogue(self, text: str) -> None:
        """Set new dialogue text and reset typing effect."""
        self.dialogue_text = text
        self.displayed_text = ""
        self.typing_index = 0
        self.last_type_time = pygame.time.get_ticks() / 1000
        self.dialogue_active = True 

    def _create_visual_elements(self) -> None:
        """Create visual elements for the atmospheric scene."""
        # Create stained glass dome effect
        self.dome_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        center_x, center_y = 640, -100  # Dome center above screen
        radius = 800
        
        # Draw dome segments
        for angle in range(0, 180, 15):
            color = (
                random.randint(50, 150),
                random.randint(50, 150),
                random.randint(100, 200),
                100
            )
            start_pos = (
                center_x + radius * math.cos(math.radians(angle)),
                center_y + radius * math.sin(math.radians(angle))
            )
            end_pos = (
                center_x + radius * math.cos(math.radians(angle + 15)),
                center_y + radius * math.sin(math.radians(angle + 15))
            )
            points = [
                (center_x, center_y),
                start_pos,
                end_pos
            ]
            pygame.draw.polygon(self.dome_surface, color, points)
        
        # Add cracks to the dome
        for _ in range(5):
            start_x = random.randint(300, 980)
            start_y = random.randint(0, 200)
            points = [(start_x, start_y)]
            for _ in range(random.randint(3, 6)):
                points.append((
                    points[-1][0] + random.randint(-30, 30),
                    points[-1][1] + random.randint(10, 30)
                ))
            pygame.draw.lines(self.dome_surface, (0, 0, 0, 200), False, points, 2)
        
        # Create scripture on walls
        self.scripture_surface = pygame.Surface((1280, 720), pygame.SRCALPHA)
        scriptures = [
            "Truth", "Light", "Logos", "Word", "Spirit",
            "αρχή", "λόγος", "φῶς", "ἀλήθεια"  # Greek text
        ]
        
        font = pygame.font.SysFont('Arial', 24)
        for text in scriptures:
            x = random.randint(50, 1230)
            y = random.randint(50, 670)
            # Draw faded/erased effect
            alpha = random.randint(30, 128)
            text_surface = font.render(text, True, (*self.colors['scripture'][:3], alpha))
            # Randomly rotate text
            angle = random.randint(-30, 30)
            rotated_text = pygame.transform.rotate(text_surface, angle)
            self.scripture_surface.blit(rotated_text, 
                                      (x - rotated_text.get_width()//2,
                                       y - rotated_text.get_height()//2))
        
        # Create light rays
        self.light_rays = []
        for _ in range(5):
            x = random.randint(300, 980)
            self.light_rays.append({
                'x': x,
                'width': random.randint(40, 80),
                'alpha': random.randint(20, 40)
            }) 

    def _collect_shard(self, shard: Dict[str, any]) -> None:
        """Collect a mirror shard and add it to inventory."""
        # Check if character is close enough to collect
        shard_center_x = shard["rect"].centerx
        character_center_x = self.character_pos[0]
        if abs(shard_center_x - character_center_x) < 100:  # Collection range
            shard["collected"] = True
            # Add to inventory
            for slot in self.inventory_slots:
                if not slot["item"]:
                    slot["item"] = shard
                    self._play_sound("shard_collect")
                    self._set_dialogue("You found a mirror shard! Place it in the mirror frame.")
                    break
        else:
            # Move character to shard if too far
            self.character_target = shard_center_x
            self.character_direction = 1 if shard_center_x > self.character_pos[0] else -1
            self.character_moving = True
            
    def _place_shard(self, slot: Dict[str, any]) -> None:
        """Place a shard in a mirror slot."""
        if self.dragged_item:
            slot["shard"] = self.dragged_item
            self.dragged_item = None
            self._play_sound("shard_place")
            
            # Count placed shards
            placed_count = sum(1 for s in self.mirror_slots if s["shard"])
            self._set_dialogue(f"Shard placed! {placed_count}/{len(self.mirror_slots)} shards collected.")
            
            # Check if mirror is complete
            if placed_count == len(self.mirror_slots):
                self._check_puzzle_completion() 