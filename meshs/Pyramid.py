import pygame

from backwork.Vector3D import Vector3D
from meshs.Mesh import Mesh, Face, Transform


class Pyramid(Mesh):
    mesh: Mesh

    def __init__(self, transform: Transform = Transform()):
        super().__init__(
            points=[
                Vector3D(0, 0, -0.5),
                Vector3D(0.5, 0.5, 0.5),
                Vector3D(0.5, -0.5, 0.5),
                Vector3D(-0.5, -0.5, 0.5),
                Vector3D(-0.5, 0.5, 0.5)
            ],
            faces=(
                Face(pointIndex=(0, 1, 2), color=pygame.Color(255, 0, 0)),
                Face(pointIndex=(0, 2, 3), color=pygame.Color(0, 255, 0)),
                Face(pointIndex=(0, 3, 4), color=pygame.Color(0, 0, 255)),
                Face(pointIndex=(0, 4, 1), color=pygame.Color(255, 100, 0)),
                Face(pointIndex=(1, 2, 3, 4), color=pygame.Color(0, 0, 0)),
            ),
            transform=transform
        )
