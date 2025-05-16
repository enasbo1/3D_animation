import pygame

from backwork.Vector3D import Vector3D
from meshs.Mesh import Mesh, Face


class Pyramid(Mesh):
    mesh: Mesh

    def __init__(self):
        super().__init__()

        self.mesh = Mesh(
            points=(
                Vector3D(1, -1, 0),
                Vector3D(1, 1, .1),
                Vector3D(2, 0, 1),
                Vector3D(3, 0, -.2)
            ),
            faces=(
                Face(pointIndex=(0, 1, 2), color=pygame.Color(255, 0, 0)),
                Face(pointIndex=(1, 2, 3), color=pygame.Color(0, 255, 0)),
                Face(pointIndex=(2, 3, 0), color=pygame.Color(0, 0, 255)),
                Face(pointIndex=(0, 1, 3), color=pygame.Color(0, 0, 0)),
            ),
            position=Vector3D(10, 0, 0)
        )
