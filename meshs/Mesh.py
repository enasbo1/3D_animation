import pygame as pyg

from backwork.mathAddOn import approach
from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion


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
    animation: list[Transform] = list()
    animationCurrent: int = 0
    animationNext: int = 0
    animationPlay: bool = False
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
        self.animation.append(transform)

    def scale(self, mult: float):
        for pointI in range(len(self.points)):
            self.points[pointI] *= mult

    def playAnim(self):
        currentTransform = self.transform
        nextTransform = self.animation[self.animationNext]
        speed = 0.01

        if currentTransform.rotation != nextTransform.rotation:
            currentTransform.rotation = Quaternion(
                approach(currentTransform.rotation.r, nextTransform.rotation.r, speed),
                approach(currentTransform.rotation.i, nextTransform.rotation.i, speed),
                approach(currentTransform.rotation.j, nextTransform.rotation.j, speed),
                approach(currentTransform.rotation.k, nextTransform.rotation.k, speed)
            )
            return

        self.animationCurrent = self.animationNext
        self.animationNext += 1
        self.animationNext %= len(self.animation)
        self.transform = self.animation[self.animationCurrent]
