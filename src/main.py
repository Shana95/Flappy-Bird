# pylint: disable=no-member
"""Main execution script for the Flappy Bird game loop."""

# pylint: disable=too-many-locals

import sys

import pygame

import player
from background import Ground, Sky


def main() -> None:
    """Initialize the game engine and manage the real-time event loop."""
    pygame.init()
    original_width = 288
    original_height = 512

    # Get the current monitor height
    screen_info = pygame.display.Info()
    monitor_height = screen_info.current_h
    # Optional offset to adjust the window width if needed
    offset = 0

    # Set the window height to 90% of the monitor height
    window_height = int(monitor_height * 0.90)
    # Scale the screen dimensions
    scale = window_height / original_height
    window_width = int(original_width * scale + offset)

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Flappy Bird")
    # Create a canvas surface to draw the game elements, which will be scaled to fit the window
    canvas = pygame.Surface((original_width, original_height))
    clock = pygame.time.Clock()
    fps = 60

    velocity = 1

    filename_sky = "background-day.png"
    filename_ground = "base.png"

    sky = Sky(filename_sky, 0, 0, canvas)
    ground = Ground(filename_ground, 0, sky.get_height(), canvas)

    bird_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    bird = player.Bird(90, 220)
    bird_group.add(bird)

    game_loop = True

    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                bird.enable_fly()
                bird.jump()

        bird_state = bird.get_state()

        # Draw the game elements on the canvas
        sky.draw()
        ground.update(velocity, bird_state)
        bird_group.draw(canvas)
        bird.update(ground.get_pos_y())

        # Scale the canvas to fit the window
        scaled_canvas = pygame.transform.smoothscale(
            canvas, (window_width, window_height)
        )
        window.blit(scaled_canvas, (0, 0))

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
