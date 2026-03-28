"""Module containing game state management and reset logic."""

import pygame

import player
from score import Score
from ui import GameOverScreen, StartScreen


def reset_game(
    bird: player.Bird,
    pipe_group: pygame.sprite.Group,
    score: Score,
    start_screen: StartScreen,
    gameover_screen: GameOverScreen,
):
    """
    Reset all game entities to their initial states for a new match.

    This function restores the UI screens' transparency, resets the bird's
    position and physics, clears all pipes from the screen, and resets the score.
    """
    start_screen.reset()
    gameover_screen.reset()
    bird.reset()
    pipe_group.empty()
    score.reset()
