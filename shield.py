import pygame

from settings import *


class Shield:

    def __init__(self, x, y):

        self.blocks = []

        columns = SHIELD_WIDTH // SHIELD_BLOCK_SIZE
        rows = SHIELD_HEIGHT // SHIELD_BLOCK_SIZE

        for row in range(rows):

            for column in range(columns):

                block_x = x + column * SHIELD_BLOCK_SIZE
                block_y = y + row * SHIELD_BLOCK_SIZE

                block = pygame.Rect(
                    block_x,
                    block_y,
                    SHIELD_BLOCK_SIZE,
                    SHIELD_BLOCK_SIZE
                )

                self.blocks.append(block)

    def draw(self, screen):

        for block in self.blocks:

            pygame.draw.rect(
                screen,
                GREEN,
                block
            )