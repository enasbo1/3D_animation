import pygame

from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from meshs.Mesh import Mesh
from engine.worker import PygIO, Worker
from scripts.Transform3D import Transform3D


class QuaternionRotation:
    """Classe utilitaire pour les rotations par quaternions"""

    @staticmethod
    def rotation_quaternion(axis: Vector3D, angle: float):
        """Crée un quaternion pour une rotation autour d'un axe"""
        return Quaternion.rotation(axis, angle)

    @staticmethod
    def rotate_point(point: Vector3D, q: Quaternion) -> Vector3D:
        """Applique une rotation quaternion à un point: q * v * q̄"""
        return q.rotate_point(point)


class ObjectRotationQuaternion:
    mesh: Mesh
    transform: Transform3D
    rotation_speed: float
    operation_count: int
    axe: Vector3D = Vector3D(6, 3, 2)

    def __init__(self, worker: Worker, transform: Transform3D):
        self.transform = transform
        self.worker = worker

    def init(self, mesh):
        self.mesh = mesh
        self.operation_count = 0

    def update(self):
        self.operation_count = 0

        # Update Rotation angle
        self.transform.rotation = self.transform.rotation * Quaternion.rotation(self.axe, self.worker.deltaTime)
        self.operation_count += 7

    def show_over(self, pygIO: PygIO):
        pygIO.draw_text(-850, -470,
                        f"Rotation Quaternion: {self.transform.rotation}",
                        30, pygame.Color(255, 255, 255),
                        False)
        pygIO.draw_text(-850, -430,
                        f"Opérations: {self.operation_count}",
                        30, pygame.Color(255, 255, 255),
                        False)
