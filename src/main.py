# pylint: disable=no-member
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
"""Main execution script for the Flappy Bird game loop."""

import random
import sys

import pygame

import player
import reset
import score
import settings
import ui
from background import Ground, Sky
from pipe import Pipe


def main() -> None:
    """Initialize the game engine and manage the real-time event loop."""
    pygame.init()

    # Get the current monitor height
    screen_info = pygame.display.Info()
    monitor_height = screen_info.current_h
    # Optional offset to adjust the window width if needed
    offset = 0

    # Set the window height to 90% of the monitor height
    window_height = int(monitor_height * 0.90)
    # Scale the screen dimensions
    scale = window_height / settings.ORIGINAL_HEIGHT
    window_width = int(settings.ORIGINAL_WIDTH * scale + offset)

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Flappy Bird")
    # Create a canvas surface to draw the game elements, which will be scaled to fit the window
    canvas = pygame.Surface((settings.ORIGINAL_WIDTH, settings.ORIGINAL_HEIGHT))
    clock = pygame.time.Clock()

    # the more the offset the more the ground goes down
    sky = Sky(settings.FILE_SKY, settings.SKY_POS_X, settings.SKY_POS_Y, canvas)
    ground = Ground(
        settings.FILE_GROUND, settings.GROUND_POS_X, settings.GROUND_POS_Y, canvas
    )

    bird_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    bird = player.Bird(settings.BIRD_START_X, settings.BIRD_START_Y)
    bird_group.add(bird)

    pipe_group: pygame.sprite.Group = pygame.sprite.Group()
    spawn_pipe_event = pygame.USEREVENT
    # Set a timer to trigger the SPAWNPIPE event
    pygame.time.set_timer(spawn_pipe_event, settings.SPAWN_PIPE_TIMER)

    actual_score = score.Score(
        settings.FONT_BORDER,
        settings.FONT_FILL,
        int(sky.get_width() / 2),
        settings.SCORE_POS_Y,
    )

    start_screen = ui.StartScreen(
        settings.FILE_START,
        settings.START_SCREEN_X,
        settings.START_SCREEN_Y,
        settings.START_TRANSPARENCY_INIT,
        settings.START_TRANSPARENCY_TARGET,
    )
    gameover_screen = ui.GameOverScreen(
        settings.FILE_GAMEOVER,
        settings.GAMEOVER_SCREEN_X,
        settings.GAMEOVER_SCREEN_Y,
        settings.GAMEOVER_TRANSPARENCY_INIT,
        settings.GAMEOVER_TRANSPARENCY_TARGET,
    )

    game_loop = True

    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                pygame.quit()
                sys.exit()

            if event.type == spawn_pipe_event and bird.fly and not bird.died:
                # Generate random vertical position and gap size for the new pipes
                random_y = random.randint(settings.PIPE_MIN_Y, settings.PIPE_MAX_Y)
                # randomize the gap
                random_gap = random.randint(
                    settings.PIPE_GAP_MIN, settings.PIPE_GAP_MAX
                )

                # Create the pipes
                bottom_pipe = Pipe(
                    settings.ORIGINAL_WIDTH + 50, random_y, 0, random_gap
                )
                top_pipe = Pipe(settings.ORIGINAL_WIDTH + 50, random_y, 1, random_gap)

                pipe_group.add(bottom_pipe, top_pipe)

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                if not bird.died:
                    bird.enable_fly()
                    bird.jump()

            # reset the game when r or MOUSERIGHT is pressed
            if (
                (event.type == pygame.KEYDOWN and event.key == pygame.K_r)
                or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3)
                and bird.died
            ):

                reset.reset_game(
                    bird, pipe_group, actual_score, start_screen, gameover_screen
                )

        bird_state = bird.get_state()
        if pygame.sprite.spritecollide(
            bird, pipe_group, False, pygame.sprite.collide_mask
        ):
            bird.die()

        # Draw the game elements on the canvas
        sky.draw()
        pipe_group.draw(canvas)
        pipe_group.update(settings.VELOCITY, bird_state)
        ground.update(settings.VELOCITY, bird_state)
        start_screen.draw(bird_state, canvas)
        bird_group.draw(canvas)
        bird.update(ground.get_pos_y())
        gameover_screen.draw(bird_state, canvas)

        for pipe in pipe_group:
            if pipe.get_position() != 1 and pipe.check_passed(bird.rect.centerx):
                actual_score.scored()

        actual_score.draw(
            start_screen.target_transparency_reached(), canvas, bird_state
        )
        # Scale the canvas to fit the window
        scaled_canvas = pygame.transform.smoothscale(
            canvas, (window_width, window_height)
        )
        window.blit(scaled_canvas, (0, 0))

        pygame.display.update()
        clock.tick(settings.FPS)


if __name__ == "__main__":
    main()
