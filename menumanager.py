import pygame

from settings import *


class MenuManager:

    def __init__(self):

        self.title_font = pygame.font.Font(None, 96)
        self.text_font = pygame.font.Font(None, 48)
        self.input_font = pygame.font.Font(None, 56)

        self.player_name = ""

        self.max_name_length = 12

        # start -> name -> done
        self.menu_state = "start"

        self.finished = False

    def reset(self):

        self.player_name = ""
        self.menu_state = "start"
        self.finished = False

    def handle_event(self, event):

        if event.type != pygame.KEYDOWN:
            return

        # -------------------------
        # PRESS ENTER SCREEN
        # -------------------------

        if self.menu_state == "start":

            if event.key == pygame.K_RETURN:

                self.menu_state = "name"

            return

        # -------------------------
        # NAME INPUT SCREEN
        # -------------------------

        if event.key == pygame.K_BACKSPACE:

            self.player_name = self.player_name[:-1]

            return

        if event.key == pygame.K_RETURN:

            if len(self.player_name.strip()) > 0:

                self.finished = True

            return

        if (

            len(self.player_name) < self.max_name_length
            and event.unicode.isprintable()
            and event.unicode != ""

        ):

            self.player_name += event.unicode

    def draw(self, screen):

        if self.menu_state == "start":

            self.draw_start(screen)

        else:

            self.draw_name(screen)

    def draw_start(self, screen):

        screen.fill(BLACK)

        title = self.title_font.render(
            "SPACE INVADERS",
            True,
            WHITE
        )

        screen.blit(

            title,

            title.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    SCREEN_HEIGHT // 2 - 80

                )

            )

        )

        press = self.text_font.render(

            "Press ENTER to Begin",

            True,

            WHITE

        )

        screen.blit(

            press,

            press.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    SCREEN_HEIGHT // 2 + 20

                )

            )

        )

        pygame.display.flip()

    def draw_name(self, screen):

        screen.fill(BLACK)

        title = self.text_font.render(

            "ENTER YOUR NAME",

            True,

            WHITE

        )

        screen.blit(

            title,

            title.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    SCREEN_HEIGHT // 2 - 80

                )

            )

        )

        name = self.input_font.render(

            self.player_name + "_",

            True,

            WHITE

        )

        screen.blit(

            name,

            name.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    SCREEN_HEIGHT // 2

                )

            )

        )

        hint = self.text_font.render(

            "Press ENTER when ready",

            True,

            WHITE

        )

        screen.blit(

            hint,

            hint.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    SCREEN_HEIGHT // 2 + 80

                )

            )

        )

        pygame.display.flip()