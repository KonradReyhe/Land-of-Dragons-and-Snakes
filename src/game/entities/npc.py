"""
Base NPC Class
Defines common functionality for all NPCs in the game.
"""

from typing import Dict, List, Optional, Tuple
import pygame
from ..core.resource_manager import ResourceManager

class NPC:
    def __init__(self, name: str, position: Tuple[int, int]):
        """Initialize the NPC."""
        self.name = name
        self.position = position
        self.resource_manager = ResourceManager()
        
        # Dialogue state
        self.dialogue_stage = 0
        self.dialogue_options: List[str] = []
        self.current_dialogue: Optional[str] = None
        self.is_talking = False
        
        # Visual state
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.facing_right = True
        self.serpent_visible = False
        
        # Load NPC resources
        self.load_resources()
        
    def load_resources(self) -> None:
        """Load NPC-specific resources."""
        # Load idle animation frames
        self.idle_frames = [
            self.resource_manager.load_image(f"character_{self.name}_idle_{i}.png")
            for i in range(4)
        ]
        
        # Load talking animation frames
        self.talk_frames = [
            self.resource_manager.load_image(f"character_{self.name}_talk_{i}.png")
            for i in range(8)
        ]
        
        # Load serpent sprite if exists
        try:
            self.serpent_sprite = self.resource_manager.load_image(
                f"character_{self.name}_serpent.png"
            )
        except pygame.error:
            self.serpent_sprite = None
            
    def update(self, dt: float) -> None:
        """Update NPC state."""
        # Update animation frame
        if self.is_talking:
            self.animation_frame = (
                self.animation_frame + self.animation_speed
            ) % len(self.talk_frames)
        else:
            self.animation_frame = (
                self.animation_frame + self.animation_speed
            ) % len(self.idle_frames)
            
    def render(self, screen: pygame.Surface) -> None:
        """Render the NPC."""
        # Get current animation frame
        if self.is_talking:
            frame = self.talk_frames[int(self.animation_frame)]
        else:
            frame = self.idle_frames[int(self.animation_frame)]
            
        # Flip frame if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
            
        # Draw NPC
        screen.blit(frame, self.position)
        
        # Draw serpent if visible
        if self.serpent_visible and self.serpent_sprite:
            serpent_pos = (
                self.position[0] + 50,  # Offset from NPC
                self.position[1] - 20
            )
            screen.blit(self.serpent_sprite, serpent_pos)
            
    def start_dialogue(self) -> None:
        """Start dialogue with the NPC."""
        self.is_talking = True
        self.current_dialogue = self.get_dialogue()
        
    def end_dialogue(self) -> None:
        """End dialogue with the NPC."""
        self.is_talking = False
        self.current_dialogue = None
        
    def get_dialogue(self) -> str:
        """Get current dialogue based on stage."""
        return ""  # To be implemented by child classes
        
    def get_dialogue_options(self) -> List[str]:
        """Get available dialogue options."""
        return self.dialogue_options
        
    def select_option(self, option_index: int) -> None:
        """Handle selection of a dialogue option."""
        pass  # To be implemented by child classes
        
    def advance_stage(self) -> None:
        """Advance the NPC's dialogue stage."""
        self.dialogue_stage += 1
        self.current_dialogue = self.get_dialogue()
        
    def set_serpent_visible(self, visible: bool) -> None:
        """Set whether the NPC's serpent is visible."""
        self.serpent_visible = visible 