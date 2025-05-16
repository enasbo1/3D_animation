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
                Face(pointIndex=(0, 1, 2, 3), color=pygame.Color(255, 0, 0)),      # Rouge
                Face(pointIndex=(4, 5, 6, 7), color=pygame.Color(0, 255, 0)),      # Vert
                Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(0, 0, 255)),      # Bleu
                Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(255, 255, 0)),    # Jaune
                Face(pointIndex=(0, 3, 7, 4), color=pygame.Color(255, 0, 255)),    # Magenta
                Face(pointIndex=(1, 2, 6, 5), color=pygame.Color(0, 255, 255)),    # Cyan
            ),
            transform=transform
        )
