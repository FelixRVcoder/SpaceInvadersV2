"""
==========================
ScoreManager.py
Manages the player's score, including updating and displaying it on the screen
==========================
"""


import pygame

from settings import *


class ScoreManager:

    def __init__(self):

        self.score = 0

        self.font = pygame.font.Font(

            None,

            36

        )

    def add_score(self, amount):

        self.score += amount

    def draw(

        self,

        screen,

        player,

        level

    ):

        score_text = self.font.render(

            f"Score: {self.score}",

            True,

            BLACK

        )

        level_text = self.font.render(

            f"Level: {level}",

            True,

            BLACK

        )

        lives_text = self.font.render(

            f"Lives: {player.lives}",

            True,

            BLACK

        )

        screen.blit(

            score_text,

            (15, 10)

        )

        screen.blit(

            level_text,

            (15, 45)

        )

        screen.blit(

            lives_text,

            (SCREEN_WIDTH - 130, 10)

        )