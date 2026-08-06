"""
============================
CollisionManager.py
A file which contains the collision logic for the game
============================
"""


class CollisionManager:


    def update(

        self,

        player,

        bullet_manager,

        invader_manager,

        invader_bullet_manager,

        shield_manager,

        score_manager,

        ufo_manager,

        sound_manager

    ):


        # -------------------------
        # PLAYER BULLETS
        # -------------------------

        for bullet in bullet_manager.bullets:


            if not bullet.active:

                continue



            hit = False



            # SHIELDS

            for shield in shield_manager.shields:


                collided_blocks = [

                    block

                    for block in shield.blocks

                    if bullet.rect.colliderect(block)

                ]


                if collided_blocks:


                    # Player bullet comes upward,
                    # destroy the bottom-most block first

                    block = max(

                        collided_blocks,

                        key=lambda b: b.y

                    )


                    shield.blocks.remove(block)


                    bullet.destroy()


                    hit = True

                    break



            if hit:

                continue



            # UFO

            if (

                ufo_manager.ufo.active

                and

                bullet.rect.colliderect(

                    ufo_manager.ufo.rect

                )

            ):


                bullet.destroy()


                score = ufo_manager.destroy()

                score_manager.add_score(score)


                continue




            # INVADERS

            for invader in invader_manager.invaders:


                if (

                    invader.alive

                    and

                    bullet.rect.colliderect(

                        invader.rect

                    )

                ):


                    bullet.destroy()

                    invader.destroy()

                    score_manager.add_score(10)

                    sound_manager.invader_dead()

                    break





        # -------------------------
        # ENEMY BULLETS
        # -------------------------

        for bullet in invader_bullet_manager.bullets:


            if not bullet.alive:

                continue



            hit = False



            # SHIELDS

            for shield in shield_manager.shields:


                collided_blocks = [

                    block

                    for block in shield.blocks

                    if bullet.rect.colliderect(block)

                ]



                if collided_blocks:


                    # Enemy bullet comes downward,
                    # destroy top-most block first

                    block = min(

                        collided_blocks,

                        key=lambda b: b.y

                    )


                    shield.blocks.remove(block)


                    bullet.destroy()


                    hit = True

                    break



            if hit:

                continue



            # PLAYER

            if bullet.rect.colliderect(player.rect):


                bullet.destroy()


                player.lives -= 1


                sound_manager.player_damage()