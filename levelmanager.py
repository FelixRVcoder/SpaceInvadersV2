class LevelManager:

    def __init__(self, invader_manager):

        self.level = 1

        self.invader_manager = invader_manager

    def update(self):

        if len(self.invader_manager.invaders) == 0:

            self.level += 1

            print(f"LEVEL {self.level}")

            self.invader_manager.next_level()