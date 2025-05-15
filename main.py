import engine.worker as worker
from scripts.QuaternionRotation import ObjectRotationQuaternion

game = worker.Worker(ObjectRotationQuaternion())
game.start()

while game.pygIO.running:
    game.mainLoop()

game.end()
