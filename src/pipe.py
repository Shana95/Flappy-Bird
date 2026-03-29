# pylint: disable=no-member
# pylint: disable=too-many-locals
"""Module for managing pipe obstacles in the game"""

import pygame

import states


class Pipe(pygame.sprite.Sprite):
    """Handles the obstacles (pipes) and their interaction with the game world."""

    pipe_bottom_surface: pygame.Surface | None = None
    pipe_top_surface: pygame.Surface | None = None

    def __init__(self, x: int, y: int, position: int, gap: int, *groups):
        super().__init__(*groups)

        if Pipe.pipe_bottom_surface is None:
            Pipe.pipe_bottom_surface = pygame.image.load(
                "../assets/Game Objects/pipe-green.png"
            ).convert_alpha()
            Pipe.pipe_top_surface = pygame.transform.flip(
                Pipe.pipe_bottom_surface, False, True
            )

        self.passed = False
        self.position = position

        assert Pipe.pipe_top_surface is not None
        assert Pipe.pipe_bottom_surface is not None

        if self.position == 1:
            self.image = Pipe.pipe_top_surface
            self.rect = self.image.get_rect(midbottom=(x, y - (gap // 2)))
        else:
            self.image = Pipe.pipe_bottom_surface
            self.rect = self.image.get_rect(midtop=(x, y + (gap // 2)))

        self.mask = pygame.mask.from_surface(self.image)

    def get_position(self):
        """Return the pipe's position attribute"""
        return self.position

    def _is_off_screen(self) -> bool:
        """Check if the pipe has completely moved off the left side of the screen."""
        return self.rect.right < -50

    def check_passed(self, bird_x: int) -> bool:
        """Determine if the bird has crossed the center of the pipe."""
        if not self.passed and bird_x > self.rect.centerx:
            self.passed = True
            return True
        return False

    def update(self, velocity: int, bird_state) -> None:
        """Update the pipe's position and handle its lifecycle."""
        if bird_state == states.States.FLYING:
            self.rect.x -= velocity
            if self._is_off_screen():
                self.kill()
