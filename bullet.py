"""
==========================
Bullet.py
A file which contains the bullets form and states
DOES NOT CONTROL COLLISIONS OR FIRING, ONLY THE BULLET ITSELF
==========================
"""



import pygame

from settings import *


class Bullet:

    def __init__(self, x, y):

        self.width = 4
        self.height = 20

        self.rect = pygame.Rect(
            x - self.width // 2,
            y,
            self.width,
            self.height
        )

        self.speed = USER_BULLET_SPEED

        self.active = True

    def update(self):

        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.active = False
    
    def destroy(self):

        self.active = False