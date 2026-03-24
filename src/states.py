"""
Module defining the possible states of the bird entity.
Used to coordinate game physics, animations, and UI transitions.
"""

from enum import Enum


class States(Enum):
    """
    Enumeration of the possible states for the bird during the game.

    This Enum is used to control the game flow, animations,
    and background scrolling.
    """

    READY = 1
    """The initial state where the bird floats and waits for player input."""
    FLYING = 2
    """The bird is active in the game with physics and gravity applied."""
    GROUNDED = 3
    """The bird has touched the ground; physics are disabled and game is over."""
    FALLING = 4
    """The bird has hit a pipe and is falling toward the ground."""
