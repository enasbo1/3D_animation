from engine.worker import PygIO


class Menu:
    menuToDisplay: int = 0

    @staticmethod
    def selectMode(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = 200
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Main Menu:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: Select Mesh and Reset", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Select Treatment", 30, "#FFFFFF", False)

    @staticmethod
    def selectMesh(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = 200
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Mesh to display:", 30, "#FFFFFF", False)
        # pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: Pyramid", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Cube", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "9: Return", 30, "#FFFFFF", False)


    @staticmethod
    def selectTreatment(pygIO: PygIO):
        boxPosX = -pygIO.width // 2
        boxPosY = 200
        pygIO.draw_rect(boxPosX, boxPosY + 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPosX + 20, boxPosY + 60, "Treatment to display:", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 100, "0: None", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 140, "1: Test treatment", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 180, "2: Matrice rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 220, "3: Quaternion rotation", 30, "#FFFFFF", False)
        pygIO.draw_text(boxPosX + 20, boxPosY + 300, "9: Return", 30, "#FFFFFF", False)
        pass
