import random
import pygame

from ufo import UFO


class UFOManager:

    def __init__(self):

        self.ufo = UFO()

        self.spawn_delay = random.randint(
            20000,
            40000
        )

        self.last_spawn = pygame.time.get_ticks()

    def update(self):

        current_time = pygame.time.get_ticks()

        if (

            not self.ufo.active

            and current_time - self.last_spawn >= self.spawn_delay

        ):

            self.ufo.spawn()

            self.last_spawn = current_time

            self.spawn_delay = random.randint(

                20000,

                40000

            )

        self.ufo.update()

    def destroy(self):

        self.ufo.score = random.choice(

            [

                50,

                100,

                150,

                200,

                250,

                300

            ]

        )

        score = self.ufo.score

        self.ufo.destroy()

        return score