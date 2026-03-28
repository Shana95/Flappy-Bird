# pylint: disable=too-many-instance-attributes
# pylint: disable=no-member
"""Module handling the bird's logic, including physics, animations, and death states."""

import pygame

import states


class Bird(pygame.sprite.Sprite):
    """
    Class representing the player-controlled bird.
    Inherits from pygame.sprite.Sprite to utilize Group management.
    """

    def __init__(self, pos_x: int, pos_y: int) -> None:
        """Initialize the bird with animations"""
        super().__init__()

        self.images = []
        for i in range(0, 3):
            image = pygame.image.load(
                f"../assets/Game Objects/yellowbird-{i}.png"
            ).convert_alpha()
            self.images.append(image)

        self.image_index = 0.0

        self.original_image = self.images[int(self.image_index)]
        self.image = self.original_image
        self.rect = self.image.get_rect(midbottom=(pos_x, pos_y))

        self.gravity = 0.0
        self.fly = False
        self.died = False
        self.is_rotated_to_death = False
        self.mask = pygame.mask.from_surface(self.image)

    def get_state(self) -> states.States:
        """Returns the current states.States member based on bird physics."""
        if not self.fly and not self.died:
            return states.States.READY
        if not self.fly and self.died:
            return states.States.GROUNDED
        if self.fly and not self.died:
            return states.States.FLYING
        return states.States.FALLING

    def enable_fly(self) -> None:
        """Enable gravity and physics for the bird."""
        self.fly = True

    def disable_fly(self) -> None:
        """Disable gravity and physics for the bird."""
        self.fly = False

    def die(self):
        """Trigger the bird's death state."""
        self.fly = False
        self.died = True

    def reset(self):
        """
        Reset the bird to its initial state for a new game.

        This resets the vertical position, gravity, death flags,
        and restores the original unrotated image.
        """
        self.rect.midbottom = (90, 220)
        self.gravity = 0.0
        self.died = False
        self.is_rotated_to_death = False
        self.image = self.original_image

    def hit_ground(self, ground_line: int):
        """Check if the bird's vertical position exceeds the ground line."""
        visible_bottom = self.image.get_bounding_rect().bottom
        empty_space = self.image.get_height() - visible_bottom

        if self.rect.bottom - empty_space >= ground_line:
            self.rect.bottom = ground_line + empty_space
            # Upon hitting the ground, reset gravity.
            self.gravity = 0

            if not self.died:
                self.die()

            self.disable_fly()

    def hit_ceiling(self):
        """Prevent the bird from flying above the sky (screen top)."""
        if self.rect.top <= 0:
            self.rect.top = 0
            self.gravity = max(self.gravity, 0.0)

    def jump(self) -> None:
        """Apply an upward impulse to the bird's gravity."""
        self.gravity = -7

    def apply_gravity(self) -> None:
        """Update gravity value and apply it to the bird's vertical position."""
        self.gravity += 0.5
        self.rect.y += int(self.gravity)

    def _animate(self) -> None:
        """Exclusively handles frame transitions for the wing-flapping animation."""
        self.image_index = (self.image_index + 0.30) % len(self.images)
        self.original_image = self.images[int(self.image_index)]
        if not self.fly:
            self.image = self.original_image

    def _rotate(self) -> None:
        """Exclusively handles the bird's rotation based on its vertical velocity."""
        angle = self.gravity * -3
        if angle <= -90:
            angle = -90
        elif angle >= 25:
            angle = 25
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _apply_physics(self) -> None:
        """Exclusively manages gravity and vertical movement."""
        self.gravity += 0.5
        self.rect.y += int(self.gravity)

    def update(self, ground_line: int) -> None:
        """
        Update bird logic every frame if the bird is still alive.
        ground_line indicates the Current Y position of the ground.
        """
        if not self.died:
            self._animate()

        if self.fly or self.died:
            self._apply_physics()
            self.hit_ceiling()
            self.hit_ground(ground_line)

        if not self.died:
            # Only rotate the bird if it's still alive
            self._rotate()
        elif self.rect.bottom < ground_line:
            if not self.is_rotated_to_death:
                current_center = self.rect.center
                self.image = pygame.transform.rotate(self.original_image, -90)
                self.rect = self.image.get_rect(center=current_center)
                self.is_rotated_to_death = True
        elif not self.is_rotated_to_death and self.gravity == 0:
            self.is_rotated_to_death = True
        # if self.gravity == 0 and self.died:
        #     visible_bottom = self.image.get_bounding_rect().bottom
        #     empty_space = self.image.get_height() - visible_bottom
        #     self.rect.bottom = ground_line + empty_space
