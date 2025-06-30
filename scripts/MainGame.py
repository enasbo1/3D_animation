import pygame as pyg

from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from engine.worker import GameMaster, PygIO
from scripts.Menu import Menu, MENU_KEYS
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
    inputText: str = "0"
    newQtn = list[float]

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

        if self.menu.menuToDisplay == MENU_KEYS["SELECT_MODE"]:
            self.menu.selectMode(pygIO)
        elif self.menu.menuToDisplay == MENU_KEYS["ADD_MESH"]:
            self.menu.addMesh(pygIO)
        elif self.menu.menuToDisplay == MENU_KEYS["CHANGE_MESH"]:
            self.menu.changeMesh(pygIO, self.meshList)
        elif self.menu.menuToDisplay == MENU_KEYS["SELECT_TREATMENT"]:
            self.menu.selectTreatment(pygIO)
        elif self.menu.menuToDisplay == MENU_KEYS["SET_MESH_ROTATION"]:
            self.menu.setRotation(pygIO, self.inputText)
        pass

    def fixedUpdate(self):
        # if self.mesh is not None and self.mesh.animationPlay:
        #     self.mesh.playAnim()

        if self.treatment is not None:
            self.treatment.update()

    def menuInputs(self):
        if self.keyPressed != -1:
            if not self.worker.keysInput[self.keyPressed]:
                self.keyPressed = -1
            return

        if self.menu.menuToDisplay == MENU_KEYS["SELECT_MODE"]:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.menu.meshListOffset -= 1
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.changeMenu(self.menu.meshListOffset + 1)
            if self.worker.keysInput[pyg.K_3]:
                self.keyPressed = pyg.K_3
                self.changeMenu(self.menu.meshListOffset + 2)
            if self.worker.keysInput[pyg.K_4]:
                self.keyPressed = pyg.K_4
                self.changeMenu(self.menu.meshListOffset + 3)
            if self.worker.keysInput[pyg.K_5]:
                self.keyPressed = pyg.K_5
                self.menu.meshListOffset += 1

        elif self.menu.menuToDisplay == MENU_KEYS["ADD_MESH"]:
            if self.worker.keysInput[pyg.K_1]:
                self.keyPressed = pyg.K_1
                self.addMesh(0)
            if self.worker.keysInput[pyg.K_2]:
                self.keyPressed = pyg.K_2
                self.addMesh(1)

        elif self.menu.menuToDisplay == MENU_KEYS["CHANGE_MESH"]:
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

        elif self.menu.menuToDisplay == MENU_KEYS["SELECT_TREATMENT"]:
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

        elif self.menu.menuToDisplay == MENU_KEYS["SET_MESH_ROTATION"]:
            if self.menu.rotationSet >= 4:
                self.mesh.transform.rotation = Quaternion(
                    self.newQtn[0],
                    self.newQtn[1],
                    self.newQtn[2],
                    self.newQtn[3]
                )
                self.changeMenu(MENU_KEYS["SELECT_MODE"])
            for event in pyg.event.get():
                if event.type == pyg.KEYDOWN:
                    if event.key == pyg.K_BACKSPACE:
                        self.inputText = self.inputText[:-1]
                    elif event.key == pyg.K_n:
                        self.menu.rotationSet += 1
                        print(self.inputText)
                        self.newQtn.append(float(self.inputText))
                        self.inputText = "0"
                    elif event.key == pyg.K_p:
                        self.keyPressed = pyg.K_0
                        self.changeMenu(0)
                    else:
                        self.inputText += event.unicode
            # if self.worker.keysInput[pyg.K_BACKSPACE]:
            #     self.inputText = self.inputText[:-1]
            # elif self.worker.keysInput[pyg.K_KP_ENTER]:
            #     self.menu.rotationSet += 1
            #     self.inputText = "0"
            # elif self.keyPressed != -1:
            #     self.inputText += self.worker.keysInput

        if self.worker.keysInput[pyg.K_0] and self.menu.menuToDisplay != MENU_KEYS["SET_MESH_ROTATION"]:
            self.keyPressed = pyg.K_0
            self.changeMenu(0)

    def changeMenu(self, menu: int):
        if menu == MENU_KEYS["ADD_ANIM_TO_MESH"]:
            self.mesh.animation.append(self.mesh.transform.copy())
        elif menu == MENU_KEYS["PLAY_ANIMATION"]:
            self.mesh.animationPlay = not self.mesh.animationPlay
            pass
        else:
            self.newQtn = list()
            self.menu.rotationSet = 0
            self.menu.meshListOffset = 0
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
