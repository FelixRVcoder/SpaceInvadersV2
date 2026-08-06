"""
===========================================
Space Invader V2
player.py

Contains the Player class.

Responsibilities:
- Load the player sprite
- Move the player
- Draw the player
- Handle player lives
===========================================
"""

import os

import pygame

from settings import *


class Player:

    def __init__(self):

        print("Creating Player...")

        # Load sprite
        base_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_dir, "assets", "images", "tank.png")

        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
            self.image.fill((0, 255, 0))

        # Scale sprite (we'll tweak this later if needed)
        self.image = pygame.transform.scale(
            self.image,
            (
                PLAYER_WIDTH,
                PLAYER_HEIGHT
            )
        )

        # Create hitbox
        self.rect = self.image.get_rect()

        # Start near the bottom-center
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20

        # Player stats
        self.speed = PLAYER_SPEED
        self.lives = 3

        print("Player created!")

    def move(self, direction):
        """
        Move the player horizontally.

        direction:
            -1 = left
            1 = right
            0 = don't move
        """

        self.rect.x += direction * self.speed

        # Prevent leaving the screen
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def wants_to_shoot(self, keys):
        """
        Returns True if the player is trying to shoot.
        """

        return keys[pygame.K_SPACE]