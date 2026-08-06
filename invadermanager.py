from invader import Invader
from settings import *

import pygame


class InvaderManager:

    def __init__(self):

        print("Creating InvaderManager...")


        self.level = 1

        self.invaders = []


        self.direction = 1


        self.speed = INVADER_STEP_DISTANCE

        self.drop_distance = INVADER_DROP_DISTANCE


        self.move_delay = INVADER_STEP_DELAY

        self.minimum_delay = 60


        self.last_move = pygame.time.get_ticks()


        self.create_formation()


        print("InvaderManager ready!")



    def create_formation(self):

        self.invaders.clear()


        rows = INVADER_ROWS

        columns = INVADER_COLUMNS


        spacing_x = INVADER_SPACING_X

        spacing_y = INVADER_SPACING_Y


        formation_width = (

            (columns - 1) * spacing_x

            +

            INVADER_WIDTH

        )


        start_x = (

            SCREEN_WIDTH - formation_width

        ) // 2


        start_y = INVADER_START_Y



        for row in range(rows):

            for column in range(columns):


                x = start_x + column * spacing_x

                y = start_y + row * spacing_y


                self.invaders.append(

                    Invader(
                        x,
                        y
                    )

                )


        self.direction = 1

        self.last_move = pygame.time.get_ticks()



    def next_level(self):

        self.level += 1


        print(
            f"LEVEL {self.level}"
        )


        self.move_delay = max(

            self.minimum_delay,

            self.move_delay - 20

        )


        self.create_formation()



    def update(self):


        self.invaders = [

            invader

            for invader in self.invaders

            if invader.alive

        ]


        if not self.invaders:

            return



        current_time = pygame.time.get_ticks()



        if current_time - self.last_move < self.move_delay:

            return



        self.last_move = current_time



        # -------------------------
        # CHECK NEXT POSITION
        # -------------------------

        should_drop = False



        for invader in self.invaders:


            next_x = (

                invader.rect.x

                +

                self.direction * self.speed

            )


            if next_x < 0 or next_x + invader.rect.width > SCREEN_WIDTH:

                should_drop = True

                break




        # -------------------------
        # DROP
        # -------------------------

        if should_drop:


            self.direction *= -1


            for invader in self.invaders:

                invader.rect.y += self.drop_distance



        # -------------------------
        # MOVE
        # -------------------------

        else:


            for invader in self.invaders:

                invader.rect.x += (

                    self.direction

                    *

                    self.speed

                )