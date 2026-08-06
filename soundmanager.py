"""
==========================
soundmanager.py
Manages the sound effects in the game, including shooting, invader death, and player damage sounds.
==========================
"""


import os

import pygame


class SoundManager:

    def __init__(self):

        pygame.mixer.init()

        base_dir = os.path.dirname(__file__)

        self.player_shoot_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "assets", "sounds", "player_shoot.ogg")
        )

        self.invader_dead_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "assets", "sounds", "invader_dead.ogg")
        )

        self.player_damage_sound = pygame.mixer.Sound(
            os.path.join(base_dir, "assets", "sounds", "player_damage.ogg")
        )

        # Volumes

        self.player_shoot_sound.set_volume(0.4)

        self.invader_dead_sound.set_volume(0.5)

        self.player_damage_sound.set_volume(0.6)

    def player_shoot(self):

        self.player_shoot_sound.play()

    def invader_dead(self):

        self.invader_dead_sound.play()

    def player_damage(self):

        self.player_damage_sound.play()