import pygame

class StyledPanel:
    def __init__(self, rect, title="", color=(40, 40, 40), border_color=(100, 100, 100)):
        self.rect = rect
        self.title = title
        self.color = color
        self.border_color = border_color
        # Scale font sizes based on panel size
        self.font = pygame.font.Font(None, max(20, int(rect.height * 0.05)))
        self.title_font = pygame.font.Font(None, max(24, int(rect.height * 0.06)))
        self.border_radius = max(5, int(rect.height * 0.02))
        self.border_width = 2
        
    def cleanup(self) -> None:
        """Clean up panel resources."""
        self.font = None
        self.title_font = None
        
    def draw(self, screen):
        # Draw main panel with rounded corners
        pygame.draw.rect(screen, self.color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
        
        # Draw title if exists
        if self.title:
            title_text = self.title_font.render(self.title, True, (200, 200, 200))
            title_rect = title_text.get_rect(midtop=(self.rect.centerx, self.rect.y + 10))
            screen.blit(title_text, title_rect)

class InventoryPanel(StyledPanel):
    def __init__(self, rect):
        super().__init__(rect, "Inventory", (30, 30, 35), (80, 80, 85))
        self.items = []
        self.slot_size = 60  # Size of each inventory slot
        self.slots_per_row = 2  # Number of slots per row
        self.slot_padding = 10  # Padding between slots
        self.scroll_offset = 0
        self.dragged_item = None
        self.dragged_item_original_pos = None
        self.dragged_item_index = None
        self.font = pygame.font.Font(None, 24)
        # Map of item names to their image paths
        self.item_paths = {
            "scroll_whole": "scroll/scroll_whole.png",
            "scroll_fragment": "scroll/scroll_fragment.png",
            "candle_unlit": "candles/candle_unlit.png",
            "candle_lit": "candles/candle_lit.png",
            "jar_of_oil": "jar/jar_of_oil.png",
            "matches": "firetools/matches.png",
            "cloth_oil": "cloth_oil.png",
            "feather_duster": "feather_duster.png",
            "puzzle_box": "puzzle_box.png",
            "sacred_cleaning_cloth": "usable/sacred_cleaning_cloth.png"
        }
        
    def cleanup(self) -> None:
        """Clean up inventory resources."""
        super().cleanup()
        self.items.clear()
        self.dragged_item = None
        self.dragged_item_original_pos = None
        self.dragged_item_index = None
        self.scroll_offset = 0
        
    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)
            
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            
    def get_slot_rect(self, index):
        """Get the rectangle for a specific inventory slot"""
        row = index // self.slots_per_row
        col = index % self.slots_per_row
        
        x = self.rect.x + self.slot_padding + (col * (self.slot_size + self.slot_padding))
        y = self.rect.y + 50 + (row * (self.slot_size + self.slot_padding)) - self.scroll_offset
        
        return pygame.Rect(x, y, self.slot_size, self.slot_size)
        
    def get_item_at_pos(self, pos):
        """Get the item and index at a specific position"""
        for i, item in enumerate(self.items):
            slot_rect = self.get_slot_rect(i)
            if slot_rect.collidepoint(pos):
                return item, i
        return None, None
        
    def start_drag(self, pos):
        """Start dragging an item"""
        item, index = self.get_item_at_pos(pos)
        if item:
            self.dragged_item = item
            self.dragged_item_original_pos = pos
            self.dragged_item_index = index
            
    def update_drag(self, pos):
        """Update the position of the dragged item"""
        if self.dragged_item:
            self.dragged_item_pos = pos
            
    def end_drag(self, pos):
        """End dragging an item and handle the result"""
        if self.dragged_item:
            target_item, target_index = self.get_item_at_pos(pos)
            
            # If dropped on another item, try to combine them
            if target_item and target_index != self.dragged_item_index:
                return self.dragged_item, target_item
                
            self.dragged_item = None
            self.dragged_item_original_pos = None
            self.dragged_item_index = None
            return None, None
            
    def _get_item_image_path(self, item_name):
        """Get the correct image path for an item"""
        if item_name in self.item_paths:
            return f"assets/images/objects/items/{self.item_paths[item_name]}"
        return None
            
    def draw(self, screen):
        super().draw(screen)
        
        # Draw inventory slots
        for i in range(len(self.items)):
            slot_rect = self.get_slot_rect(i)
            if slot_rect.bottom > self.rect.bottom - 10:
                continue
                
            # Draw slot background
            pygame.draw.rect(screen, (50, 50, 55), slot_rect, border_radius=5)
            pygame.draw.rect(screen, (100, 100, 105), slot_rect, 1, border_radius=5)
            
            # Draw item in slot if it's not being dragged
            if i != self.dragged_item_index:
                item = self.items[i]
                # Load and scale item image
                try:
                    image_path = self._get_item_image_path(item)
                    if image_path:
                        item_image = pygame.image.load(image_path).convert_alpha()
                        # Scale image to fit slot while maintaining aspect ratio
                        img_rect = item_image.get_rect()
                        scale = min(self.slot_size * 0.8 / img_rect.width, 
                                  self.slot_size * 0.8 / img_rect.height)
                        new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
                        item_image = pygame.transform.scale(item_image, new_size)
                        
                        # Center image in slot
                        img_rect = item_image.get_rect(center=slot_rect.center)
                        screen.blit(item_image, img_rect)
                    else:
                        # If no image path found, draw item name as text
                        text = self.font.render(item, True, (200, 200, 200))
                        text_rect = text.get_rect(center=slot_rect.center)
                        screen.blit(text, text_rect)
                except Exception as e:
                    print(f"Error loading image for {item}: {e}")
                    # If image loading fails, draw item name as text
                    text = self.font.render(item, True, (200, 200, 200))
                    text_rect = text.get_rect(center=slot_rect.center)
                    screen.blit(text, text_rect)
                    
        # Draw dragged item
        if self.dragged_item:
            try:
                image_path = self._get_item_image_path(self.dragged_item)
                if image_path:
                    item_image = pygame.image.load(image_path).convert_alpha()
                    # Scale image for dragging (slightly larger than slot)
                    img_rect = item_image.get_rect()
                    scale = min(self.slot_size * 0.9 / img_rect.width,
                              self.slot_size * 0.9 / img_rect.height)
                    new_size = (int(img_rect.width * scale), int(img_rect.height * scale))
                    item_image = pygame.transform.scale(item_image, new_size)
                    
                    # Draw at mouse position
                    img_rect = item_image.get_rect(center=pygame.mouse.get_pos())
                    screen.blit(item_image, img_rect)
                    
                    # Add subtle glow effect
                    glow_surface = pygame.Surface(img_rect.size, pygame.SRCALPHA)
                    pygame.draw.rect(glow_surface, (255, 255, 255, 50),
                                   glow_surface.get_rect(), border_radius=5)
                    screen.blit(glow_surface, img_rect)
                else:
                    # If no image path found, draw item name as text
                    text = self.font.render(self.dragged_item, True, (200, 200, 200))
                    text_rect = text.get_rect(center=pygame.mouse.get_pos())
                    screen.blit(text, text_rect)
            except Exception as e:
                print(f"Error loading dragged image for {self.dragged_item}: {e}")
                # If image loading fails, draw item name as text
                text = self.font.render(self.dragged_item, True, (200, 200, 200))
                text_rect = text.get_rect(center=pygame.mouse.get_pos())
                screen.blit(text, text_rect)

    def update(self, delta_time: float) -> None:
        """Update inventory state with the given time delta."""
        # Handle any time-based animations or effects
        if self.dragged_item:
            # Update dragged item position if needed
            mouse_pos = pygame.mouse.get_pos()
            self.dragged_item_pos = mouse_pos
            
        # Update scroll position if needed (for future scrolling implementation)
        pass

