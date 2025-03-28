"""
Scene 1 module for Land of Dragons and Snakes.
This will contain the logic for the first scene of the game.
"""

import pygame
import os
import time
from utils.cutout import Cutout

# Constants
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
ASSETS_DIR = "assets/scene1/"
CHARACTERS_DIR = "assets/characters/"

# UI Constants
INVENTORY_HEIGHT = 90  # Slightly smaller
INVENTORY_WIDTH = 600  # Fixed width for centered inventory
INVENTORY_SLOT_SIZE = 48  # Smaller slots
INVENTORY_PADDING = 8
INVENTORY_X = (SCREEN_WIDTH - INVENTORY_WIDTH) // 2  # Center inventory
MESSAGE_BOX_HEIGHT = 80
MESSAGE_DURATION = 3.0  # seconds

# Dialog Constants
DIALOG_WIDTH = 800
DIALOG_HEIGHT = 150
DIALOG_PADDING = 20
DIALOG_BG_COLOR = (20, 18, 24, 220)
DIALOG_BORDER_COLOR = (90, 85, 95)
DIALOG_TEXT_COLOR = (220, 215, 230)
DIALOG_FONT_SIZE = 32

# Visual Style Constants
OVERLAY_ALPHA = 180
MESSAGE_BOX_COLOR = (20, 20, 30)
INVENTORY_BG_COLOR = (25, 22, 29)  # Darker, more medieval
INVENTORY_SLOT_COLOR = (35, 32, 39)
INVENTORY_BORDER_COLOR = (90, 85, 95)  # More visible borders
INVENTORY_INNER_COLOR = (45, 42, 50)

# Game Constants
CHARACTER_SPEED = 5
CHARACTER_STOP_THRESHOLD = 5
CHARACTER_Y = 700  # Higher position to avoid inventory
CHARACTER_IDLE_RANGE = 50
CHARACTER_ACCELERATION = 0.2

# Mirror Shard Constants
SHARD_SIZE = (150, 150)  # Consistent size for shards

# Interactive Object Constants
BOOKSHELF_SIZE = (250, 450)  # Width, Height - slightly larger for more presence
BOOKSHELF_Y = 400  # Lower on wall for better visibility

# Object Positions (single bookshelf)
SCENE_OBJECTS = [
    # Format: (name, x, y, width, height, is_movable, description)
    ("bookshelf", 860, BOOKSHELF_Y, BOOKSHELF_SIZE[0], BOOKSHELF_SIZE[1], True, 
     "An old bookshelf, filled with dusty tomes. Something seems off about its placement...")
]

# Mirror shard position (hidden behind bookshelf)
MIRROR_POSITIONS = [
    # Behind the bookshelf
    ("mirror_shard", 900, BOOKSHELF_Y + BOOKSHELF_SIZE[1] - 100, 
     "Behind the bookshelf, you discover a fragment of an ancient mirror...")
]

class MessageLog:
    def __init__(self):
        self.font = pygame.font.Font(None, 42)
        self.messages = []
        self.current_alpha = 255

    def add_message(self, text):
        self.messages.append({
            'text': text,
            'time': time.time(),
            'surface': self.font.render(text, True, (255, 255, 255)),
            'alpha': 255
        })

    def update(self):
        current_time = time.time()
        self.messages = [msg for msg in self.messages 
                        if current_time - msg['time'] < MESSAGE_DURATION]
        
        for msg in self.messages:
            time_left = MESSAGE_DURATION - (current_time - msg['time'])
            if time_left < 0.5:
                msg['alpha'] = int(255 * (time_left / 0.5))

    def render(self, screen):
        if not self.messages:
            return
            
        # Draw medieval-style message box
        overlay = pygame.Surface((SCREEN_WIDTH, MESSAGE_BOX_HEIGHT))
        overlay.fill(MESSAGE_BOX_COLOR)
        overlay.set_alpha(OVERLAY_ALPHA)
        screen.blit(overlay, (0, 0))
        
        # Add decorative lines
        pygame.draw.line(screen, INVENTORY_BORDER_COLOR,
                        (0, MESSAGE_BOX_HEIGHT - 2),
                        (SCREEN_WIDTH, MESSAGE_BOX_HEIGHT - 2), 2)
        
        latest = self.messages[-1]
        msg_surface = latest['surface']
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, MESSAGE_BOX_HEIGHT // 2))
        
        temp_surface = msg_surface.copy()
        temp_surface.set_alpha(latest['alpha'])
        screen.blit(temp_surface, msg_rect)

