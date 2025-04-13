"""
Game State Manager
Handles persistent game data, progression, and save/load functionality.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional

class GameState:
    def __init__(self):
        """Initialize the game state."""
        self.armor_pieces: Dict[str, bool] = {
            "belt_of_truth": False,
            "breastplate_of_righteousness": False,
            "shoes_of_peace": False,
            "shield_of_faith": False,
            "helmet_of_salvation": False,
            "sword_of_spirit": False
        }
        
        self.scrolls_read: List[str] = []
        self.glyphs_collected: List[str] = []
        self.echoes_found: List[str] = []
        self.serpent_typology: Dict[str, Dict] = {}
        
        self.current_scene: str = "mirror_chamber"
        self.serpent_vision: bool = False
        self.coin_of_deceit: bool = False
        
        self.save_path = Path("saves")
        self.save_path.mkdir(exist_ok=True)

    def has_all_armor(self) -> bool:
        """Check if player has collected all armor pieces."""
        return all(self.armor_pieces.values())

    def can_access_scene(self, scene_name: str) -> bool:
        """Check if player can access a specific scene."""
        scene_requirements = {
            "marketplace": ["belt_of_truth"],
            "ruined_church": ["belt_of_truth", "breastplate_of_righteousness"],
            "bell_towers": ["belt_of_truth", "breastplate_of_righteousness", "shoes_of_peace"],
            "dragon_cavern": ["belt_of_truth", "breastplate_of_righteousness", 
                            "shoes_of_peace", "shield_of_faith", "helmet_of_salvation"]
        }
        
        if scene_name not in scene_requirements:
            return True
            
        required_armor = scene_requirements[scene_name]
        return all(self.armor_pieces[armor] for armor in required_armor)

    def save_game(self, slot: int = 0) -> bool:
        """Save the current game state to a file."""
        try:
            save_data = {
                "armor_pieces": self.armor_pieces,
                "scrolls_read": self.scrolls_read,
                "glyphs_collected": self.glyphs_collected,
                "echoes_found": self.echoes_found,
                "serpent_typology": self.serpent_typology,
                "current_scene": self.current_scene,
                "serpent_vision": self.serpent_vision,
                "coin_of_deceit": self.coin_of_deceit
            }
            
            save_file = self.save_path / f"save_{slot}.json"
            with open(save_file, 'w') as f:
                json.dump(save_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False

    def load_game(self, slot: int = 0) -> bool:
        """Load a game state from a file."""
        try:
            save_file = self.save_path / f"save_{slot}.json"
            if not save_file.exists():
                return False
                
            with open(save_file, 'r') as f:
                save_data = json.load(f)
                
            self.armor_pieces = save_data["armor_pieces"]
            self.scrolls_read = save_data["scrolls_read"]
            self.glyphs_collected = save_data["glyphs_collected"]
            self.echoes_found = save_data["echoes_found"]
            self.serpent_typology = save_data["serpent_typology"]
            self.current_scene = save_data["current_scene"]
            self.serpent_vision = save_data["serpent_vision"]
            self.coin_of_deceit = save_data["coin_of_deceit"]
            
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False

    def get_completion_percentage(self) -> float:
        """Calculate game completion percentage."""
        total_items = (
            len(self.armor_pieces) +  # 6 armor pieces
            len(self.scrolls_read) +  # 30 scrolls
            len(self.glyphs_collected) +  # 12 glyphs
            len(self.echoes_found) +  # 8 echoes
            len(self.serpent_typology)  # 7 serpent types
        )
        
        max_items = 6 + 30 + 12 + 8 + 7  # Total possible items
        return (total_items / max_items) * 100 