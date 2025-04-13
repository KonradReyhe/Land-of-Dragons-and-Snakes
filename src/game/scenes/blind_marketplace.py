"""
Blind Marketplace Scene
The second scene of the game, serving as a hub area with multiple NPCs.
"""

from typing import Dict, List, Optional, Tuple
import pygame
from .base_scene import BaseScene
from ..entities.npc import NPC
from ..core.resource_manager import ResourceManager
from ..core.input_manager import InputManager

class BlindMarketplace(BaseScene):
    def __init__(self):
        """Initialize the Blind Marketplace scene."""
        super().__init__("blind_marketplace")
        
        # NPCs
        self.npcs: Dict[str, NPC] = {
            "justifier": NPC("justifier", (300, 400)),
            "mother": NPC("mother", (600, 400)),
            "performer": NPC("performer", (900, 400)),
            "mason": NPC("mason", (1200, 400)),
            "silent_child": NPC("silent_child", (1500, 400))
        }
        
        # Scene state
        self.active_npc: Optional[NPC] = None
        self.dialogue_active = False
        self.serpent_vision = False
        self.fountain_broken = True
        self.bell_towers_visible = True
        
        # Load scene-specific resources
        self.load_resources()
        
    def load_resources(self) -> None:
        """Load scene-specific resources."""
        super().load_resources()
        
        # Load fountain image
        self.fountain_image = self.resource_manager.load_image("fountain.png")
        self.fountain_rect = pygame.Rect(800, 300, 200, 200)
        
        # Load bell tower images
        self.bell_tower_images = {
            "boaz": self.resource_manager.load_image("bell_tower_boaz.png"),
            "jachin": self.resource_manager.load_image("bell_tower_jachin.png")
        }
        self.bell_tower_rects = {
            "boaz": pygame.Rect(200, 100, 100, 200),
            "jachin": pygame.Rect(1600, 100, 100, 200)
        }
        
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle scene-specific events."""
        super().handle_event(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Toggle serpent vision
                self._toggle_serpent_vision()
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                self._handle_click(event.pos)
                
    def _toggle_serpent_vision(self) -> None:
        """Toggle serpent vision mode."""
        self.serpent_vision = not self.serpent_vision
        for npc in self.npcs.values():
            npc.set_serpent_visible(self.serpent_vision)
            
    def _handle_click(self, pos: Tuple[int, int]) -> None:
        """Handle click interactions in the Blind Marketplace."""
        if self.dialogue_active:
            self._handle_dialogue_click(pos)
            return
            
        # Check NPCs
        for npc in self.npcs.values():
            if npc.rect.collidepoint(pos):
                self._start_dialogue(npc)
                return
                
        # Check fountain
        if self.fountain_rect.collidepoint(pos):
            self._interact_with_fountain()
            return
            
        # Check bell towers
        for name, rect in self.bell_tower_rects.items():
            if rect.collidepoint(pos):
                self._interact_with_bell_tower(name)
                return
                
    def _handle_dialogue_click(self, pos: Tuple[int, int]) -> None:
        """Handle clicks during dialogue."""
        if not self.active_npc:
            return
            
        # Check dialogue options
        option_rects = self._get_dialogue_option_rects()
        for i, rect in enumerate(option_rects):
            if rect.collidepoint(pos):
                self.active_npc.select_option(i)
                return
                
        # Click anywhere else to advance dialogue
        self.active_npc.advance_stage()
        
    def _start_dialogue(self, npc: NPC) -> None:
        """Start dialogue with an NPC."""
        self.active_npc = npc
        self.dialogue_active = True
        npc.start_dialogue()
        
    def _interact_with_fountain(self) -> None:
        """Handle fountain interaction."""
        if self.fountain_broken:
            # Play fountain sound
            try:
                sound = self.resource_manager.load_sound("fountain_broken.ogg")
                sound.play()
            except pygame.error:
                pass
                
    def _interact_with_bell_tower(self, name: str) -> None:
        """Handle bell tower interaction."""
        # Check if player has crystal shard
        if self.game_state.has_item("crystal_shard"):
            # Transition to bell tower scene
            self.start_fade(fade_in=False)
            pygame.time.set_timer(
                pygame.USEREVENT + 1,  # Custom event for scene transition
                1000  # 1 second delay
            )
            
    def update(self, dt: float) -> None:
        """Update the Blind Marketplace scene."""
        super().update(dt)
        
        # Update NPCs
        for npc in self.npcs.values():
            npc.update(dt)
            
        # Check for scene completion
        if all(npc.dialogue_stage >= 3 for npc in self.npcs.values()):
            self._complete_scene()
            
    def _complete_scene(self) -> None:
        """Complete the scene and transition to next."""
        # Award Crystal Shard
        self.game_state.add_item("crystal_shard")
        
        # Start fade out
        self.start_fade(fade_in=False)
        
        # Transition to next scene after fade
        pygame.time.set_timer(
            pygame.USEREVENT + 1,  # Custom event for scene transition
            1000  # 1 second delay
        )
        
    def render(self, screen: pygame.Surface) -> None:
        """Render the Blind Marketplace scene."""
        super().render(screen)
        
        # Draw fountain
        screen.blit(self.fountain_image, self.fountain_rect)
        
        # Draw bell towers
        for name, image in self.bell_tower_images.items():
            screen.blit(image, self.bell_tower_rects[name])
            
        # Draw NPCs
        for npc in self.npcs.values():
            npc.render(screen)
            
        # Draw dialogue if active
        if self.dialogue_active and self.active_npc:
            self._render_dialogue(screen)
            
        # Draw fade effect
        if self.fade_alpha > 0:
            screen.blit(self.fade_surface, (0, 0))
            
    def _render_dialogue(self, screen: pygame.Surface) -> None:
        """Render the dialogue box and options."""
        # Draw dialogue box
        dialogue_rect = pygame.Rect(100, 800, 1720, 200)
        pygame.draw.rect(screen, (0, 0, 0, 200), dialogue_rect)
        
        # Draw NPC name
        font = self.resource_manager.get_font("main", 24)
        name_text = font.render(self.active_npc.name, True, (255, 255, 255))
        screen.blit(name_text, (120, 820))
        
        # Draw dialogue text
        dialogue_text = self.active_npc.current_dialogue
        if dialogue_text:
            text_surface = font.render(dialogue_text, True, (255, 255, 255))
            screen.blit(text_surface, (120, 860))
            
        # Draw dialogue options
        options = self.active_npc.get_dialogue_options()
        if options:
            for i, option in enumerate(options):
                option_rect = pygame.Rect(120, 900 + i * 30, 1680, 30)
                pygame.draw.rect(screen, (50, 50, 50), option_rect)
                option_text = font.render(option, True, (255, 255, 255))
                screen.blit(option_text, (130, 905 + i * 30))
                
    def _get_dialogue_option_rects(self) -> List[pygame.Rect]:
        """Get rectangles for dialogue options."""
        options = self.active_npc.get_dialogue_options()
        return [
            pygame.Rect(120, 900 + i * 30, 1680, 30)
            for i in range(len(options))
        ] 