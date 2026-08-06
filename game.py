import pygame

from settings import *

from player import Player
from bulletmanager import BulletManager
from invadermanager import InvaderManager
from invaderbulletmanager import InvaderBulletManager
from shieldmanager import ShieldManager
from scoremanager import ScoreManager

from rendermanager import RenderManager
from collisionmanager import CollisionManager
from levelmanager import LevelManager
from losemanager import LoseManager
from ufomanager import UFOManager
from soundmanager import SoundManager

from menumanager import MenuManager

from leaderboardmanager import LeaderboardManager
from leaderboardscreen import LeaderboardScreen



class Game:


    def __init__(self):

        pygame.init()


        self.screen = pygame.display.set_mode(
            (
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
        )


        pygame.display.set_caption(
            WINDOW_TITLE
        )


        self.clock = pygame.time.Clock()

        self.running = True


        # MENU

        self.menu_manager = MenuManager()

        self.in_menu = True

        self.player_name = ""



        # OBJECTS

        self.player = Player()

        self.bullet_manager = BulletManager()

        self.invader_manager = InvaderManager()

        self.invader_bullet_manager = InvaderBulletManager()

        self.shield_manager = ShieldManager()

        self.score_manager = ScoreManager()

        self.render_manager = RenderManager()

        self.sound_manager = SoundManager()

        self.collision_manager = CollisionManager()

        self.level_manager = LevelManager(
            self.invader_manager
        )

        self.lose_manager = LoseManager()

        self.ufo_manager = UFOManager()



        # LEADERBOARD

        self.leaderboard_manager = LeaderboardManager()

        self.leaderboard_screen = LeaderboardScreen()

        self.score_uploaded = False

        self.showing_leaderboard = False

        self.leaderboard_task = None



        # SHOOTING

        self.space_was_pressed = False

        self.last_shot_time = 0

        self.last_enemy_shot = pygame.time.get_ticks()

        self.enemy_shot_delay = 1500



    def run(self):


        while self.running:


            self.handle_events()



            if self.in_menu:


                self.menu_manager.draw(
                    self.screen
                )


                if self.menu_manager.finished:

                    self.player_name = self.menu_manager.player_name

                    self.in_menu = False



            elif self.showing_leaderboard:


                self.leaderboard_screen.update()

                self.leaderboard_screen.draw(
                    self.screen
                )


            elif self.lose_manager.game_over:


                self.lose_manager.draw(
                    self.screen
                )



                if not self.score_uploaded:


                    print("GAME OVER")



                    # TEMPORARY BYPASS
                    # Prevents pygbag from freezing

                    self.leaderboard_screen.show(

                        [],

                        self.player_name,

                        None,

                        None

                    )


                    self.score_uploaded = True

                    self.showing_leaderboard = True



            else:


                self.update()

                self.draw()



            self.clock.tick(FPS)



        pygame.quit()




    def handle_events(self):


        for event in pygame.event.get():


            if event.type == pygame.QUIT:

                self.running = False



            if self.in_menu:

                self.menu_manager.handle_event(event)





    def update(self):


        keys = pygame.key.get_pressed()


        direction = 0


        if keys[pygame.K_LEFT]:

            direction -= 1


        if keys[pygame.K_RIGHT]:

            direction += 1



        self.player.move(direction)



        current_time = pygame.time.get_ticks()


        shooting = self.player.wants_to_shoot(keys)



        if (

            shooting

            and not self.space_was_pressed

            and current_time - self.last_shot_time >= COOLDOWN

        ):


            self.bullet_manager.shoot(
                self.player
            )


            self.sound_manager.player_shoot()


            self.last_shot_time = current_time



        self.space_was_pressed = shooting



        self.bullet_manager.update()

        self.invader_bullet_manager.update()

        self.invader_manager.update()

        self.ufo_manager.update()



        if current_time - self.last_enemy_shot >= self.enemy_shot_delay:


            self.invader_bullet_manager.shoot(

                self.invader_manager.invaders

            )


            self.last_enemy_shot = current_time




        self.collision_manager.update(

            self.player,

            self.bullet_manager,

            self.invader_manager,

            self.invader_bullet_manager,

            self.shield_manager,

            self.score_manager,

            self.ufo_manager,

            self.sound_manager

        )



        self.level_manager.update()



        self.lose_manager.update(

            self.player,

            self.invader_manager,

            self.shield_manager

        )






    def draw(self):


        self.render_manager.draw(

            self.screen,

            self.player,

            self.bullet_manager,

            self.invader_manager,

            self.invader_bullet_manager,

            self.shield_manager,

            self.score_manager,

            self.level_manager.level,

            self.ufo_manager

        )