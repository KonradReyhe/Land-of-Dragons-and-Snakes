import pygame
from typing import Dict, List, Optional, Tuple
import random
import time
from ui.ui_manager import UIManager
from game.character import Character
from game.inventory import Inventory
from game.objects import InteractiveObject, FurnitureObject, CreatureObject, ItemObject
from game.background_manager import BackgroundManager
from scenes.base_scene import BaseScene

class Scene1(BaseScene):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Game state initialization
        self.house_state_score = 0
        self.max_furniture = 4
        self.cleansed_objects = []
        self.previous_house_state = 0
        
        # Scene state flags
        self.scroll_collected = False
        self.scroll_read = False
        self.scroll_clicks = 0
        self.door_visible = False
        self.mirror_ready = False
        self.puzzle_box_opened = False
        self.serpent_removed = False
        self.spider_removed = False
        self.helped_npc = False
        self.received_purification_item = False
        
        # Hidden item states
        self.drawer_opened = False
        self.altar_clicks = 0
        self.bookshelf_moved = False
        self.table_inspected = False
        self.scroll_dust_cleared = False
        
        # World progression tracking
        self.bell_tower_boaz_restored = False
        self.bell_tower_jachin_restored = False
        self.marketplace_visited = False
        self.houses_cleansed = {
            "lost_son": False,
            "scholars_lab": False,
            "dying_garden": False
        }
        self.npcs_helped = {
            "justifier": False,
            "performer": False,
            "mother": False,
            "craftsman": False,
            "alchemist": False,
            "gardener": False
        }
        
        # Armor of God progression
        self.armor_pieces = {
            "belt_of_truth": False,
            "breastplate_of_righteousness": False,
            "helmet_of_salvation": False,
            "shoes_of_peace": False,
            "shield_of_faith": False,
            "sword_of_spirit": False
        }
        
        # Creature timing
        self.last_creature_appearance = time.time()
        self.creature_visible = False
        self.creature_duration = random.uniform(2, 4)
        self.creature_cooldown = random.uniform(20, 40)
        
        # Track selected item from inventory
        self.selected_item: Optional[ItemObject] = None
        
        # Track active creature
        self.active_creature: Optional[CreatureObject] = None
        
        # Door and glow effect positions
        self.door_position = (1700, 620)
        self.glow_position = (1650, 600)
        
        # Door state
        self.door_alpha = 0
        self.door_fade_speed = 5
        
        # Initialize the scene
        self.initialize()
        
    def _load_resources(self) -> None:
        """Load scene-specific resources"""
        # Initialize background manager
        self.background_manager = BackgroundManager(self.screen_width, self.screen_height)
        self.background_manager.set_background("home", "corrupted")
        
        # Initialize character
        self.character = Character(
            self.screen_width // 2,
            int(self.screen_height * 0.8),
            self.screen_width,
            self.screen_height
        )
        
        # Initialize inventory
        self.inventory = Inventory()
        
        # Initialize door objects
        self.door = InteractiveObject(
            "door",
            self.door_position,
            "assets/images/objects/doors/door_glowing_open.png"
        )
        
        self.door_glow = InteractiveObject(
            "door_glow",
            self.glow_position,
            "assets/images/objects/doors/door_glow_effect.png"
        )
        
        # Set initial alpha to 0 (invisible)
        self.door.image.set_alpha(0)
        self.door_glow.image.set_alpha(0)
        
        # Add door and glow to layer 1 (behind furniture)
        self.add_object(self.door_glow, 1)
        self.add_object(self.door, 1)
        
        self._scale_door_objects()
        self._initialize_objects()
        
    def _setup_ui(self) -> None:
        """Setup UI elements"""
        self.ui_manager = UIManager(self.screen_width, self.screen_height)
        self.ui_manager.set_ui_visibility(True, True, True)
        self.ui_manager.set_text("You awaken in a room thick with shadows. The air feels heavy with memories...")
        
    def _initialize_objects(self) -> None:
        """Initialize all objects in the scene"""
        # Initialize layers if they don't exist
        for i in range(5):
            if i not in self.layers:
                self.layers[i] = []
        
        # Layer 0: Background elements (furthest back)
        self.layers[0].append(
            FurnitureObject(
                "wall",
                "neutral",
                (0, 0),
                "assets/images/objects/furniture/wall/wall.png"
            )
        )
        
        # Layer 1: Main furniture and interactive objects
        self.layers[1].extend([
            FurnitureObject(
                "table",
                "corrupted",
                (400, 500),
                "assets/images/objects/furniture/table/table_corrupted.png"
            ),
            FurnitureObject(
                "chair",
                "corrupted",
                (450, 600),
                "assets/images/objects/furniture/chair/chair_corrupted.png"
            ),
            InteractiveObject(
                "door",
                (800, 400),
                "assets/images/objects/doors/door.png"
            ),
            InteractiveObject(
                "door_glow",
                (800, 400),
                "assets/images/objects/doors/door_glow.png"
            )
        ])
        
        # Layer 2: Items and collectibles
        self.layers[2].extend([
            ItemObject(
                "scroll",
                (420, 450),
                "assets/images/objects/items/scroll/scroll_whole.png"
            ),
            ItemObject(
                "key",
                (500, 550),
                "assets/images/objects/items/keys/key.png"
            )
        ])
        
        # Layer 3: Creatures and NPCs
        self.layers[3].extend([
            CreatureObject(
                "shadow_serpent",
                (780, 650),
                "assets/images/objects/creatures/shadow_serpent/shadow_serpent.png",
                self.screen_width,
                self.screen_height
            ),
            CreatureObject(
                "large_black_spider",
                (120, 640),
                "assets/images/objects/creatures/spider/large_black_spider.png",
                self.screen_width,
                self.screen_height
            )
        ])
        
        # Layer 4: Foreground elements (closest to camera)
        self.layers[4].append(
            FurnitureObject(
                "carpet",
                "corrupted",
                (300, 550),
                "assets/images/objects/furniture/carpet/carpet_corrupted.png"
            )
        )
        
        # Scale items appropriately
        self._scale_items()
        
    def _scale_items(self) -> None:
        """Scale all items to appropriate sizes"""
        for layer_id in self.layers:
            for obj in self.layers[layer_id]:
                if isinstance(obj, (FurnitureObject, ItemObject)):
                    # Scale based on screen size
                    scale_factor = min(
                        self.screen_width / 1920,
                        self.screen_height / 1080
                    )
                    obj.scale(scale_factor)
                elif isinstance(obj, CreatureObject):
                    # Scale creatures slightly smaller
                    scale_factor = min(
                        self.screen_width / 1920,
                        self.screen_height / 1080
                    ) * 0.8
                    obj.scale(scale_factor)
                    
    def _scale_door_objects(self):
        """Scale door and glow effect to appropriate sizes"""
        # Scale door to about 1/3 of screen height
        door_height = self.screen_height // 3
        door_scale = door_height / self.door.image.get_height()
        door_width = int(self.door.image.get_width() * door_scale)
        self.door.image = pygame.transform.scale(
            self.door.image, 
            (door_width, door_height)
        )
        self.door.rect = self.door.image.get_rect(center=self.door_position)
        
        # Scale glow slightly larger than door
        glow_scale = door_scale * 1.2
        glow_width = int(self.door_glow.image.get_width() * glow_scale)
        glow_height = int(self.door_glow.image.get_height() * glow_scale)
        self.door_glow.image = pygame.transform.scale(
            self.door_glow.image,
            (glow_width, glow_height)
        )
        self.door_glow.rect = self.door_glow.image.get_rect(center=self.glow_position)
        
    def _show_door(self):
        """Show the door with a fade-in effect"""
        self.door_visible = True
        self.door.visible = True
        self.door_glow.visible = True
        self.door_alpha = 0
        
        # Set initial alpha for fade-in
        self.door.image.set_alpha(0)
        self.door_glow.image.set_alpha(0)
        
        # Update narrative
        self.ui_manager.set_text("A door appears in the wall, glowing with divine light...")
        
    def _handle_door_click(self):
        """Handle door click to transition to Scene 2"""
        if self.door_visible and self.door.rect.collidepoint(pygame.mouse.get_pos()):
            self.ui_manager.set_text("The door opens, revealing the path to the marketplace...")
            # TODO: Implement scene transition
            return True
        return False
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle pygame events with hover effects"""
        # Handle UI events first
        if self.ui_manager:
            self.ui_manager.handle_event(event)
            
        # Handle character movement and object interaction
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check if clicking on objects (check layers in reverse order)
            for layer in range(4, -1, -1):  # 4 to 0
                if layer in self.layers:
                    for obj in self.layers[layer]:
                        if obj.rect.collidepoint(mouse_pos):
                            self._handle_object_click(obj, mouse_pos)
                            return
                            
            # Check for door click
            if self._handle_door_click():
                return
            
            # If no object clicked, move character
            self.character.set_target(mouse_pos)
            
        # Handle hover effects
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for layer in self.layers.values():
                for obj in layer:
                    if isinstance(obj, ItemObject) and not obj.collected:
                        obj.update_hover(mouse_pos)
                        
    def _handle_object_click(self, obj: InteractiveObject, mouse_pos: Tuple[int, int]) -> None:
        """Handle clicking on scene objects"""
        if isinstance(obj, FurnitureObject):
            if obj.name == "altar":
                self.altar_clicks += 1
                if self.altar_clicks == 2:
                    # Reveal matches behind altar
                    for item in self.layers[2]:
                        if item.name == "matches":
                            item.visible = True
                            self.ui_manager.set_text("You found matches hidden behind the altar.")
                            
            elif obj.name == "drawer" and not self.drawer_opened:
                self.drawer_opened = True
                # Reveal candle and puzzle box in drawer
                for item in self.layers[2]:
                    if item.name in ["candle_unlit", "puzzle_box"]:
                        item.visible = True
                self.ui_manager.set_text("You opened the drawer and found some items.")
                
            elif obj.name == "table" and not self.table_inspected:
                self.table_inspected = True
                # Reveal jar of oil under table
                for item in self.layers[2]:
                    if item.name == "jar_of_oil":
                        item.visible = True
                self.ui_manager.set_text("You found a jar of oil under the table.")
                
            if self.ui_manager.inventory_panel.dragged_item:
                # Handle dropping dragged item on furniture
                dragged_item = self.ui_manager.inventory_panel.dragged_item
                if self._can_use_item_on_furniture(dragged_item, obj):
                    self._use_item_on_furniture(dragged_item, obj)
                else:
                    if obj.name == "mirror":
                        self.ui_manager.set_text("The mirror's surface ripples like dark water. Not yet... something else must be done first.")
                    else:
                        self.ui_manager.set_text("The corruption resists your attempt. Perhaps another approach is needed...")
                self.ui_manager.inventory_panel.end_drag(mouse_pos)
            else:
                # Descriptive text based on furniture state
                if obj.state == "corrupted":
                    messages = {
                        "bed": "The bed is stained with dark memories. Something skitters in its shadow...",
                        "table": "Ancient wood, scarred by time. Remnants of ritual tools remain.",
                        "mirror": "Your reflection is distorted, barely visible through the grime.",
                        "altar": "Once sacred, now defiled. The corruption runs deep.",
                        "drawer": "The drawer emanates unease. Something serpentine moves within..."
                    }
                    self.ui_manager.set_text(messages.get(obj.name, f"The {obj.name} bears the weight of corruption."))
                elif obj.state == "cleansed":
                    messages = {
                        "bed": "The bed radiates peace now, memories gentled.",
                        "table": "The table stands proud again, its purpose restored.",
                        "mirror": "The mirror gleams with truth, waiting for the final revelation.",
                        "altar": "Sacred energy hums within the restored altar.",
                        "drawer": "The drawer rests easy, its shadows banished."
                    }
                    self.ui_manager.set_text(messages.get(obj.name, f"The {obj.name} has been restored to its true purpose."))
                
        elif isinstance(obj, ItemObject):
            if not obj.collected and obj.visible:  # Only collect if item is visible
                if self.inventory.add_item(obj.name):
                    obj.collected = True
                    self.ui_manager.inventory_panel.add_item(obj.name)
                    # Narrative messages for collecting items
                    messages = {
                        "scroll_whole": "An ancient scroll, its edges worn by countless hands...",
                        "scroll_fragment": "A torn piece of parchment, bearing cryptic symbols.",
                        "candle_unlit": "A ritual candle, waiting for sacred flame.",
                        "matches": "These matches feel unusually warm to the touch.",
                        "jar_of_oil": "Holy oil, its surface shimmering with golden light.",
                        "cloth_oil": "A simple cloth, but it yearns for purpose.",
                        "feather_duster": "A feather duster, oddly pristine amidst the decay.",
                        "puzzle_box": "An intricate box, its mechanisms singing with secrets."
                    }
                    self.ui_manager.set_text(messages.get(obj.name, "The item resonates with hidden meaning."))
                else:
                    self.ui_manager.set_text("Your spirit is burdened... you cannot carry more.")
                    
        elif isinstance(obj, CreatureObject):
            messages = {
                "shadow_serpent": "A serpent of shadow writhes at the edge of vision...",
                "large_black_spider": "Eight eyes glitter in the darkness, watching... always watching..."
            }
            self.ui_manager.set_text(messages.get(obj.name, "A creature of corruption lurks nearby."))
            
    def _read_fathers_scroll(self):
        """Handle the reading of the father's scroll"""
        self.scroll_read = True
        self.ui_manager.set_text(
            "Do not forget the path. The darkness has spread, but light remains. "
            "Help others before cleansing your own house. Only then will the door open."
        )
        # Show the door after reading scroll
        self._show_door()
        
    def _prepare_marketplace_transition(self):
        """Prepare for transition to Scene 2: The Blind Marketplace"""
        # Add door to scene
        door = FurnitureObject(
            "door",
            "locked",
            (self.screen_width - 200, self.screen_height // 2),
            "assets/images/objects/furniture/door/door_locked.png"
        )
        self.add_object(door, 1)
        
        # Add transition items
        market_key = ItemObject(
            "market_key",
            (self.screen_width - 250, self.screen_height // 2 + 50),
            "assets/images/objects/items/keys/market_key.png"
        )
        self.add_object(market_key, 2)
        
        # Update narrative
        self.ui_manager.set_text("""
        A door appears in the wall, leading to the marketplace. 
        A key rests nearby, its surface etched with symbols of commerce and truth.
        The scroll's words echo in your mind...
        """)
        
    def _can_use_item_on_furniture(self, item: ItemObject, furniture: FurnitureObject) -> bool:
        """Check if an item can be used on the furniture"""
        if furniture.state not in ["corrupted", "dirty"]:
            return False
            
        # Check for cleansing prerequisites
        if item.name == "sacred_cleaning_cloth":
            if not (self.scroll_read and self.helped_npc and self.received_purification_item):
                self.ui_manager.set_text("""
                The corruption resists. You must first:
                1. Understand your father's message
                2. Help others in the marketplace
                3. Receive the purification item
                """)
                return False
                
            # Mirror requires special conditions
            if furniture.name == "mirror":
                if not self.puzzle_box_opened:
                    self.ui_manager.set_text("The mirror resists. Something else must be done first...")
                    return False
            return True
            
        # Special cases for specific furniture
        if furniture.name == "altar" and item.name == "scroll_whole":
            return True
            
        if furniture.name == "drawer" and item.name == "scroll_fragment":
            return True
            
        return False
        
    def _use_item_on_furniture(self, item: ItemObject, furniture: FurnitureObject) -> None:
        """Use an item on a piece of furniture"""
        if item.name == "sacred_cleaning_cloth":
            self._cleanse_furniture(furniture)
            self.inventory.remove_item(item.name)
            self.ui_manager.inventory_panel.remove_item(item.name)
            
        elif furniture.name == "altar" and item.name == "scroll_whole":
            # Special handling for placing scroll on altar
            self.ui_manager.set_text("The scroll begins to glow with ancient power...")
            self.inventory.remove_item(item.name)
            self.ui_manager.inventory_panel.remove_item(item.name)
            
        elif furniture.name == "drawer" and item.name == "scroll_fragment":
            # Special handling for using scroll fragment on drawer
            self.ui_manager.set_text("The drawer mechanism clicks and shifts...")
            self.inventory.remove_item(item.name)
            self.ui_manager.inventory_panel.remove_item(item.name)
        
    def _cleanse_furniture(self, furniture: FurnitureObject) -> None:
        """Cleanse a piece of furniture and update its state"""
        # Update furniture state and image
        if furniture.name == "mirror":
            furniture.state = "purified"
            furniture.image = pygame.image.load(
                "assets/images/objects/furniture/mirror/mirror_purified.png"
            ).convert_alpha()
        else:
            furniture.state = "cleansed"
            furniture.image = pygame.image.load(
                f"assets/images/objects/furniture/{furniture.name}/{furniture.name}_cleansed.png"
            ).convert_alpha()
            
        # Scale the new image to match previous size
        if furniture.name == "bed":
            target_width = 200
        elif furniture.name == "table":
            target_width = 190
        elif furniture.name == "mirror":
            target_width = 150
        elif furniture.name == "altar":
            target_width = 220
        elif furniture.name == "drawer":
            target_width = int(furniture.image.get_width() * 0.95)
        else:
            target_width = 180
            
        scale_factor = target_width / furniture.image.get_width()
        new_size = (int(furniture.image.get_width() * scale_factor),
                   int(furniture.image.get_height() * scale_factor))
        furniture.image = pygame.transform.scale(furniture.image, new_size)
        furniture.rect = furniture.image.get_rect(center=furniture.position)
            
        # Add glow effect for cleansed furniture
        glow_surface = pygame.Surface(furniture.image.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, (255, 255, 200, 30), 
                        glow_surface.get_rect(), border_radius=5)
        furniture.image.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)
            
        # Update house state
        self.house_state_score += 1
        self.cleansed_objects.append(furniture.name)
        
        # Update UI text with narrative messages
        cleansing_messages = {
            "bed": "The bed shudders as darkness seeps away, leaving peace in its wake...",
            "table": "Ancient stains fade from the wood as it remembers its purpose...",
            "mirror": "The mirror's surface clears, revealing truths long hidden...",
            "altar": "Divine energy surges through the altar, burning away corruption...",
            "drawer": "The drawer's shadows scatter like startled serpents..."
        }
        self.ui_manager.set_text(cleansing_messages.get(furniture.name, "The corruption fades, leaving clarity in its wake..."))
        
        # Check for house state message
        if self.house_state_score >= self.max_furniture:
            self.ui_manager.set_text("The room exhales deeply, as if awakening from a long nightmare...")
            
        # Handle creature removal with narrative
        if furniture.name == "bed" and self.layers[3][0] in self.layers[3]:
            self.ui_manager.set_text("The spider's web unravels, its darkness dissolving into memory...")
            self.layers[3][0].fade_out()
            self.spider_removed = True
        elif furniture.name == "drawer" and self.layers[3][1] in self.layers[3]:
            self.ui_manager.set_text("The serpent writhes and fades, its coils unwinding into nothingness...")
            self.layers[3][1].fade_out()
            self.serpent_removed = True
            
        # Check for mirror activation
        if self.house_state_score >= self.max_furniture and self.puzzle_box_opened:
            self.mirror_ready = True
            
    def _check_house_state(self) -> None:
        """Check and update house state based on cleansed objects"""
        # Calculate new state
        if self.house_state_score >= self.max_furniture:
            new_state = "cleansed"
        elif self.house_state_score > 0:
            new_state = "neutral"
        else:
            new_state = "corrupted"
            
        # Only trigger transition if state changed
        if self.house_state_score != self.previous_house_state:
            self.background_manager.set_background("home", new_state)
            self.previous_house_state = self.house_state_score
            
    def update(self) -> None:
        """Update scene state"""
        # Calculate delta time (assuming 60 FPS)
        delta_time = 1/60
        
        # Update background
        self.background_manager.update(delta_time)
        
        # Update character
        self.character.update()
        
        # Update UI
        if self.ui_manager:
            self.ui_manager.update(delta_time)
            
        # Update all objects by layer
        for layer_id in self.layers:
            for obj in self.layers[layer_id]:
                if hasattr(obj, 'update'):
                    obj.update(delta_time)
                    
        # Check house state for background changes
        self._check_house_state()
        
        # Update door fade effect
        if self.door_visible and self.door.image.get_alpha() < 255:
            new_alpha = min(255, self.door.image.get_alpha() + self.door_fade_speed)
            self.door.image.set_alpha(new_alpha)
            self.door_glow.image.set_alpha(new_alpha)
            
        # Update creature visibility
        current_time = time.time()
        if not self.creature_visible:
            if current_time - self.last_creature_appearance > self.creature_cooldown:
                # Time to show a creature
                self.creature_visible = True
                self.last_creature_appearance = current_time
                # Choose which creature to show
                if random.random() < 0.5:
                    self.active_creature = self.layers[3][0]
                else:
                    self.active_creature = self.layers[3][1]
                    
                if self.active_creature:
                    self.active_creature.appear()
        else:
            if current_time - self.last_creature_appearance > self.creature_duration:
                # Time to hide the creature
                self.creature_visible = False
                self.last_creature_appearance = current_time
                if self.active_creature:
                    self.active_creature.fade_out()
                self.active_creature = None
                # Set new random durations
                self.creature_duration = random.uniform(2, 4)
                self.creature_cooldown = random.uniform(20, 40)
        
    def draw(self) -> None:
        """Draw the scene"""
        # Fill screen with black to clear previous frame
        self.screen.fill((0, 0, 0))
        
        # Draw background
        self.background_manager.draw(self.screen)
        
        # Draw all objects by layer
        for layer in range(5):  # 0 to 4
            if layer in self.layers:
                for obj in self.layers[layer]:
                    if hasattr(obj, 'visible') and not obj.visible:
                        continue
                    self.screen.blit(obj.image, obj.rect)
        
        # Draw character
        self.character.draw(self.screen)
        
        # Draw UI elements last
        self.ui_manager.draw(self.screen)
        
        # Draw selected item cursor if applicable
        if self.selected_item:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.selected_item.image, mouse_pos)
        
        # Draw door and glow with proper alpha
        if self.door_visible:
            self.screen.blit(self.door_glow.image, self.door_glow.rect)
            self.screen.blit(self.door.image, self.door.rect)
        
        # Draw door if visible
        if self.door_visible:
            # Draw door cutout with optional glow animation
            pass  # Door drawing logic will be implemented separately 

    def cleanup(self):
        """Clean up scene resources"""
        super().cleanup()
        # Clean up additional resources
        self.background_manager = None
        self.ui_manager = None
        self.character = None
        self.inventory = None
        self.layers.clear()
        self.door = None
        self.door_glow = None 