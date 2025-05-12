from engine.worker import GameMaster, PygIO


class MainGame(GameMaster):

    def onCreate(self):
        self.worker.show_over = self.show_over

    def start(self):
        pass

    def update(self):
        pass

    def show_over(self, pygIO: PygIO):
        pass

    def fixedUpdate(self):
        pass
