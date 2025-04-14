"""
Game State Manager
Handles persistent game data, progression, and save/load functionality.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, TypedDict, Literal

logger = logging.getLogger(__name__)

class ArmorPieces(TypedDict):
    belt_of_truth: bool
    breastplate_of_righteousness: bool
    shoes_of_peace: bool
    shield_of_faith: bool
    helmet_of_salvation: bool
    sword_of_spirit: bool

class SaveData(TypedDict):
    armor_pieces: ArmorPieces
    scrolls_read: List[str]
    glyphs_collected: List[str]
    echoes_found: List[str]
    serpent_typology: Dict[str, Dict]
    current_scene: str
    serpent_vision: bool
    coin_of_deceit: bool

class GameState:
    """Manages the game's persistent state including progression, items, and save data."""
    
    def __init__(self) -> None:
        """Initialize the game state with default values."""
        self.armor_pieces: ArmorPieces = {
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
        """Check if player has collected all armor pieces.
        
        Returns:
            bool: True if all armor pieces are collected, False otherwise.
        """
        return all(self.armor_pieces.values())

    def can_access_scene(self, scene_name: str) -> bool:
        """Check if player can access a specific scene based on collected armor.
        
        Args:
            scene_name: Name of the scene to check access for.
            
        Returns:
            bool: True if player can access the scene, False otherwise.
        """
        scene_requirements: Dict[str, List[str]] = {
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
        """Save the current game state to a file.
        
        Args:
            slot: Save slot number (0-9).
            
        Returns:
            bool: True if save was successful, False otherwise.
        """
        if not 0 <= slot <= 9:
            logger.error(f"Invalid save slot: {slot}")
            return False
            
        try:
            save_data: SaveData = {
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
            logger.info(f"Game saved successfully to slot {slot}")
            return True
        except Exception as e:
            logger.error(f"Error saving game: {e}")
            return False

    def load_game(self, slot: int = 0) -> bool:
        """Load a game state from a file.
        
        Args:
            slot: Save slot number (0-9).
            
        Returns:
            bool: True if load was successful, False otherwise.
        """
        if not 0 <= slot <= 9:
            logger.error(f"Invalid save slot: {slot}")
            return False
            
        try:
            save_file = self.save_path / f"save_{slot}.json"
            if not save_file.exists():
                logger.error(f"Save file not found for slot {slot}")
                return False
                
            with open(save_file, 'r') as f:
                save_data: SaveData = json.load(f)
                
            self.armor_pieces = save_data["armor_pieces"]
            self.scrolls_read = save_data["scrolls_read"]
            self.glyphs_collected = save_data["glyphs_collected"]
            self.echoes_found = save_data["echoes_found"]
            self.serpent_typology = save_data["serpent_typology"]
            self.current_scene = save_data["current_scene"]
            self.serpent_vision = save_data["serpent_vision"]
            self.coin_of_deceit = save_data["coin_of_deceit"]
            
            logger.info(f"Game loaded successfully from slot {slot}")
            return True
        except Exception as e:
            logger.error(f"Error loading game: {e}")
            return False

    def get_completion_percentage(self) -> float:
        """Calculate the game completion percentage.
        
        Returns:
            float: Completion percentage from 0 to 100.
        """
        total_items = (
            len(self.armor_pieces) +  # Armor pieces
            len(self.scrolls_read) +  # Scrolls
            len(self.glyphs_collected) +  # Glyphs
            len(self.echoes_found)  # Echoes
        )
        
        collected_items = (
            sum(1 for collected in self.armor_pieces.values() if collected) +
            len(self.scrolls_read) +
            len(self.glyphs_collected) +
            len(self.echoes_found)
        )
        
        return (collected_items / total_items) * 100 if total_items > 0 else 0.0 