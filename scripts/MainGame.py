import pygame as pyg

from backwork.Vector3D import Vector3D
from engine.worker import GameMaster, PygIO
from scripts.Menu import Menu
from scripts.DisplayTest import DisplayTest
from scripts.MatrixRotation import ObjectRotationMatrix
from scripts.QuaternionRotation import ObjectRotationQuaternion
from scripts.Transform3D import Transform3D
from meshs.Mesh import Mesh
from meshs.Cube import Cube
from meshs.Pyramid import Pyramid


class MainGame(GameMaster):
    menu: Menu
    treatment: DisplayTest | ObjectRotationMatrix | ObjectRotationQuaternion = None

    mesh: Mesh = None
    meshList: list[Mesh] = list()
    transform: Transform3D

    test: DisplayTest
    matrixRotate: ObjectRotationMatrix
    quaternionRotate: ObjectRotationQuaternion

    cube: Mesh
    pyramid: Mesh

    keyPressed: int = 0

    def onCreate(self):
        self.transform = Transform3D()
        self.menu = Menu()
        self.worker.show_over = self.show_over
        self.test = DisplayTest(self.worker)
        self.matrixRotate = ObjectRotationMatrix(self.worker, self.transform)
        self.quaternionRotate = ObjectRotationQuaternion(self.worker, self.transform)
        self.transform.position = Vector3D(10, 0, 0)
        self.meshList.append(Mesh(transform=self.transform))

    def start(self):
        pass

    def update(self):
        self.menuInputs()
        if self.mesh is not None:
            if self.worker.keysInput[pyg.K_q]:
                self.mesh.transform.position += Vector3D(0, 1, 0) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_d]:
                self.mesh.transform.position += Vector3D(0, -1, 0) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_z]:
                self.mesh.transform.position += Vector3D(1, 0, 0) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_s]:
                self.mesh.transform.position += Vector3D(-1, 0, 0) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_f]:
                self.mesh.transform.position += Vector3D(0, 0, 1) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_r]:
                self.mesh.transform.position += Vector3D(0, 0, -1) * self.worker.deltaTime

            if self.worker.keysInput[pyg.K_o]:
                self.mesh.scale(1 + self.worker.deltaTime)

            if self.worker.keysInput[pyg.K_i]:
                self.mesh.scale(1 - self.worker.deltaTime)
        pass

    def show_over(self, pygIO: PygIO):

        if self.treatment is not None:
            self.treatment.show_over(pygIO)

        if self.menu.menuToDisplay == 0:
            self.menu.selectMode(pygIO)
        elif self.menu.menuToDisplay == 1:
            self.menu.addMesh(pygIO)
        elif self.menu.menuToDisplay == 2:
            self.menu.changeMesh(pygIO, self.meshList)
        elif self.menu.menuToDisplay == 3:
            self.menu.selectTreatment(pygIO)
        pass

    def fixedUpdate(self):
        if self.treatment is not None:
            self.treatment.update()

    def menuInputs(self):
        if self.keyPressed != -1:
            if not self.worker.keysInput[self.keyPressed]:
                self.keyPressed = -1
            return

        if self.menu.menuToDisplay == 0:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.changeMenu(1)
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.changeMenu(2)
            if self.worker.keysInput[pyg.K_3]:
                self.keyPressed = pyg.K_3
                self.changeMenu(3)

        elif self.menu.menuToDisplay == 1:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.addMesh(0)
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.addMesh(1)

        elif self.menu.menuToDisplay == 2:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.menu.meshListOffset -= 1
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.changeMesh(1)
            if self.worker.keysInput[pyg.K_3]:
                self.keyPressed = pyg.K_3
                self.changeMesh(2)
            if self.worker.keysInput[pyg.K_4]:
                self.keyPressed = pyg.K_4
                self.menu.meshListOffset += 1

        elif self.menu.menuToDisplay == 3:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.changeTreatment(None)
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.changeTreatment(self.test)
            if self.worker.keysInput[pyg.K_3]:
                self.keyPressed = pyg.K_3
                self.changeTreatment(self.matrixRotate)
            if self.worker.keysInput[pyg.K_4]:
                self.keyPressed = pyg.K_4
                self.changeTreatment(self.quaternionRotate)

        if self.worker.keysInput[pyg.K_0]:
            self.keyPressed = pyg.K_0
            self.changeMenu(0)

    def changeMenu(self, menu: int):
        self.menu.menuToDisplay = menu

    def addMesh(self, meshType: int):
        if meshType == 0:
            mesh = Pyramid(transform=Transform3D())
        else:
            mesh = Cube(transform=Transform3D())
        mesh.transform.position = Vector3D(10, 0, 0)

        self.mesh = mesh
        self.meshList.append(mesh)
        self.worker.renderer.mesh.append(mesh)

    def changeMesh(self, meshIndex: int):
        meshIndex += self.menu.meshListOffset - 1
        if meshIndex < len(self.meshList):
            self.mesh = self.meshList[meshIndex]

    def changeTreatment(self, treatment):
        if self.mesh is not None:

            self.treatment = treatment
            if self.treatment is not None:
                self.treatment.init(self.mesh)
                self.treatment.transform = self.mesh.transform
