from engine.worker import PygIO
from meshs.Mesh import Mesh


class Menu:
    menuToDisplay: int = 0
    meshListOffset: int = 0

    @staticmethod
    def selectMode(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Main Menu:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: Add Mesh", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Select Object", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "2: Select Treatment", 30, "#FFFFFF", False)

    @staticmethod
    def addMesh(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Mesh to add:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: Pyramid", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Cube", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "9: Return", 30, "#FFFFFF", False)

    def changeMesh(self, pygIO: PygIO, meshList: list[Mesh]):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Mesh to add:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: up", 30, "#FFFFFF", False)

        i = 0
        while len(meshList) > i + self.meshListOffset >= 0 and i < 2:
            mesh = meshList[i + self.meshListOffset]
            boxPosY += 40
            if mesh.name is not None:
                pygIO.draw_text(boxPosX + 20, boxPosY + 100, str(i + 1) + ": " + mesh.name, 30, "#FFFFFF", False)
            else:
                pygIO.draw_text(boxPosX + 20, boxPosY + 100, str(i + 1) + ": WIP", 30, "#FFFFFF", False)
            i += 1

        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "3: down", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "9: Return", 30, "#FFFFFF", False)

    @staticmethod
    def selectTreatment(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Treatment to display:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: None", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Test treatment", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "2: Matrice rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 220, "3: Quaternion rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 260, "9: Return", 30, "#FFFFFF", False)
        pass
