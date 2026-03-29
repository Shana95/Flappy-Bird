"""Module for managing the game scoring system."""

import pygame

import states


class Score:
    """Handles the game scoring system and renders it using layered fonts."""

    def __init__(
        self, font_border_name: str, font_fill_name: str, pos_x: int, pos_y: int
    ) -> None:
        self.font_border = pygame.font.Font(f"../assets/Fonts/{font_border_name}", 32)
        self.font_fill = pygame.font.Font(f"../assets/Fonts/{font_fill_name}", 32)
        self.value = 0
        self.pos_x = pos_x
        self.pos_y = pos_y

    def reset(self) -> None:
        """Reset the current score value to zero."""
        self.value = 0

    def scored(self) -> None:
        """Increment the score value by one."""
        self.value += 1

    def draw(
        self,
        timing: bool,
        screen: pygame.Surface,
        bird_state: states.States,
    ) -> None:
        """Render the score layers onto the provided screen surface."""
        if bird_state == states.States.FLYING and timing:
            surf_border = self.font_border.render(
                str(self.value), True, (0, 0, 0)
            ).convert_alpha()
            rect_border = surf_border.get_rect(center=(self.pos_x, self.pos_y))

            surf_fill = self.font_fill.render(
                str(self.value), True, (255, 255, 255)
            ).convert_alpha()
            rect_fill = surf_fill.get_rect(center=(self.pos_x, self.pos_y))

            screen.blit(surf_fill, rect_fill)
            screen.blit(surf_border, rect_border)
