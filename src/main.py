# pylint: disable=no-member
# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=line-too-long
# pylint: disable=too-many-branches
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

    # ==========================================
    # 1. INITIALIZATION & ASSETS
    # ==========================================
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()

    sfx_wing = pygame.mixer.Sound(f"../assets/Sound Effects/{settings.SFX_WING}")
    sfx_point = pygame.mixer.Sound(f"../assets/Sound Effects/{settings.SFX_POINT}")
    sfx_hit = pygame.mixer.Sound(f"../assets/Sound Effects/{settings.SFX_HIT}")
    sfx_die = pygame.mixer.Sound(f"../assets/Sound Effects/{settings.SFX_DIE}")
    sfx_swoosh = pygame.mixer.Sound(f"../assets/Sound Effects/{settings.SFX_SWOOSH}")

    # ==========================================
    # 2. DISPLAY & CANVAS CONFIGURATION
    # ==========================================
    screen_info = pygame.display.Info()

    monitor_height = screen_info.current_h
    window_height = int(monitor_height * 0.90)
    scale = window_height / settings.ORIGINAL_HEIGHT
    window_width = int(settings.ORIGINAL_WIDTH * scale)

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Flappy Bird")

    canvas = pygame.Surface((settings.ORIGINAL_WIDTH, settings.ORIGINAL_HEIGHT))
    clock = pygame.time.Clock()

    # ==========================================
    # 3. GAME OBJECTS INSTANTIATION
    # ==========================================
    sky = Sky(settings.FILE_SKY, settings.SKY_POS_X, settings.SKY_POS_Y, canvas)
    ground = Ground(
        settings.FILE_GROUND, settings.GROUND_POS_X, settings.GROUND_POS_Y, canvas
    )

    bird_group: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
    bird = player.Bird(settings.BIRD_START_X, settings.BIRD_START_Y)
    bird_group.add(bird)

    pipe_group: pygame.sprite.Group = pygame.sprite.Group()
    spawn_pipe_event = pygame.USEREVENT
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

    # ==========================================
    # 4. MAIN GAME LOOP
    # ==========================================
    game_loop = True
    while game_loop:

        # --- A. Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False
                pygame.quit()
                sys.exit()

            # Game Reset Input
            if bird.is_dead() and (
                (event.type == pygame.KEYDOWN and event.key == pygame.K_r)
                or (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3)
            ):
                sfx_swoosh.play()
                reset.reset_game(
                    bird, pipe_group, actual_score, start_screen, gameover_screen
                )

            # Pipe Spawning
            if (
                event.type == spawn_pipe_event
                and bird.is_flying()
                and not bird.is_dead()
            ):
                random_y = random.randint(settings.PIPE_MIN_Y, settings.PIPE_MAX_Y)
                random_gap = random.randint(
                    settings.PIPE_GAP_MIN, settings.PIPE_GAP_MAX
                )

                bottom_pipe = Pipe(
                    settings.ORIGINAL_WIDTH + 50, random_y, 0, random_gap
                )
                top_pipe = Pipe(settings.ORIGINAL_WIDTH + 50, random_y, 1, random_gap)

                pipe_group.add(bottom_pipe, top_pipe)

            # Bird Jump Input
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or (
                event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
            ):
                if not bird.is_dead():
                    sfx_wing.play()
                    bird.enable_fly()
                    bird.jump()

        # --- B. Game Logic & Collisions ---
        bird_state = bird.get_state()
        if pygame.sprite.spritecollide(
            bird, pipe_group, False, pygame.sprite.collide_mask  # type: ignore
        ):
            if not bird.is_dead():
                bird.die()
                sfx_hit.play()
                sfx_die.play()

        if bird.current_bottom() >= ground.get_pos_y():
            if not bird.is_dead():
                sfx_hit.play()
                bird.die()

        # Score Logic
        for pipe in pipe_group:
            if pipe.get_position() != 1 and pipe.check_passed(bird.get_centerx()):
                actual_score.scored()
                sfx_point.play()

        # --- C. Rendering & Updates ---
        sky.draw()
        pipe_group.draw(canvas)
        pipe_group.update(settings.VELOCITY, bird_state)
        ground.update(settings.VELOCITY, bird_state)
        start_screen.draw(bird_state, canvas)
        bird_group.draw(canvas)
        bird.update(ground.get_pos_y())
        gameover_screen.draw(bird_state, canvas)

        actual_score.draw(
            start_screen.target_transparency_reached(), canvas, bird_state
        )

        # --- D. Display Scaling & Tick ---
        scaled_canvas = pygame.transform.smoothscale(
            canvas, (window_width, window_height)
        )
        window.blit(scaled_canvas, (0, 0))

        pygame.display.update()
        clock.tick(settings.FPS)


if __name__ == "__main__":
    main()
