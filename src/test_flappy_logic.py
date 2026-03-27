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
        
        # Dynamic Rect positioning to allow physics updates and maintain position during rotations
        def dynamic_get_rect(**kwargs):
            # Se viene passato un centro o una posizione, crea il rect lì
            if 'midbottom' in kwargs: return pygame.Rect(kwargs['midbottom'][0], kwargs['midbottom'][1], 50, 50)
            if 'midtop' in kwargs: return pygame.Rect(kwargs['midtop'][0], kwargs['midtop'][1], 50, 50)
            if 'center' in kwargs: return pygame.Rect(kwargs['center'][0]-25, kwargs['center'][1]-25, 50, 50)
            # Default
            return pygame.Rect(0, 0, 50, 50)

        mock_surface.get_rect.side_effect = dynamic_get_rect
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

def test_bird_state_transitions():
    """
    Verifies the bird's state machine transitions during a standard lifecycle:
    from READY to FLYING, and halting at GROUNDED upon collision.
    """
    bird = player.Bird(100, 200)
    
    assert bird.get_state() == States.READY
    
    bird.enable_fly()
    assert bird.get_state() == States.FLYING
    
    bird.die()
    assert bird.get_state() == States.GROUNDED

def test_pipe_movement():
    """Ensures the pipe correctly updates its x-coordinate."""
    pipe_instance = pipe.Pipe(300, 200, 0, 100)
    initial_x = pipe_instance.rect.x
    velocity = 5
    pipe_instance.update(velocity, States.FLYING)
    assert pipe_instance.rect.x == initial_x - velocity

def test_pipe_scoring_logic():
    """Validates the scoring boundary logic."""
    pipe_instance = pipe.Pipe(100, 200, 0, 100)
    pipe_instance.rect.centerx = 100
    has_passed = pipe_instance.check_passed(110)
    assert has_passed is True
    assert pipe_instance.passed is True

def test_ground_scrolling():
    """Verifies the parallax ground object scrolls correctly."""
    mock_screen = MagicMock(spec=pygame.Surface)
    ground = background.Ground("base.png", 0, 500, mock_screen)
    ground.width = 700 
    initial_x = ground.pos_x
    velocity = 10
    ground.update(velocity, States.FLYING)
    assert ground.pos_x == initial_x - velocity

@pytest.mark.parametrize("y_pos, expected_death", [
    (100, False), # Volo normale
    (560, True),  # Collisione con il terreno
])
def test_bird_ground_collision(y_pos, expected_death):
    """Parameterized test covering ground collision scenarios."""
    bird = player.Bird(100, y_pos)
    bird.rect.bottom = y_pos
    bird.hit_ground(500)
    assert bird.died is expected_death

def test_bird_applies_physics_when_flying():
    """Ensures gravity affects the bird only when the state is FLYING."""
    bird = player.Bird(100, 200)
    bird.enable_fly()
    initial_y = bird.rect.y
    # Chiamiamo update due volte per accumulare gravità a sufficienza (> 1.0)
    bird.update(500)
    bird.update(500)
    # Verifichiamo che la posizione Y sia cambiata rispetto all'originale
    assert bird.rect.y != initial_y

def test_bird_no_physics_when_not_flying():
    """Ensures the bird remains static when the game is not active."""
    bird = player.Bird(100, 200)
    initial_y = bird.rect.y
    bird.update(500)
    assert bird.rect.y == initial_y

def test_bird_hits_ceiling():
    """Validates ceiling collision constraints preventing out-of-bounds flight."""
    bird = player.Bird(100, 50)
    bird.enable_fly()
    bird.rect.top = -10
    bird.update(500)
    assert bird.rect.top == 0

def test_bird_hits_ground_and_dies():
    """Ensures fatal state is triggered upon forced ground intersection."""
    bird = player.Bird(100, 600)
    bird.enable_fly()
    bird.rect.bottom = 600
    bird.update(500)
    assert bird.died is True
    assert bird.fly is False