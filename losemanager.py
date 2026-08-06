import pygame

from settings import *


class LoseManager:

    def __init__(self):

        self.game_over = False

        self.font = pygame.font.Font(

            None,

            96

        )

        self.game_over_time = 0

    def update(

        self,

        player,

        invader_manager,

        shield_manager

    ):

        if self.game_over:

            return

        # -------------------------
        # Player died
        # -------------------------

        if player.lives <= 0:

            self.game_over = True

            self.game_over_time = pygame.time.get_ticks()

            return

        # -------------------------
        # Invaders reached shields
        # -------------------------

        for invader in invader_manager.invaders:

            for shield in shield_manager.shields:

                for block in shield.blocks:

                    if invader.rect.colliderect(block):

                        self.game_over = True

                        self.game_over_time = pygame.time.get_ticks()

                        return

    def draw(

        self,

        screen

    ):

        screen.fill(BLACK)

        text = self.font.render(

            "GAME OVER",

            True,

            WHITE

        )

        rect = text.get_rect(

            center=(

                SCREEN_WIDTH // 2,

                SCREEN_HEIGHT // 2

            )

        )

        screen.blit(

            text,

            rect

        )

        pygame.display.flip()

    def finished(self):

        return (

            pygame.time.get_ticks()

            - self.game_over_time

            >= 2500

        )