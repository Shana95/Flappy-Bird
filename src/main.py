# pylint: disable=no-member
"""Main execution script for the Flappy Bird game loop."""

import sys

import pygame

import player
from background import Ground, Sky


def main() -> None:
    """Initialize the game engine and manage the real-time event loop."""
    screen_width = 1024
    screen_height = 768

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    fps = 60

    velocity = 1

    filename_sky = "background-day.png"
    filename_ground = "base.png"

    sky = Sky(filename_sky, 0, 0, screen)
    ground = Ground(filename_ground, 0, sky.get_height(), screen)

    bird_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    bird = player.Bird(90, 220)
    bird_group.add(bird)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                bird.enable_fly()
                bird.jump()

        sky.draw()
        ground.update(velocity)
        bird_group.draw(screen)
        bird.update(ground.get_pos_y())

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
