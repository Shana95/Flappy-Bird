# pylint: disable=no-member
# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
"""Module containing UI classes to manage game screens and animations."""

import pygame

import states


class UI:
    """Base class for all User Interface elements in the game."""

    def __init__(
        self,
        imagepath: str,
        pos_x: int,
        pos_y: int,
        transparency: int,
        target_transparency: int,
    ):
        self.image = pygame.image.load(f"../assets/UI/{imagepath}")
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))
        self.pos_x = pos_x
        self.pos_y = pos_y

        self.original_transparency = transparency
        self.transparency = self.original_transparency
        self.target_transparency = target_transparency
        self.image.set_alpha(self.transparency)

    def reset(self) -> None:
        """Reset the UI transparency to its original value."""
        self.transparency = self.original_transparency
        self.image.set_alpha(self.transparency)

    def target_transparency_reached(
        self,
    ) -> bool:
        """Check if the current transparency has reached the target value."""
        return self.transparency == self.target_transparency

    def _animation(self):
        """Abstract method to handle animation logic"""

    def display(self):
        """Abstract method to display the UI element on the screen."""


class StartScreen(UI):
    """Class representing the game over screen shown after the player loses."""

    def _animation(self):
        """Decrease transparency to create a fade-out effect."""
        if self.transparency > self.target_transparency:
            self.transparency -= 5
            self.image.set_alpha(self.transparency)

    def draw(self, bird_state: states.States, screen: pygame.Surface) -> None:
        """
        Draw the start screen on the given surface.

        The screen stays fully visible if the bird is in the READY state,
        otherwise it gradually fades out.
        """
        if bird_state == states.States.READY:
            screen.blit(self.image, self.rect)
            return

        if self.transparency > 0:
            self._animation()
            screen.blit(self.image, self.rect)


class GameOverScreen(UI):
    """Class representing the game over screen shown after the player loses."""

    def _animation(self):
        """Increase transparency to create a fade-in effect."""
        if self.transparency < self.target_transparency:
            self.transparency += 5
            self.image.set_alpha(self.transparency)

    def draw(self, bird_state: states.States, screen: pygame.Surface) -> None:
        """
        Draw the game over screen on the given surface.

        The screen gradually fades in only when the bird state is GROUNDED.
        """
        if bird_state == states.States.GROUNDED:
            self._animation()
            screen.blit(self.image, self.rect)
