import pytest
import pygame
from ..game.scenes.starting_screen import StartingScreen

# Initialize pygame for testing
pygame.init()
pygame.display.set_mode((1280, 720))

class MockGameState:
    def __init__(self):
        self.current_scene = None

@pytest.fixture
def game_state():
    return MockGameState()

@pytest.fixture
def starting_screen(game_state):
    return StartingScreen(game_state)

def test_starting_screen_initialization(starting_screen):
    """Test that StartingScreen initializes correctly."""
    assert starting_screen.scene_name == "starting_screen"
    assert starting_screen.title_text == "Land of Dragons and Snakes"
    assert starting_screen.button_text == "Start Journey"
    assert not starting_screen.button_hovered

def test_button_hover(starting_screen):
    """Test button hover state changes."""
    # Simulate mouse over button
    event = pygame.event.Event(pygame.MOUSEMOTION, {
        'pos': starting_screen.button_rect.center
    })
    starting_screen.handle_events(event)
    assert starting_screen.button_hovered

    # Simulate mouse outside button
    event = pygame.event.Event(pygame.MOUSEMOTION, {
        'pos': (0, 0)
    })
    starting_screen.handle_events(event)
    assert not starting_screen.button_hovered

def test_button_click(starting_screen):
    """Test button click triggers scene transition."""
    # First hover over button
    starting_screen.button_hovered = True
    
    # Simulate click on button
    event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {
        'button': 1,
        'pos': starting_screen.button_rect.center
    })
    
    # Store the original transition method
    original_transition = starting_screen.start_transition
    transition_called = False
    
    def mock_transition(scene_name):
        nonlocal transition_called
        transition_called = True
        assert scene_name == "mirror_chamber"
    
    # Replace with mock
    starting_screen.start_transition = mock_transition
    
    # Handle the click event
    starting_screen.handle_events(event)
    
    # Verify transition was called
    assert transition_called
    
    # Restore original method
    starting_screen.start_transition = original_transition

def test_glow_animation(starting_screen):
    """Test glow animation updates correctly."""
    initial_alpha = starting_screen.glow_alpha
    
    # Update for one frame
    starting_screen.update(0.016)  # Simulate one frame at 60 FPS
    
    # Alpha should have changed
    assert starting_screen.glow_alpha != initial_alpha
    
    # Test bounds
    for _ in range(100):  # Run multiple updates
        starting_screen.update(0.016)
        assert 0 <= starting_screen.glow_alpha <= 100

def test_decorative_line_drawing(starting_screen):
    """Test decorative line drawing function."""
    # Create a test surface
    surface = pygame.Surface((100, 100))
    start_pos = (10, 10)
    end_pos = (90, 90)
    color = (255, 255, 255)
    
    # Draw line
    starting_screen._draw_decorative_line(surface, start_pos, end_pos, color)
    
    # Check that pixels were drawn
    assert surface.get_at(start_pos) == color  # Check start point
    assert surface.get_at(end_pos) == color    # Check end point 