import pygame

from backwork.Vector3D import Vector3D
from meshs.Mesh import Mesh, Face, Transform


class Cube(Mesh):
    def __init__(self, transform: Transform = Transform()):
        super().__init__(
            points=[
                Vector3D(-1, -1, -1),
                Vector3D(1, -1, -1),
                Vector3D(1, 1, -1),
                Vector3D(-1, 1, -1),
                Vector3D(-1, -1, 1),
                Vector3D(1, -1, 1),
                Vector3D(1,  1, 1),
                Vector3D(-1, 1, 1)
            ],
            faces=(
                Face(pointIndex=(3, 2, 1, 0), color=pygame.Color(200, 0, 0)),      # Rouge
                Face(pointIndex=(4, 5, 6, 7), color=pygame.Color(0, 200, 0)),      # Vert
                Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(0, 0, 200)),      # Bleu
                Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(150, 150, 0)),    # Jaune
                Face(pointIndex=(0, 4, 7, 3), color=pygame.Color(150, 0, 150)),    # Magenta
                Face(pointIndex=(1, 2, 6, 5), color=pygame.Color(0, 150, 150)),    # Cyan
            ),
            transform=transform
        )

        self.name = "Cube"