class InventoryBar:
    def __init__(self):
        self.slots = []
        self.item_images = {}
        self.font = pygame.font.Font(None, 24)
        self.hover_item = None
        self.hover_start_time = 0
        self.tooltip_delay = 0.5
        self.max_visible_slots = 8  # Limit number of visible slots

    def add_item(self, name, image_path):
        if name not in self.item_images:
            image = pygame.image.load(image_path).convert_alpha()
            self.item_images[name] = pygame.transform.scale(image, (INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE))
        if name not in self.slots:
            self.slots.append(name)

    def handle_click(self, pos):
        slot_index = self._get_slot_at_position(pos)
        if slot_index is not None and slot_index < len(self.slots):
            return self.slots[slot_index]
        return None

    def handle_hover(self, pos):
        slot_index = self._get_slot_at_position(pos)
        current_time = time.time()
        
        if slot_index is not None and slot_index < len(self.slots):
            if self.hover_item != self.slots[slot_index]:
                self.hover_item = self.slots[slot_index]
                self.hover_start_time = current_time
        else:
            self.hover_item = None

    def _get_slot_at_position(self, pos):
        if (SCREEN_HEIGHT - INVENTORY_HEIGHT <= pos[1] <= SCREEN_HEIGHT and
            INVENTORY_X <= pos[0] <= INVENTORY_X + INVENTORY_WIDTH):
            relative_x = pos[0] - INVENTORY_X - INVENTORY_PADDING
            slot_index = relative_x // (INVENTORY_SLOT_SIZE + INVENTORY_PADDING)
            if 0 <= slot_index < self.max_visible_slots:
                return slot_index
        return None

    def render(self, screen):
        # Draw main inventory panel
        inventory_rect = pygame.Rect(INVENTORY_X, SCREEN_HEIGHT - INVENTORY_HEIGHT,
                                   INVENTORY_WIDTH, INVENTORY_HEIGHT)
        
        # Draw main background
        pygame.draw.rect(screen, INVENTORY_BG_COLOR, inventory_rect)
        
        # Draw decorative borders
        pygame.draw.rect(screen, INVENTORY_BORDER_COLOR, inventory_rect, 2)
        pygame.draw.line(screen, INVENTORY_BORDER_COLOR,
                        (INVENTORY_X, SCREEN_HEIGHT - INVENTORY_HEIGHT + 4),
                        (INVENTORY_X + INVENTORY_WIDTH, SCREEN_HEIGHT - INVENTORY_HEIGHT + 4), 1)
        
        # Draw slots
        for i in range(min(self.max_visible_slots, len(self.slots))):
            x = INVENTORY_X + INVENTORY_PADDING + i * (INVENTORY_SLOT_SIZE + INVENTORY_PADDING)
            y = SCREEN_HEIGHT - INVENTORY_HEIGHT + (INVENTORY_HEIGHT - INVENTORY_SLOT_SIZE) // 2
            
            # Draw slot background with inner shadow effect
            slot_rect = pygame.Rect(x, y, INVENTORY_SLOT_SIZE, INVENTORY_SLOT_SIZE)
            pygame.draw.rect(screen, INVENTORY_SLOT_COLOR, slot_rect)
            pygame.draw.rect(screen, INVENTORY_INNER_COLOR, slot_rect, 1)
            pygame.draw.rect(screen, INVENTORY_BORDER_COLOR, slot_rect, 2)
            
            if i < len(self.slots):
                item_name = self.slots[i]
                if item_name in self.item_images:
                    screen.blit(self.item_images[item_name], (x + 2, y + 2))
                
                if item_name == self.hover_item and time.time() - self.hover_start_time > self.tooltip_delay:
                    self._draw_tooltip(screen, item_name, (x, y))

    def _draw_tooltip(self, screen, item_name, pos):
        text = self.font.render(item_name.replace('_', ' ').title(), True, (255, 255, 255))
        padding = 10
        tooltip_rect = pygame.Rect(pos[0], pos[1] - 35, text.get_width() + padding * 2, 25)
        
        if tooltip_rect.right > SCREEN_WIDTH:
            tooltip_rect.right = SCREEN_WIDTH
        
        pygame.draw.rect(screen, MESSAGE_BOX_COLOR, tooltip_rect)
        pygame.draw.rect(screen, INVENTORY_BORDER_COLOR, tooltip_rect, 1)
        screen.blit(text, (tooltip_rect.x + padding, tooltip_rect.y + 4))

