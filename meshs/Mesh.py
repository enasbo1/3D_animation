import pygame as pyg

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D


class Face:
    pointIndex: tuple[int, int, int] | tuple[int, int, int, int]
    color: pyg.Color
    camDist: float
    pointPers: tuple[Vector2D, ...]

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
    pointsOrigin: list[Vector3D]
    faces: tuple[Face, ...]
    position: Vector3D
    rotation: Vector3D
    scale: Vector3D

    transformedPoints = property(lambda self: self.transform.apply(self))

    def __init__(self,
                 points: list[Vector3D] = None,
                 faces: tuple[Face, ...] = None,
                 transform: Transform = Transform(),
                 position: Vector3D = Vector3D.zero(),
                 rotation: Vector3D = Vector3D.one(),
                 scale: Vector3D = Vector3D.one()
                 ):

        self.pointsOrigin = points if points is not None else []
        self.points = list(point + position for point in self.pointsOrigin)
        self.faces = faces if faces is not None else []
        self.transform = transform
        self.position = position
        self.rotation = rotation
        self.scale = scale
