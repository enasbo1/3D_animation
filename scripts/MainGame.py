import pygame as pyg

from engine.render import Mesh
from engine.worker import GameMaster, PygIO
from scripts.Menu import Menu
from scripts.DisplayTest import DisplayTest
from scripts.MatrixRotation import ObjectRotationMatrix
from scripts.QuaternionRotation import ObjectRotationQuaternion
from scripts.UncenteredRotation import ObjectUncenteredRotation
from meshs.Pyramid import Pyramid
from meshs.Cube import Cube


class MainGame(GameMaster):
    menu: Menu
    mesh: Mesh = None
    treatment: DisplayTest | ObjectRotationMatrix | ObjectRotationQuaternion | ObjectUncenteredRotation = None
    test: DisplayTest
    matrixRotate: ObjectRotationMatrix
    quaternionRotate: ObjectRotationQuaternion
    # uncenteredRotate: ObjectUncenteredRotation

    keyPressed: int = 0

    def onCreate(self):
        self.menu = Menu()
        self.worker.show_over = self.show_over
        self.test = DisplayTest(self.worker)
        self.matrixRotate = ObjectRotationMatrix()
        self.quaternionRotate = ObjectRotationQuaternion()
        # self.uncenteredRotate = ObjectUncenteredRotation(self.worker)

    def start(self):
        pass

    def update(self):
        self.menuInputs()

        if self.treatment is not None:
            self.treatment.update()
        pass

    def show_over(self, pygIO: PygIO):

        if self.treatment is not None:
            self.treatment.show_over(pygIO)

        if self.menu.menuToDisplay == 0:
            self.menu.selectMode(pygIO)
        elif self.menu.menuToDisplay == 1:
            self.menu.selectMesh(pygIO)
        elif self.menu.menuToDisplay == 2:
            self.menu.selectTreatment(pygIO)
        pass

    def fixedUpdate(self):
        pass

    def menuInputs(self):
        if self.keyPressed != -1:
            if not self.worker.keysInput[self.keyPressed]:
                self.keyPressed = -1
            return

        if self.menu.menuToDisplay == 0:
            if self.worker.keysInput[pyg.K_0]:
                self.keyPressed = pyg.K_0
                self.changeMenu(1)
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.changeMenu(2)

        elif self.menu.menuToDisplay == 1:
            if self.worker.keysInput[pyg.K_0]:
                self.keyPressed = pyg.K_0
                self.changeMesh(Pyramid().mesh)
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.changeMesh(Cube().mesh)
            if self.worker.keysInput[pyg.K_9]:
                self.keyPressed = pyg.K_9
                self.changeMenu(0)

        elif self.menu.menuToDisplay == 2:
            if self.worker.keysInput[pyg.K_0]:
                self.keyPressed = pyg.K_0
                self.changeTreatment(None)
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.changeTreatment(self.test)
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.changeTreatment(self.matrixRotate)
            if self.worker.keysInput[pyg.K_3]:
                self.keyPressed = pyg.K_3
                self.changeTreatment(self.quaternionRotate)
            # if self.worker.keysInput[pyg.K_4]:
            #     self.keyPressed = pyg.K_4
            #     self.changeTreatment(self.uncenteredRotate)
            if self.worker.keysInput[pyg.K_9]:
                self.keyPressed = pyg.K_9
                self.changeMenu(0)

    def changeMenu(self, menu: int):
        self.menu.menuToDisplay = menu

    def changeMesh(self, mesh):
        self.worker.renderer.mesh.clear()
        self.mesh = mesh
        self.worker.renderer.mesh.append(mesh)

    def changeTreatment(self, treatment):
        if self.mesh is not None:
            self.treatment = treatment
            if self.treatment is not None:
                self.treatment.init(self.mesh)
