# pylint: disable=too-many-locals
"""Module containing classes to manage
game background elements like Sky and Ground."""

import pygame

import states


class Background:
    """Base class for background elements, providing common attributes and methods."""

    def __init__(self, filename: str, pos_x: int, pos_y: int, screen: pygame.Surface):
        """Initialize background with image, position, and screen reference."""
        self.screen = screen
        self.surface = pygame.image.load(
            f"../assets/Game Objects/{filename}"
        ).convert_alpha()
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_width(self) -> int:
        """Return the width of the background surface."""
        return self.width

    def get_height(self) -> int:
        """Return the height of the background surface."""
        return self.height

    def get_pos_x(self) -> int:
        """Return the current X position."""
        return self.pos_x

    def get_pos_y(self) -> int:
        """Return the current Y position."""
        return self.pos_y

    def draw(self) -> None:
        """Method to draw the object on the screen."""
        self.screen.blit(self.surface, (self.pos_x, self.pos_y))


class Sky(Background):
    """Class representing the sky background layer."""


class Ground(Background):
    """Class representing the scrolling ground with movement logic."""

    def __init__(
        self, filename: str, pos_x: int, sky_height: int, screen: pygame.Surface
    ):
        """Initialize the ground and calculate its vertical position."""
        super().__init__(filename, pos_x, 0, screen)
        self.pos_y = sky_height - self.get_height()

    def move(self, velocity: int) -> None:
        """Update the X position to create a scrolling effect."""
        self.pos_x -= velocity
        if abs(self.pos_x) > (self.width / 7):
            self.pos_x = 0

    def update(self, velocity: int, bird_state: states.States) -> None:
        """
        Draws the ground and updates its position based on the bird's state.

        The ground only scrolls if the bird is in an active state (e.g., READY or FLYING),
        preventing background movement after a collision.
        """
        self.draw()
        if bird_state in (states.States.FLYING, states.States.READY):
            self.move(velocity)
