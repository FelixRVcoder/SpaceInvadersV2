"""
===========================
ufo.py
Manages the UFO object in the game, including its spawning, movement, and destruction.
===========================
"""


import os
import random

import pygame

from settings import *


class UFO:

    def __init__(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "assets", "images", "ufo.png")

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((70, 35), pygame.SRCALPHA)
            self.image.fill((255, 0, 255))

        self.image = pygame.transform.scale(
            self.image,
            (70, 35)
        )

        self.rect = self.image.get_rect()

        self.active = False

        self.speed = 4

        self.direction = 1

        self.score = 0

    def spawn(self):

        self.active = True

        self.direction = random.choice([-1, 1])

        self.rect.y = 40

        if self.direction == 1:

            self.rect.right = 0

        else:

            self.rect.left = SCREEN_WIDTH

    def update(self):

        if not self.active:

            return

        self.rect.x += self.speed * self.direction

        if self.direction == 1:

            if self.rect.left > SCREEN_WIDTH:

                self.active = False

        else:

            if self.rect.right < 0:

                self.active = False

    def destroy(self):

        self.active = False