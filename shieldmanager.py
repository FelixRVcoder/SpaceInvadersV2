"""
===========================
shieldmanager.py
Manages the shield objects in the game, including their creation, rendering, and collision detection with bullets.
===========================
"""


from shield import Shield

from settings import *


class ShieldManager:

    def __init__(self):

        self.shields = []

        self.create_shields()

    def create_shields(self):

        spacing = SCREEN_WIDTH // (SHIELD_COUNT + 1)

        y = SCREEN_HEIGHT - SHIELD_Y_OFFSET

        for i in range(SHIELD_COUNT):

            x = spacing * (i + 1) - SHIELD_WIDTH // 2

            self.shields.append(

                Shield(x, y)

            )

    def draw(self, screen):

        for shield in self.shields:

            shield.draw(screen)