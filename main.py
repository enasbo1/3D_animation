import engine.worker as worker
import scripts.MainGame as mg

game = worker.Worker(mg.MainGame())
game.start()

while game.pygIO.running:
    game.mainLoop()

game.end()
