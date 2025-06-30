from engine.worker import PygIO
from meshs.Mesh import Mesh

MENU_KEYS = {
    "SELECT_MODE": 0,
    "ADD_MESH": 1,
    "CHANGE_MESH": 2,
    "SELECT_TREATMENT": 3,
    "SET_MESH_ROTATION": 4
}


class Menu:
    menuToDisplay: int = 0
    meshListOffset: int = 0
    rotationSet: int = 0

    @staticmethod
    def selectMode(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Main Menu:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "1: Add Mesh", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "2: Select Object", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "3: Select Treatment", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 220, "4: Set Mesh Quaternion", 30, "#FFFFFF", False)

    @staticmethod
    def addMesh(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Mesh to add:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "1: Pyramid", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "2: Cube", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "0: Return", 30, "#FFFFFF", False)

    def changeMesh(self, pygIO: PygIO, meshList: list[Mesh]):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Select mesh:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "1: ^", 30, "#FFFFFF", False)

        i = 0
        while len(meshList) > i + self.meshListOffset >= 0 and i < 2:
            mesh = meshList[i + self.meshListOffset]
            boxPosY += 40
            if mesh.name is not None:
                pygIO.draw_text(boxPosX + 20, boxPosY + 100, str(i + 2) + ": " + mesh.name, 30, "#FFFFFF", False)
            else:
                pygIO.draw_text(boxPosX + 20, boxPosY + 100, str(i + 2) + ": None(WIP)", 30, "#FFFFFF", False)
            i += 1

        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "4: v", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "0: Return", 30, "#FFFFFF", False)

    @staticmethod
    def selectTreatment(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Treatment to display:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "1: None", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "2: Test treatment", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "3: Matrice rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 220, "4: Quaternion rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 260, "0: Return", 30, "#FFFFFF", False)
        pass

    def setRotation(self, pygIO: PygIO, inputText: str):
        boxPosX = -pygIO.width // 2
        boxPosY = pygIO.height // 2 - 300
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Set rotation:", 30, "#FFFFFF", False)
        if self.rotationSet == 0:
            pygIO.draw_text(boxPosX + 20, boxPosY + 100, "R: " + inputText, 30, "#FFFFFF", False)
        elif self.rotationSet == 1:
            pygIO.draw_text(boxPosX + 20, boxPosY + 100, "I: " + inputText, 30, "#FFFFFF", False)
        elif self.rotationSet == 2:
            pygIO.draw_text(boxPosX + 20, boxPosY + 100, "J: " + inputText, 30, "#FFFFFF", False)
        elif self.rotationSet == 3:
            pygIO.draw_text(boxPosX + 20, boxPosY + 100, "K: " + inputText, 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 260, "N: Next", 30, "#FFFFFF", False)
        pass
