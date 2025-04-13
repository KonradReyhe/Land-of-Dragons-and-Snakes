"""
Mirror Chamber Scene
A mystical chamber where the player must collect and place mirror shards.
"""

from typing import Dict, List, Optional, Tuple
import pygame
import math
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
        
        # Colors
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
            'glow': (255, 223, 0, 50)  # Golden glow
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
        
        # Character state
        ground_y = 600  # Shards moved lower
        self.mirror_shards: List[Dict[str, any]] = [
            {"collected": False, "position": (180, ground_y), "rect": pygame.Rect(180, ground_y, 50, 50), "image": None},
            {"collected": False, "position": (420, ground_y - 30), "rect": pygame.Rect(420, ground_y - 30, 50, 50), "image": None},
            {"collected": False, "position": (650, ground_y + 20), "rect": pygame.Rect(650, ground_y + 20, 50, 50), "image": None},
            {"collected": False, "position": (850, ground_y - 15), "rect": pygame.Rect(850, ground_y - 15, 50, 50), "image": None},
            {"collected": False, "position": (1050, ground_y + 10), "rect": pygame.Rect(1050, ground_y + 10, 50, 50), "image": None}
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
        self.inventory_rect = pygame.Rect(10, 10, 250, 300)  # Smaller, more compact
        self.inventory_slots = []
        self.dragged_item = None
        self.drag_offset = (0, 0)
        self._setup_inventory()
        
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
        
        # Serpent state
        self.serpent_visible = False
        self.serpent_position = (0, 0)
        self.serpent_animation_frame = 0
        self.serpent_animation_speed = 0.1
        
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
            
    def _set_dialogue(self, index: int, format_args: tuple = None) -> None:
        """Set the current dialogue and reset typing."""
        self.current_dialogue_index = index
        if format_args:
            self.current_dialogue = self.dialogues[index].format(*format_args)
        else:
            self.current_dialogue = self.dialogues[index]
        self.displayed_text = ""
        self.typing_timer = 0
        
    def handle_events(self, event: pygame.event.Event) -> None:
        """Handle events including movement and drag-and-drop."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                
                # First check if clicking inventory
                clicked_inventory = False
                for slot in self.inventory_slots:
                    if slot['rect'].collidepoint(mouse_pos) and slot['item']:
                        self.dragged_item = slot['item']
                        slot['item'] = None
                        # Center the item on cursor
                        self.drag_offset = (
                            -25,  # Half of the shard size (50/2)
                            -25
                        )
                        clicked_inventory = True
                        break
                
                # If not clicking inventory or mirror frame, handle movement
                if not clicked_inventory and not self.mirror_frame_rect.collidepoint(mouse_pos):
                    # Move character to click position if within reasonable height
                    if mouse_pos[1] >= 200:  # Allow clicking anywhere below y=200
                        target_x = min(max(mouse_pos[0], self.character_min_x), self.character_max_x)
                        self.character_target = target_x
                        self.character_direction = 1 if target_x > self.character_pos[0] else -1
                        self.character_moving = True
                    
                    # Check for mirror shard collection
                    for shard in self.mirror_shards:
                        if not shard["collected"] and shard["rect"].collidepoint(mouse_pos):
                            # Check if character is close enough to collect
                            shard_center_x = shard["rect"].centerx
                            character_center_x = self.character_pos[0]
                            if abs(shard_center_x - character_center_x) < 100:  # Collection range
                                shard["collected"] = True
                                # Add to inventory
                                for slot in self.inventory_slots:
                                    if not slot['item']:
                                        slot['item'] = shard
                                        self._play_sound("shard_collect")
                                        self.set_dialogue(self.dialogues[1])
                                        break
                                break
                            else:
                                # Move character to shard if too far
                                self.character_target = shard_center_x
                                self.character_direction = 1 if shard_center_x > self.character_pos[0] else -1
                                self.character_moving = True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragged_item:
                mouse_pos = pygame.mouse.get_pos()
                dropped = False
                
                # Check if dropping on mirror frame slots
                for slot in self.mirror_slots:
                    if slot['rect'].collidepoint(mouse_pos) and not slot['shard']:
                        slot['shard'] = self.dragged_item
                        dropped = True
                        self._play_sound("shard_place")
                        placed_count = sum(1 for s in self.mirror_slots if s['shard'])
                        self.set_dialogue(self.dialogues[3].format(placed_count, len(self.mirror_slots)))
                        if placed_count == len(self.mirror_slots):
                            self._check_puzzle_completion()
                        break
                
                # If not dropped on mirror, return to inventory
                if not dropped:
                    for slot in self.inventory_slots:
                        if not slot['item']:
                            slot['item'] = self.dragged_item
                            break
                
                self.dragged_item = None
                
        elif event.type == pygame.MOUSEMOTION:
            # Update slot highlighting
            mouse_pos = pygame.mouse.get_pos()
            
            # Highlight mirror slots when dragging a shard
            if self.dragged_item:
                for slot in self.mirror_slots:
                    if not slot['shard']:  # Only highlight empty slots
                        slot['highlighted'] = slot['rect'].collidepoint(mouse_pos)
            
            # Highlight inventory slots
            for slot in self.inventory_slots:
                if not self.dragged_item:  # Only highlight when not dragging
                    slot['highlighted'] = slot['rect'].collidepoint(mouse_pos) and slot['item']

    def update(self, dt: float) -> None:
        """Update the scene state."""
        super().update(dt)
        
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
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw mirror frame and slots
        screen.blit(self.mirror_frame, self.mirror_frame_rect)
        for slot in self.mirror_slots:
            if slot['highlighted']:
                pygame.draw.rect(screen, (255, 223, 0, 50), slot['rect'], 2)  # Highlight available slots
            if slot['shard']:
                screen.blit(slot['shard']['image'], slot['rect'])
        
        # Draw mirror shards on ground
        for shard in self.mirror_shards:
            if not shard["collected"]:
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
        # Create inventory frame with medieval styling
        self.inventory_frame = pygame.Surface((self.inventory_rect.width + 40, self.inventory_rect.height + 40), pygame.SRCALPHA)
        
        # Main background with gradient
        for y in range(self.inventory_rect.height + 40):
            alpha = max(180, int(200 * (1 - y/(self.inventory_rect.height + 40))))
            pygame.draw.line(self.inventory_frame, (30, 25, 35, alpha), 
                           (0, y), (self.inventory_rect.width + 40, y))
        
        # Ornate border
        border_rect = pygame.Rect(20, 20, self.inventory_rect.width, self.inventory_rect.height)
        # Inner panel
        pygame.draw.rect(self.inventory_frame, (45, 40, 50, 230), border_rect)
        # Main border
        pygame.draw.rect(self.inventory_frame, (139, 105, 20), border_rect, 3)  # Golden border
        
        # Corner decorations
        corner_size = 20
        for x, y in [(20, 20), (20 + self.inventory_rect.width - corner_size, 20),
                     (20, 20 + self.inventory_rect.height - corner_size),
                     (20 + self.inventory_rect.width - corner_size, 20 + self.inventory_rect.height - corner_size)]:
            # Outer corner
            pygame.draw.rect(self.inventory_frame, (184, 134, 11), (x, y, corner_size, corner_size), 2)
            # Inner corner design
            pygame.draw.rect(self.inventory_frame, (218, 165, 32), (x+3, y+3, corner_size-6, corner_size-6), 1)
            # Corner dot
            pygame.draw.circle(self.inventory_frame, (218, 165, 32), (x + corner_size//2, y + corner_size//2), 2)
        
        # Title with medieval styling
        title_font = pygame.font.SysFont('Arial', 36)  # Slightly larger font
        title_text = "Inventory"
        
        # Calculate title position (centered)
        title_surface = title_font.render(title_text, True, (218, 165, 32))
        title_width = title_surface.get_width()
        title_x = (self.inventory_rect.width + 40 - title_width) // 2
        
        # Draw title shadow layers for depth
        for offset in [(2, 2), (2, 1), (1, 2)]:
            title_shadow = title_font.render(title_text, True, (0, 0, 0))
            self.inventory_frame.blit(title_shadow, (title_x + offset[0], 35 + offset[1]))
        
        # Draw main title text
        self.inventory_frame.blit(title_surface, (title_x, 35))
        
        # Add decorative lines under title
        line_y = 70
        line_padding = 40
        pygame.draw.line(self.inventory_frame, (184, 134, 11), 
                        (line_padding, line_y), (self.inventory_rect.width + 40 - line_padding, line_y), 2)
        pygame.draw.line(self.inventory_frame, (218, 165, 32), 
                        (line_padding + 10, line_y + 3), (self.inventory_rect.width + 40 - line_padding - 10, line_y + 3), 1)
        
        # Slot styling
        self.slot_frame = pygame.Surface((50, 50), pygame.SRCALPHA)  # Smaller slots
        pygame.draw.rect(self.slot_frame, (60, 55, 65, 200), (0, 0, 50, 50))
        pygame.draw.rect(self.slot_frame, (139, 105, 20), (0, 0, 50, 50), 2)
        # Slot corner accents
        for x, y in [(0, 0), (45, 0), (0, 45), (45, 45)]:
            pygame.draw.line(self.slot_frame, (218, 165, 32), (x, y), (x+5, y), 1)
            pygame.draw.line(self.slot_frame, (218, 165, 32), (x, y), (x, y+5), 1)
        
        # Create mirror shards with more detail and distinct appearance
        shard_colors = [
            (200, 200, 255, 200),  # Blue tint
            (200, 255, 200, 200),  # Green tint
            (255, 200, 200, 200),  # Red tint
            (255, 255, 200, 200),  # Yellow tint
            (200, 255, 255, 200)   # Cyan tint
        ]
        
        for i, shard in enumerate(self.mirror_shards):
            surface = pygame.Surface((50, 50), pygame.SRCALPHA)
            # Create unique shard shapes for each piece
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
            
            # Main shard color with transparency
            pygame.draw.polygon(surface, shard_colors[i], points)
            # Shard border
            pygame.draw.polygon(surface, (255, 255, 255), points, 2)
            # Shard highlight
            highlight_points = [
                (points[0][0] + 5, points[0][1] + 5),
                (points[1][0] - 5, points[1][1] + 5),
                (points[2][0] - 5, points[2][1] - 5)
            ]
            pygame.draw.polygon(surface, (255, 255, 255, 128), highlight_points)
            shard["image"] = surface
            
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
            
        # Create serpent frames with more detail
        self.serpent_frames = []
        for i in range(4):
            surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            # Body
            pygame.draw.ellipse(surface, (0, 150, 0), (20, 20, 60, 40))
            # Head
            pygame.draw.circle(surface, (0, 200, 0), (80, 40), 20)
            # Eyes
            eye_color = (255, 0, 0) if i % 2 == 0 else (255, 255, 0)
            pygame.draw.circle(surface, eye_color, (85, 35), 5)
            pygame.draw.circle(surface, eye_color, (85, 45), 5)
            # Tongue
            if i % 2 == 0:
                pygame.draw.line(surface, (255, 0, 0), (90, 40), (100, 40), 2)
            self.serpent_frames.append(surface)
            
        # Set serpent position
        self.serpent_position = (400, 300)
        self.serpent_rect = pygame.Rect(400, 300, 100, 100)
        
    def _start_cutscene(self) -> None:
        """Start the serpent cutscene."""
        self.cutscene_active = True
        self.cutscene_timer = 0
        self.cutscene_phase = 0
        self.serpent_visible = True
        self._set_dialogue(4)  # "The mirror is complete!"
        self._play_sound("serpent_appear")
            
    def _break_free_from_serpent(self) -> None:
        """Break free from the serpent's influence."""
        self.cutscene_active = False
        self.serpent_visible = False
        self._set_dialogue(6)  # "You have broken free!"
        self._play_sound("serpent_defeat")
        self._complete_scene()
        
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