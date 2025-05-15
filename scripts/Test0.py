import pygame

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D
from engine.render import Mesh, Face
from engine.worker import GameMaster, PygIO


class Test0(GameMaster):
    testMesh: Mesh

    def onCreate(self):
        self.worker.show_over = self.show_over
        self.testMesh = Mesh(
            points=(
                Vector3D(9, -1, 0),
                Vector3D(9, 1, .1),
                Vector3D(10, 0, 1),
                Vector3D(11, 0, -.2)
            ),
            faces=(
                Face(pointIndex=(0, 1, 2), color=pygame.Color(255, 0, 0)),
                Face(pointIndex=(1, 2, 3), color=pygame.Color(0, 255, 0)),
                Face(pointIndex=(2, 3, 0), color=pygame.Color(0, 0, 255)),
                Face(pointIndex=(0, 1, 3), color=pygame.Color(0, 0, 0)),
            )
        )
        self.worker.renderer.mesh.append(self.testMesh)

    def start(self):
        pass

    def update(self):
        origin = Vector2D(10, 0)
        for i in self.testMesh.points:
            a, n = (i.project_h() - origin).exponential
            a += self.worker.deltaTime
            v = Vector2D.from_exp(a, n) + origin
            i.x = v.x
            i.y = v.y

    def show_over(self, pygIO: PygIO):
        pass

    def fixedUpdate(self):
        pass