class TextPanel(StyledPanel):
    def __init__(self, rect):
        super().__init__(rect, "Dialog", (30, 30, 35), (80, 80, 85))
        self.text = ""
        self.text_padding = 20
        self.line_height = max(25, int(rect.height * 0.2))
        
    def cleanup(self) -> None:
        """Clean up text panel resources."""
        super().cleanup()
        self.text = ""
        
    def set_text(self, text):
        self.text = text
        
    def update(self, delta_time: float) -> None:
        """Update text panel state with the given time delta."""
        pass  # No time-based updates needed for text panel
        
    def draw(self, screen):
        super().draw(screen)
        
        if self.text:
            # Split text into lines that fit the panel
            words = self.text.split()
            lines = []
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.font.render(test_line, True, (200, 200, 200))
                
                if test_surface.get_width() <= self.rect.width - (2 * self.text_padding):
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            
            if current_line:
                lines.append(' '.join(current_line))
            
            # Draw each line with proper spacing
            for i, line in enumerate(lines):
                y_pos = self.rect.y + 50 + (i * self.line_height)
                if y_pos + self.line_height > self.rect.bottom - 10:
                    break
                    
                line_text = self.font.render(line, True, (200, 200, 200))
                text_rect = line_text.get_rect(topleft=(self.rect.x + self.text_padding, y_pos))
                screen.blit(line_text, text_rect)

class OptionsButton:
    def __init__(self, rect):
        self.rect = rect
        self.font = pygame.font.Font(None, max(20, int(rect.height * 0.5)))
        self.color = (50, 50, 55)
        self.hover_color = (70, 70, 75)
        self.border_color = (100, 100, 105)
        self.is_hovered = False
        self.border_radius = max(5, int(rect.height * 0.2))
        
    def cleanup(self) -> None:
        """Clean up button resources."""
        pass  # No resources to clean up
        
    def update(self, delta_time: float) -> None:
        """Update button state."""
        pass  # No time-based updates needed
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered:
            return True
        return False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=self.border_radius)
        
        text = self.font.render("Options", True, (200, 200, 200))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect) 