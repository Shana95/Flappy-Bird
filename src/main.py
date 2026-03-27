# pylint: disable=no-member
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
"""Main execution script for the Flappy Bird game loop."""

import random
import sys

import pygame

import player
import score
import ui
from background import Ground, Sky
from pipe import Pipe


def reset_game(bird, pipe_group):  # score_manager):
    """Riporta il gioco allo stato iniziale."""
    # Reset the bird's position and state
    bird.rect.midbottom = (90, 220)
    bird.gravity = 0
    bird.died = False
    bird.is_rotated_to_death = False
    # Reset the bird's image to the original (non-rotated) state
    bird.image = bird.original_image

    pipe_group.empty()

    # Reset the score manager if implemented
    # score_manager.reset()


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
    filename_start = "message.png"
    filename_gameover = "gameover.png"

    # the more the offset the more the ground goes down
    ground_offset = 560
    sky = Sky(filename_sky, 0, 0, canvas)
    ground = Ground(filename_ground, 0, ground_offset, canvas)

    bird_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    bird = player.Bird(90, 220)
    bird_group.add(bird)

    pipe_group: pygame.sprite.Group = pygame.sprite.Group()
    spawn_pipe_event = pygame.USEREVENT
    # Set a timer to trigger the SPAWNPIPE event
    pygame.time.set_timer(spawn_pipe_event, 2750)

    actual_score = score.Score(
        "flappyborder.ttf", "flappyfill.ttf", int(sky.get_width() / 2), 50
    )

    start_transparency = 255
    gameover_transparency = 0
    start_screen = ui.StartScreen(filename_start, 150, 305, start_transparency)
    gameover_screen = ui.GameOverScreen(
        filename_gameover, 150, 305, gameover_transparency
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
                random_y = random.randint(150, 350)
                # randomize the gap
                random_gap = random.randint(100, 130)

                # Create the pipes
                bottom_pipe = Pipe(original_width + 50, random_y, 0, random_gap)
                top_pipe = Pipe(original_width + 50, random_y, 1, random_gap)

                pipe_group.add(bottom_pipe, top_pipe)

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                if not bird.died:
                    bird.enable_fly()
                    bird.jump()

            # reset the game when r is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and bird.died:
                reset_game(bird, pipe_group)

        bird_state = bird.get_state()
        if pygame.sprite.spritecollide(
            bird, pipe_group, False, pygame.sprite.collide_mask
        ):
            bird.die()

        # Draw the game elements on the canvas
        sky.draw()
        pipe_group.draw(canvas)
        pipe_group.update(velocity, bird_state)
        ground.update(velocity, bird_state)
        start_screen.draw(bird_state, canvas)
        bird_group.draw(canvas)
        bird.update(ground.get_pos_y())
        gameover_screen.draw(bird_state, canvas)

        for pipe in pipe_group:
            if pipe.get_position() != 1 and pipe.check_passed(bird.rect.centerx):
                actual_score.scored()

        actual_score.draw(canvas)
        # Scale the canvas to fit the window
        scaled_canvas = pygame.transform.smoothscale(
            canvas, (window_width, window_height)
        )
        window.blit(scaled_canvas, (0, 0))

        pygame.display.update()
        clock.tick(fps)


if __name__ == "__main__":
    main()
