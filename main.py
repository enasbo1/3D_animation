import engine.worker as worker
from scripts.QuaternionRotation import ObjectRotationQuaternion
from scripts.MatrixRotation import ObjectRotationMatrix
from scripts.UncenteredRotation import ObjectUncenteredRotation

game = worker.Worker(ObjectRotationQuaternion())
game.start()

while game.pygIO.running:
    game.mainLoop()

game.end()
