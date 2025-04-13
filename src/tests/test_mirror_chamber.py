import pytest
import pygame
import sys
from ..game.scenes.mirror_chamber import MirrorChamber
from ..game.core.scene_manager import Scene

# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((1280, 720))

class MockGameState:
    def __init__(self):
        self.armor_pieces = {}

@pytest.fixture
def game_state():
    return MockGameState()

@pytest.fixture
def mirror_chamber(game_state):
    return MirrorChamber(game_state)

def test_mirror_chamber_initialization(mirror_chamber):
    """Test that MirrorChamber initializes correctly."""
    assert mirror_chamber.scene_name == "mirror_chamber"
    assert len(mirror_chamber.mirror_shards) == 5
    assert not any(shard["collected"] for shard in mirror_chamber.mirror_shards)
    assert len(mirror_chamber.placed_shards) == 0

def test_mirror_shard_collection(mirror_chamber):
    """Test collecting mirror shards."""
    # Simulate clicking on a shard
    first_shard = mirror_chamber.mirror_shards[0]
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
        'button': 1,
        'pos': first_shard["position"]
    })
    mirror_chamber.handle_events(event)
    
    # Check that the shard was collected
    assert first_shard["collected"]
    assert len([shard for shard in mirror_chamber.mirror_shards if shard["collected"]]) == 1

def test_character_movement(mirror_chamber):
    """Test character movement."""
    initial_pos = mirror_chamber.character_pos[0]
    
    # Simulate clicking to move right
    target_x = initial_pos + 100
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
        'button': 1,
        'pos': (target_x, mirror_chamber.character_pos[1])
    })
    mirror_chamber.handle_events(event)
    
    # Update for one frame
    mirror_chamber.update(0.016)  # Simulate one frame at 60 FPS
    
    # Character should have moved right
    assert mirror_chamber.character_direction == 1
    assert mirror_chamber.character_pos[0] > initial_pos

def test_dialogue_system(mirror_chamber):
    """Test the dialogue system."""
    test_dialogue = "Test dialogue"
    mirror_chamber._set_dialogue(0)  # Set initial dialogue
    
    assert mirror_chamber.current_dialogue == mirror_chamber.dialogues[0]
    assert mirror_chamber.typing_timer == 0

def test_puzzle_completion(mirror_chamber, game_state):
    """Test puzzle completion logic."""
    # Fill all mirror slots
    for i, slot in enumerate(mirror_chamber.mirror_slots):
        slot['shard'] = {'image': pygame.Surface((50, 50))}
    
    # Check puzzle completion
    mirror_chamber._check_puzzle_completion()
    
    # Verify the belt of truth was awarded
    assert game_state.armor_pieces.get("belt_of_truth") == True

def test_serpent_cutscene(mirror_chamber):
    """Test serpent cutscene triggers."""
    mirror_chamber._start_cutscene()
    
    assert mirror_chamber.cutscene_active
    assert mirror_chamber.serpent_visible
    assert mirror_chamber.cutscene_phase == 0
    assert mirror_chamber.current_dialogue == mirror_chamber.dialogues[4]

def test_break_free_from_serpent(mirror_chamber):
    """Test breaking free from serpent influence."""
    mirror_chamber._break_free_from_serpent()
    
    assert not mirror_chamber.cutscene_active
    assert not mirror_chamber.serpent_visible
    assert mirror_chamber.current_dialogue == mirror_chamber.dialogues[6]
    assert mirror_chamber.game_state.armor_pieces.get("belt_of_truth") == True 