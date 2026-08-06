import pygame

from settings import *


class LeaderboardScreen:

    def __init__(self):

        self.title_font = pygame.font.Font(
            None,
            70
        )

        self.header_font = pygame.font.Font(
            None,
            32
        )

        self.entry_font = pygame.font.Font(
            None,
            34
        )

        self.info_font = pygame.font.Font(
            None,
            32
        )


        self.entries = []

        self.player_name = ""

        self.player_rank = None

        self.player_stats = None
        self.error_message = None

        self.active = False

        self.start_time = 0

        self.duration = 10000



    def show(
        self,
        entries,
        player_name,
        player_rank,
        player_stats,
        error_message=None
    ):

        self.entries = entries

        self.player_name = player_name

        self.player_rank = player_rank

        self.player_stats = player_stats

        self.error_message = error_message

        self.active = True

        self.start_time = pygame.time.get_ticks()



    def update(self):

        if not self.active:

            return


        if (

            pygame.time.get_ticks()

            -

            self.start_time

            >= self.duration

        ):

            self.active = False




    def draw(
        self,
        screen
    ):


        screen.fill(BLACK)



        # TITLE

        title = self.title_font.render(

            "TOP 10 LEADERBOARD",

            True,

            WHITE

        )


        screen.blit(

            title,

            title.get_rect(

                center=(

                    SCREEN_WIDTH // 2,

                    55

                )

            )

        )



        # TABLE HEADER

        headers = [

            ("RANK", 70),

            ("NAME", 180),

            ("LEVEL", 470),

            ("SCORE", 610)

        ]


        for text, x in headers:


            rendered = self.header_font.render(

                text,

                True,

                WHITE

            )


            screen.blit(

                rendered,

                (

                    x,

                    120

                )

            )



        y = 165



        # TABLE ROWS

        for position, player in enumerate(

            self.entries[:10],

            start=1

        ):


            if player["name"] == self.player_name:

                color = GREEN

            else:

                color = WHITE



            rank_text = self.entry_font.render(

                str(position),

                True,

                color

            )


            name_text = self.entry_font.render(

                player["name"],

                True,

                color

            )


            level_text = self.entry_font.render(

                str(player["level"]),

                True,

                color

            )


            score_text = self.entry_font.render(

                str(player["score"]),

                True,

                color

            )


            screen.blit(

                rank_text,

                (

                    90,

                    y

                )

            )


            screen.blit(

                name_text,

                (

                    180,

                    y

                )

            )


            screen.blit(

                level_text,

                (

                    500,

                    y

                )

            )


            screen.blit(

                score_text,

                (

                    620,

                    y

                )

            )


            y += 40




        # OUTSIDE TOP 10 PLAYER

        if (

            self.player_rank

            and

            self.player_rank > 10

            and

            self.player_stats

        ):


            rank_text = self.info_font.render(

                f"Your Rank: #{self.player_rank}",

                True,

                GREEN

            )


            stats_text = self.info_font.render(

                f"Level: {self.player_stats['level']}     "
                f"Score: {self.player_stats['score']}",

                True,

                GREEN

            )


            screen.blit(

                rank_text,

                (

                    70,

                    575

                )

            )


            screen.blit(

                stats_text,

                (

                    360,

                    575

                )

            )



        if self.error_message:

            error_text = self.info_font.render(

                self.error_message,

                True,

                RED

            )

            screen.blit(

                error_text,

                (

                    40,

                    SCREEN_HEIGHT - 50

                )

            )

        pygame.display.flip()