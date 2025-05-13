import engine.worker as worker
import scripts.MainGame as mg
import backwork.affichage

game = worker.Worker(mg.MainGame())
game.start()

while game.pygIO.running:
    game.mainLoop()

game.end()
