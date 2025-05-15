import engine.worker as worker
from scripts.QuaternionRotation import ObjectRotationQuaternion
from scripts.MatrixRotation import ObjectRotationMatrix
from scripts.UncenteredRotation import ObjectUncenteredRotation

game = worker.Worker(ObjectRotationQuaternion())
game.start()

def main():
    game = worker.Worker(Menu())
    print("Exemple to display:")
    print("0: Display Test")
    print("1: Point rotation")
    print("2: Matrice rotation")
    print("3: Quaternion rotation")
    print("4: Not Centered Rotation")
    scriptToLaunch = input()

    if scriptToLaunch == "0":
        game = worker.Worker(Menu())
    elif scriptToLaunch == "1":
        game = worker.Worker(mg.MainGame())
    elif scriptToLaunch == "2":
        game = worker.Worker(mg.MainGame())
    elif scriptToLaunch == "3":
        game = worker.Worker(mg.MainGame())
    elif scriptToLaunch == "4":
        game = worker.Worker(mg.MainGame())
    else:
        return 0

    game.start()

    while game.pygIO.running:
        game.mainLoop()

    game.end()


main()
