import engine.worker as worker
from scripts.MainGame import MainGame

game = worker.Worker(MainGame())
game.start()

while game.pygIO.running:
    game.mainLoop()

game.end()
