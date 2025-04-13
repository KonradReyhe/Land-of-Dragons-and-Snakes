"""
Test configuration and shared fixtures for the Land of Dragons and Snakes game.
"""

import pytest
import pygame
import os

@pytest.fixture(autouse=True)
def pygame_setup():
    """Initialize pygame for all tests."""
    pygame.init()
    pygame.display.set_mode((1280, 720))
    
    # Ensure the assets directories exist
    os.makedirs("assets/images/backgrounds", exist_ok=True)
    os.makedirs("assets/sounds", exist_ok=True)
    os.makedirs("assets/ui/buttons", exist_ok=True)
    
    yield
    
    pygame.quit()

@pytest.fixture
def mock_surface():
    """Create a mock pygame surface for testing."""
    return pygame.Surface((1280, 720))

@pytest.fixture
def mock_event():
    """Create a mock pygame event for testing."""
    return lambda type, **kwargs: pygame.event.Event(type, kwargs) 