"""
===============================
InvaderBulletManager.py
A file which contains the firing sequence and control of the invaders bullets
===============================
"""


import random

from invaderbullet import InvaderBullet


class InvaderBulletManager:

    def __init__(self):

        self.bullets = []

    def shoot(self, invaders):

        if len(invaders) == 0:
            return

        shooter = random.choice(invaders)

        bullet = InvaderBullet(

            shooter.rect.centerx,

            shooter.rect.bottom

        )

        self.bullets.append(bullet)

    def update(self):

        for bullet in self.bullets:

            bullet.update()

        self.bullets = [

            bullet

            for bullet in self.bullets

            if bullet.alive

        ]