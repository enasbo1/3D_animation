import pygame as pyg

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D


class Face:
    pointIndex: tuple[int, int, int] | tuple[int, int, int, int]
    color: pyg.Color
    camDist: float
    pointPers: tuple[Vector2D, ...]
    light: float = 1

    def __init__(self, pointIndex: tuple[int, int, int] | tuple[int, int, int, int] = tuple(),
                 color: pyg.Color = pyg.Color(150, 150, 150)):
        self.color = color
        self.pointIndex = pointIndex


class Transform:
    def apply(self, mesh) -> tuple[Vector3D]:
        return mesh.points


class Mesh:
    transform: Transform
    points: list[Vector3D]
    faces: tuple[Face, ...]
    transformedPoints = property(lambda self: self.transform.apply(self))
    name: str = None

    def __init__(self,
                 points: list[Vector3D] = None,
                 faces: tuple[Face, ...] = None,
                 transform: Transform = Transform(),
                 ):

        self.points = [] if points is None else points
        self.faces = tuple() if faces is None else faces
        self.transform = transform
