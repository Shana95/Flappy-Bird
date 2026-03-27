import pytest
from unittest.mock import MagicMock, patch

import pygame
import background
import pipe
import player
from states import States

# --- GLOBAL FIXTURES ---

@pytest.fixture(autouse=True)
def mock_pygame_essentials():
    """
    Global fixture to mock Pygame's core functionalities.
    Ensures tests run in complete isolation without requiring a display server
    or physical asset loading, preventing I/O bottlenecks.
    """
    with patch("pygame.image.load") as mock_load, \
         patch("pygame.mask.from_surface") as mock_mask, \
         patch("pygame.transform.rotate") as mock_rotate, \
         patch("pygame.transform.flip") as mock_flip:
        
        # 1. Setup mock surface with concrete return values to satisfy internal physics math
        mock_surface = MagicMock(spec=pygame.Surface)
        mock_surface.get_rect.return_value = pygame.Rect(0, 0, 50, 50)
        mock_surface.get_width.return_value = 100
        mock_surface.get_height.return_value = 100
        
        # Define bounding box to simulate transparent pixel padding
        mock_surface.get_bounding_rect.return_value = pygame.Rect(0, 0, 50, 48)
        
        # 2. Configure chained mock calls for sprite rendering pipeline
        mock_load.return_value.convert_alpha.return_value = mock_surface
        mock_rotate.return_value = mock_surface
        mock_flip.return_value = mock_surface
        mock_mask.return_value = MagicMock()
        
        yield

# --- UNIT TESTS ---

def test_bird_jump_gravity_update():
    """
    Validates the bird's jump physics utilizing the AAAA pattern 
    (Arrange, Assert, Act, Assert) to ensure initial state integrity before the action.
    """
    # Arrange
    bird = player.Bird(100, 200)
    bird.gravity = 0
    
    # Assert (Initial Condition)
    assert bird.gravity == 0 
    
    # Act
    bird.jump()
    
    # Assert (Post-Action State)
    assert bird.gravity == -7