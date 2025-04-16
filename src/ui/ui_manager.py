import pygame
from ui.components import InventoryPanel, TextPanel, OptionsButton

class UIManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calculate UI element sizes based on screen size
        panel_width = int(screen_width * 0.15)  # 15% of screen width
        panel_height = int(screen_height * 0.3)  # 30% of screen height
        text_panel_height = int(screen_height * 0.12)  # 12% of screen height
        button_width = int(screen_width * 0.06)  # 6% of screen width
        button_height = int(screen_height * 0.03)  # 3% of screen height
        
        # Create UI panels with proper positioning
        # Inventory panel on the left side
        self.inventory_panel = InventoryPanel(pygame.Rect(
            20,  # Left margin
            20,  # Top margin
            panel_width,
            panel_height
        ))
        
        # Text panel at the top middle
        text_panel_width = int(screen_width * 0.4)  # 40% of screen width
        self.textbox = TextPanel(pygame.Rect(
            (screen_width - text_panel_width) // 2,  # Center horizontally
            20,  # Top margin
            text_panel_width,
            text_panel_height
        ))
        
        # Options button in top-right corner
        self.options_button = OptionsButton(pygame.Rect(
            screen_width - button_width - 20,  # Right margin
            20,  # Top margin
            button_width,
            button_height
        ))
        
        # Visibility flags
        self.inventory_visible = False
        self.textbox_visible = False
        self.options_visible = False
        
        # UI elements
        self.inventory_items = []
        self.current_text = ""
        
        # Default visibility settings for different scenes
        self.scene_visibility = {
            "none": {"inventory": False, "textbox": False, "options": False},
            "start": {"inventory": False, "textbox": False, "options": False},
            "scene1": {"inventory": True, "textbox": True, "options": True},
            "default": {"inventory": True, "textbox": True, "options": True}
        }

    def set_scene(self, scene_name):
        """Set UI visibility based on the current scene"""
        visibility = self.scene_visibility.get(scene_name, self.scene_visibility["default"])
        self.set_ui_visibility(
            show_inventory=visibility["inventory"],
            show_textbox=visibility["textbox"],
            show_options=visibility["options"]
        )
        
        # Set initial text for specific scenes
        if scene_name == "scene1":
            self.set_text("Welcome home traveler!")

    def set_ui_visibility(self, show_inventory=False, show_textbox=False, show_options=False):
        self.inventory_visible = show_inventory
        self.textbox_visible = show_textbox
        self.options_visible = show_options
        
    def handle_event(self, event):
        # Handle mouse events for UI elements
        if event.type == pygame.MOUSEMOTION:
            # Update hover states
            if self.options_visible:
                self.options_button.handle_event(event)
            if self.inventory_visible:
                # Handle inventory hover events
                if self.inventory_panel.dragged_item:
                    self.inventory_panel.update_drag(event.pos)
                    return True  # Only block events when dragging items
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.options_visible and self.options_button.rect.collidepoint(event.pos):
                self.options_button.handle_event(event)
                return True  # Block event when clicking options button
                
            if self.inventory_visible and self.inventory_panel.rect.collidepoint(event.pos):
                self.inventory_panel.start_drag(event.pos)
                return True  # Block event when clicking inventory
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.inventory_visible and self.inventory_panel.dragged_item:
                self.inventory_panel.end_drag(event.pos)
                return True  # Block event when releasing dragged item
                
        return False  # Don't block other events
        
    def update(self, delta_time: float = 1.0/60.0) -> None:
        """Update UI elements with the given time delta."""
        # Update UI elements that need time-based updates
        if self.inventory_visible:
            self.inventory_panel.update(delta_time)
        if self.textbox_visible:
            self.textbox.update(delta_time)
        if self.options_visible:
            self.options_button.update(delta_time)

    def draw(self, screen):
        # Draw UI elements in proper order
        if self.inventory_visible:
            self.inventory_panel.draw(screen)
        if self.textbox_visible:
            self.textbox.draw(screen)
        if self.options_visible:
            self.options_button.draw(screen)

    def set_text(self, text):
        self.current_text = text
        self.textbox.set_text(text)

    def add_to_inventory(self, item):
        if item not in self.inventory_items:
            self.inventory_items.append(item)
            self.inventory_panel.add_item(item)

    def remove_from_inventory(self, item):
        if item in self.inventory_items:
            self.inventory_items.remove(item)
            self.inventory_panel.remove_item(item)

    def cleanup(self) -> None:
        """Clean up UI resources."""
        self.inventory_items.clear()
        self.current_text = ""
        self.inventory_panel.cleanup()
        self.textbox.cleanup()
        self.options_button.cleanup()
        self.set_ui_visibility(False, False, False) 