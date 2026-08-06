from bullet import Bullet


class BulletManager:


    def __init__(self):

        self.bullets = []



    def shoot(
        self,
        player
    ):

        bullet = Bullet(

            player.rect.centerx,

            player.rect.top

        )


        self.bullets.append(

            bullet

        )



    def update(self):


        for bullet in self.bullets:


            if not bullet.active:

                continue



            bullet.rect.y -= bullet.speed



            if bullet.rect.bottom < 0:

                bullet.destroy()



        self.bullets = [

            bullet

            for bullet in self.bullets

            if bullet.active

        ]