class DialogBox:
    def __init__(self):
        self.font = pygame.font.Font(None, DIALOG_FONT_SIZE)
        self.current_text = None
        self.start_time = 0
        self.duration = 5.0  # How long to show each message
        self.surface = pygame.Surface((DIALOG_WIDTH, DIALOG_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(centerx=SCREEN_WIDTH//2, bottom=SCREEN_HEIGHT-INVENTORY_HEIGHT-20)
        
        # Opening text
        self.welcome_text = [
            "You find yourself in a peculiar room...",
            "Ancient symbols cover the walls, and broken mirrors catch what little light remains.",
            "Something about these mirror shards feels... significant."
        ]
        self.current_welcome_index = 0
        self.show_welcome_message()

    def show_welcome_message(self):
        if self.current_welcome_index < len(self.welcome_text):
            self.show_text(self.welcome_text[self.current_welcome_index])
            self.current_welcome_index += 1

    def show_text(self, text):
        self.current_text = text
        self.start_time = time.time()

    def update(self):
        if self.current_text:
            if time.time() - self.start_time > self.duration:
                self.current_text = None
                # Show next welcome message if available
                if self.current_welcome_index < len(self.welcome_text):
                    self.show_welcome_message()

    def render(self, screen):
        if self.current_text:
            # Clear surface
            self.surface.fill((0, 0, 0, 0))
            
            # Draw background with medieval style
            pygame.draw.rect(self.surface, DIALOG_BG_COLOR, 
                           (0, 0, DIALOG_WIDTH, DIALOG_HEIGHT))
            
            # Draw decorative borders
            pygame.draw.rect(self.surface, DIALOG_BORDER_COLOR,
                           (0, 0, DIALOG_WIDTH, DIALOG_HEIGHT), 2)
            pygame.draw.line(self.surface, DIALOG_BORDER_COLOR,
                           (DIALOG_PADDING, DIALOG_PADDING),
                           (DIALOG_WIDTH - DIALOG_PADDING, DIALOG_PADDING), 1)
            pygame.draw.line(self.surface, DIALOG_BORDER_COLOR,
                           (DIALOG_PADDING, DIALOG_HEIGHT - DIALOG_PADDING),
                           (DIALOG_WIDTH - DIALOG_PADDING, DIALOG_HEIGHT - DIALOG_PADDING), 1)
            
            # Render text with word wrap
            words = self.current_text.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if self.font.size(test_line)[0] < DIALOG_WIDTH - DIALOG_PADDING * 2:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            # Draw text lines
            y = DIALOG_PADDING + 10
            for line in lines:
                text_surface = self.font.render(line, True, DIALOG_TEXT_COLOR)
                text_rect = text_surface.get_rect(centerx=DIALOG_WIDTH//2, top=y)
                self.surface.blit(text_surface, text_rect)
                y += self.font.get_linesize()
            
            screen.blit(self.surface, self.rect)

class InteractiveObject(Cutout):
    def __init__(self, name, image_path, x, y, width, height, is_movable=False):
        super().__init__(name, image_path, x, y)
        self.original_x = x
        self.is_movable = is_movable
        self.is_moved = False
        self.move_distance = 100  # How far the bookshelf moves when pushed
        
        # Scale image to desired size
        if self.image:
            self.image = pygame.transform.scale(self.image, (width, height))
            self.rect.size = (width, height)
    
    def move(self):
        if self.is_movable and not self.is_moved:
            self.rect.x += self.move_distance
            self.is_moved = True
            return True
        return False

class Scene1:
    def __init__(self):
        # Load and scale background
        self.background = pygame.image.load(os.path.join(ASSETS_DIR, "scene1_background.png")).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load main character
        self.character = Cutout("main_character",
                              os.path.join(CHARACTERS_DIR, "main_character.png"),
                              860, CHARACTER_Y)
        
        # Movement system
        self.target_x = self.character.rect.x
        self.is_moving = False
        self.current_speed = 0
        
        # Initialize systems
        self.message_log = MessageLog()
        self.inventory_bar = InventoryBar()
        self.dialog_box = DialogBox()
        
        # Initialize cutouts and objects
        self.cutouts = []
        self.interactive_objects = []
        self.inventory = []
        self.revealed_shards = set()  # Track which shards have been revealed
        
        # Create bookshelf
        name, x, y, width, height, is_movable, desc = SCENE_OBJECTS[0]
        self.bookshelf = InteractiveObject(name,
                                         os.path.join(ASSETS_DIR, f"{name}.png"),
                                         x, y, width, height, is_movable)
        self.interactive_objects.append(self.bookshelf)
        
        # Create mirror shard (initially hidden)
        name, x, y, description = MIRROR_POSITIONS[0]
        self.shard = Cutout(name,
                           os.path.join(ASSETS_DIR, f"{name}.png"),
                           x, y)
        if self.shard.image:
            self.shard.image = pygame.transform.scale(self.shard.image, SHARD_SIZE)
            self.shard.rect.size = SHARD_SIZE
        self.cutouts.append(self.shard)

    def check_shard_reveal(self, bookshelf):
        """Check if moving a bookshelf should reveal a shard"""
        if bookshelf == self.bookshelf and "mirror_shard" not in self.revealed_shards:
            self.revealed_shards.add("mirror_shard")
            return "mirror_shard", MIRROR_POSITIONS[0][3]
        return None, None

    def update(self):
        self.message_log.update()
        self.dialog_box.update()
        
        if self.is_moving:
            current_x = self.character.rect.x
            distance = abs(current_x - self.target_x)
            
            if distance <= CHARACTER_STOP_THRESHOLD:
                self.is_moving = False
                self.current_speed = 0
                self.character.rect.x = self.target_x
            else:
                target_speed = min(CHARACTER_SPEED, distance / 10)
                if self.target_x > current_x:
                    self.current_speed = min(self.current_speed + CHARACTER_ACCELERATION, target_speed)
                else:
                    self.current_speed = max(self.current_speed - CHARACTER_ACCELERATION, -target_speed)
                
                new_x = current_x + self.current_speed
                new_x = max(0, min(new_x, SCREEN_WIDTH - self.character.rect.width))
                self.character.rect.x = new_x

    def render(self, screen):
        screen.blit(self.background, (0, 0))
        self.character.render(screen)
        
        # Draw interactive objects (bookshelf)
        self.bookshelf.render(screen)
        
        # Draw only revealed shards
        for cutout in self.cutouts:
            if "shard" not in cutout.name or cutout.name in self.revealed_shards:
                cutout.render(screen)
        
        self.dialog_box.render(screen)
        self.inventory_bar.render(screen)
        self.message_log.render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                clicked_item = self.inventory_bar.handle_click(event.pos)
                if clicked_item:
                    self.message_log.add_message(f"Examining {clicked_item.replace('_', ' ').title()}")
                    return
                
                # Handle character movement
                click_x = event.pos[0]
                if abs(click_x - self.character.rect.x) > CHARACTER_IDLE_RANGE:
                    self.target_x = max(0, min(click_x, SCREEN_WIDTH - self.character.rect.width))
                    self.is_moving = True
                
                # Check bookshelf interaction
                char_center_x = self.character.rect.centerx
                if self.bookshelf.is_clicked(event.pos):
                    # Check if character is close enough to interact
                    if abs(char_center_x - self.bookshelf.rect.centerx) < 150:  # Interaction range
                        if self.bookshelf.move():  # Try to move the bookshelf
                            # Check if this reveals a shard
                            shard_name, description = self.check_shard_reveal(self.bookshelf)
                            if shard_name:
                                self.dialog_box.show_text(description)
                    else:
                        self.dialog_box.show_text("I need to get closer to move that...")
                
                # Handle shard collection (only if revealed)
                for cutout in self.cutouts:
                    if cutout.is_clicked(event.pos) and cutout.name in self.revealed_shards:
                        if cutout.handle_click():
                            if "shard" in cutout.name:
                                self.inventory.append(cutout.name)
                                self.inventory_bar.add_item(cutout.name, 
                                                          os.path.join(ASSETS_DIR, f"{cutout.name}.png"))
                                
                                if len(self.inventory) == 3:
                                    self.dialog_box.show_text("The mirror begins to form... You sense its ancient power stirring.")
        
        elif event.type == pygame.MOUSEMOTION:
            self.inventory_bar.handle_hover(event.pos) 