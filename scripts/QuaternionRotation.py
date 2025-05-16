import pygame
import math

from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from meshs.Mesh import Mesh
from engine.worker import PygIO


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
    original_points: list[Vector3D]
    current_points: list[Vector3D]
    cube_position: Vector3D
    angle_x: float
    angle_y: float
    angle_z: float
    rotation_speed: float
    operation_count: float

    def init(self, mesh):
        self.mesh = mesh

        # Convertir les points du cube et les mettre à l'échelle
        scale = 1  # Taille du cube
        self.original_points = [Vector3D(p.x * scale, p.y * scale, p.z * scale) for p in mesh.pointsOrigin]
        self.current_points = self.original_points.copy()  # Points après rotation

        # Position du cube devant la caméra (plus éloigné pour mieux le voir)
        self.cube_position = Vector3D(10, 0, 0)

        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0

        self.rotation_speed = 0.005
        self.operation_count = 0

    def update(self):
        # Mise à jour des angles de rotation
        self.angle_x += self.rotation_speed
        self.angle_y += self.rotation_speed / 2
        self.angle_z += self.rotation_speed / 3

        # Réinitialisation du compteur d'opérations
        self.operation_count = 0

        # Création des quaternions de rotation pour chaque axe
        qx = QuaternionRotation.rotation_quaternion(Vector3D(1, 0, 0), self.angle_x)
        qy = QuaternionRotation.rotation_quaternion(Vector3D(0, 1, 0), self.angle_y)
        qz = QuaternionRotation.rotation_quaternion(Vector3D(0, 0, 1), self.angle_z)

        # Création du quaternion composé pour la rotation totale
        # La multiplication des quaternions se fait de droite à gauche (ordre inverse)
        # Pour appliquer X, puis Y, puis Z, il faut multiplier car le produit de quaternion n'est pas commutatif : Z * Y * X
        q_total = qz * qy * qx
        self.operation_count += 3

        # Appliquer le quaternion à tous les points
        center = Vector3D(0, 0, 0)  # Centre de rotation locale
        for i, original in enumerate(self.original_points):
            # Appliquer la rotation
            rotated = QuaternionRotation.rotate_point(original, q_total)
            self.operation_count += 1

            # Déplacer à la position finale
            self.current_points[i] = rotated + self.cube_position

        # Mettre à jour le mesh avec les points tournés
        self.mesh.points = tuple(self.current_points)

    def show_over(self, pygIO: PygIO):
        pygIO.draw_text(-500, 0,
                        f"Rotation Quaternion: X={self.angle_x:.2f}, Y={self.angle_y:.2f}, Z={self.angle_z:.2f}",
                        20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-591, 30,
                        f"Opérations: {self.operation_count}",
                        20, pygame.Color(255, 255, 255))
