import pygame

from settings import *


class RenderManager:

    def draw(

        self,

        screen,

        player,

        bullet_manager,

        invader_manager,

        invader_bullet_manager,

        shield_manager,

        score_manager,

        level,

        ufo_manager

    ):

        screen.fill(BACKGROUND_COLOR)

        # -------------------------
        # UFO
        # -------------------------

        if ufo_manager.ufo.active:

            screen.blit(

                ufo_manager.ufo.image,

                ufo_manager.ufo.rect

            )

        # -------------------------
        # Shields
        # -------------------------

        shield_manager.draw(screen)

        # -------------------------
        # Player
        # -------------------------

        screen.blit(

            player.image,

            player.rect

        )

        # -------------------------
        # Invaders
        # -------------------------

        for invader in invader_manager.invaders:

            screen.blit(

                invader.image,

                invader.rect

            )

        # -------------------------
        # Player bullets
        # -------------------------

        for bullet in bullet_manager.bullets:

            pygame.draw.rect(

                screen,

                RED,

                bullet.rect

            )

        # -------------------------
        # Enemy bullets
        # -------------------------

        for bullet in invader_bullet_manager.bullets:

            pygame.draw.rect(

                screen,

                BLUE,

                bullet.rect

            )

        score_manager.draw(

            screen,

            player,

            level

        )

        pygame.display.flip()