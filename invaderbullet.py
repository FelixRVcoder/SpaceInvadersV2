import pygame

from settings import *


class InvaderBullet:

    def __init__(self, x, y):

        self.rect = pygame.Rect(
            x,
            y,
            BULLET_WIDTH,
            BULLET_HEIGHT
        )

        self.speed = INVADER_BULLET_SPEED

        self.alive = True

    def update(self):

        self.rect.y += self.speed

        if self.rect.top > SCREEN_HEIGHT:

            self.alive = False

    def destroy(self):

        self.alive = False