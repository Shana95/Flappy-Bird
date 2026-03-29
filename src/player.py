# pylint: disable=too-many-instance-attributes
# pylint: disable=no-member
"""Module handling the bird's logic, including physics, animations, and death states."""

import pygame

import states


class Bird(pygame.sprite.Sprite):
    """
    Represents the player-controlled bird, handling physics, animations,
    and state transitions.
    Inherits from pygame.sprite.Sprite to utilize Group management.
    """

    def __init__(self, pos_x: int, pos_y: int) -> None:
        """
        Initialize the bird with its position, animations, and physical properties.
        """
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
        self.mask = pygame.mask.from_surface(self.image)

    def enable_fly(self) -> None:
        """Enable gravity and physics for the bird."""
        self.fly = True

    def disable_fly(self) -> None:
        """Disable gravity and physics for the bird."""
        self.fly = False

    def die(self):
        """
        Transition the bird to the dead state, disabling flight
        and stopping animations.
        """
        self.fly = False
        self.died = True

    def get_state(self) -> states.States:
        """
        Determine the bird's current operational state based on physical flags.

        Returns:
            states.States: The member of the States enum (READY, GROUNDED, FLYING, FALLING).
        """
        if not self.fly and not self.died:
            return states.States.READY
        if not self.fly and self.died:
            return states.States.GROUNDED
        if self.fly and not self.died:
            return states.States.FLYING
        return states.States.FALLING

    def reset(self):
        """
        Reset the bird to its initial state for a new game.

        This resets the vertical position, gravity, death flags,
        and restores the original unrotated image.
        """
        self.rect.midbottom = (90, 220)
        self.gravity = 0.0
        self.died = False
        self.image = self.original_image

    def current_bottom(self):
        """
        Calculate the y-coordinate of the bird's lowest visible pixel
        to ensure accurate ground collision by ignoring transparent padding.
        """
        visible_bottom = self.image.get_bounding_rect().bottom
        empty_space = self.image.get_height() - visible_bottom
        return self.rect.bottom - empty_space

    def hit_ground(self, ground_line: int):
        """
        Check if the bird's vertical position exceeds the ground line.
        Stops the bird at the ground surface and disables flight logic.
        """
        offset = self.image.get_height() - self.image.get_bounding_rect().bottom

        if self.current_bottom() >= ground_line:
            self.rect.bottom = ground_line + offset
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
        """
        Exclusively handles frame transitions for the wing-flapping animation
        (provided the flight flag is active).
        """
        if self.fly:
            self.image_index = (self.image_index + 0.30) % len(self.images)
            self.original_image = self.images[int(self.image_index)]

    def _rotate(self) -> None:
        """Exclusively handles the bird's rotation based on its vertical velocity."""
        if self.died:
            angle = -90
        else:
            angle = int(max(min(self.gravity * -8, 25), -90))

        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _apply_physics(self) -> None:
        """Exclusively manages gravity and vertical movement."""
        self.gravity += 0.5
        self.rect.y += int(self.gravity)

    def update(self, ground_line: int) -> None:
        """
        Orchestrate the per-frame bird logic: animation, physics, and rotation.
        """
        if not self.died:
            self._animate()

        if self.fly or self.died:
            self._apply_physics()
            self.hit_ceiling()
            self.hit_ground(ground_line)

        self._rotate()
