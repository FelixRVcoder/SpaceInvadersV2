"""
===============================
Invader.py
Contains the image of the invader and its states
===============================
"""

import os

import pygame

from settings import *


class Invader:

    def __init__(self, x, y):

        print("Creating Invader...")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "assets", "images", "invader.png")

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((INVADER_WIDTH, INVADER_HEIGHT), pygame.SRCALPHA)
            self.image.fill((255, 0, 255))

        self.image = pygame.transform.scale(
            self.image,
            (
                INVADER_WIDTH,
                INVADER_HEIGHT
            )
        )

        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.alive = True

        print("Invader created!")

    def destroy(self):

        self.alive = False