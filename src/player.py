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
        """Initialize the bird with animations, position (pos_x, pos_y), and physics state."""
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
        self.died = True

    def touched_ground(self, ground_line: int):
        """Check if the bird's vertical position exceeds the ground line."""
        if self.rect.y >= ground_line:
            self.rect.y = ground_line - self.rect.height
            self.die()
            self.disable_fly()

    def jump(self) -> None:
        """Apply an upward impulse to the bird's gravity."""
        self.gravity = -10

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
        self.image = pygame.transform.rotate(self.original_image, self.gravity * -3)
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
        if self.died:
            return
        self._animate()
        if self.fly:
            self._apply_physics()
            self._rotate()
            self.touched_ground(ground_line)
