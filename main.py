import asyncio
import pygame

from game import Game
from settings import *

async def load_leaderboard(game):

    try:

        await game.leaderboard_manager.submit_score(

            game.player_name,

            game.score_manager.score,

            game.level_manager.level

        )

        scores = await game.leaderboard_manager.get_top_scores()

        rank, stats = await game.leaderboard_manager.get_player_rank(

            game.player_name

        )

        game.leaderboard_screen.show(

            scores,

            game.player_name,

            rank,

            stats,

            game.leaderboard_manager.last_error

        )

    except Exception as e:

        game.leaderboard_screen.error_message = (

            f"Leaderboard error: {e}"

        )


async def main():

    game = Game()

    while game.running:

        game.handle_events()

        # ==========================================
        # MENU
        # ==========================================

        if game.in_menu:

            game.menu_manager.draw(
                game.screen
            )

            if game.menu_manager.finished:

                game.player_name = (

                    game.menu_manager.player_name

                )

                game.reset_game()

                game.in_menu = False

        # ==========================================
        # LEADERBOARD
        # ==========================================

        elif game.showing_leaderboard:

            game.leaderboard_screen.update()

            game.leaderboard_screen.draw(
                game.screen
            )

            if not game.leaderboard_screen.active:

                game.showing_leaderboard = False

                game.in_menu = True

                game.menu_manager.reset()

                game.player_name = ""

        # ==========================================
        # GAME OVER
        # ==========================================

        elif game.lose_manager.game_over:

            game.lose_manager.draw(
                game.screen
            )

            if game.lose_manager.finished():

                if not game.score_uploaded:

                    print("GAME OVER")

                    if game.leaderboard_task is None:

                        game.leaderboard_task = asyncio.create_task(

                            load_leaderboard(game)

                        )

                    game.leaderboard_screen.show(

                        [],

                        game.player_name,

                        None,

                        None,

                        "Loading leaderboard..."

                    )

                    game.score_uploaded = True

                    game.showing_leaderboard = True

                    game.leaderboard_screen.start_time = (

                        pygame.time.get_ticks()

                    )

        # ==========================================
        # GAMEPLAY
        # ==========================================

        else:

            game.update()

            game.draw()

        game.clock.tick(FPS)

        await asyncio.sleep(0)

    pygame.quit()


asyncio.run(main())