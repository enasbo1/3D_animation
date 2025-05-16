import pygame

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
    rotation_speed: float
    operation_count: float

    def init(self, mesh):
        self.mesh = mesh

        self.rotation_speed = 0.005
        self.operation_count = 0

    def update(self):
        mesh = self.mesh

        # Update Rotation angle
        mesh.rotation.x += self.rotation_speed
        mesh.rotation.y += self.rotation_speed / 2
        mesh.rotation.z += self.rotation_speed / 3

        # Réinitialisation du compteur d'opérations
        self.operation_count = 0

        # Création des quaternions de rotation pour chaque axe
        qx = QuaternionRotation.rotation_quaternion(Vector3D(1, 0, 0), mesh.rotation.x)
        qy = QuaternionRotation.rotation_quaternion(Vector3D(0, 1, 0), mesh.rotation.y)
        qz = QuaternionRotation.rotation_quaternion(Vector3D(0, 0, 1), mesh.rotation.z)

        # Création du quaternion composé pour la rotation totale
        # La multiplication des quaternions se fait de droite à gauche (ordre inverse)
        # Pour appliquer X, puis Y, puis Z, il faut multiplier car le produit de quaternion n'est pas commutatif : Z * Y * X
        q_total = qz * qy * qx
        self.operation_count += 3

        # Appliquer le quaternion à tous les points
        center = Vector3D(0, 0, 0)  # Centre de rotation locale
        for i, original in enumerate(mesh.pointsOrigin):
            # Appliquer la rotation
            rotated = QuaternionRotation.rotate_point(original, q_total)
            self.operation_count += 1

            # Move to final pos
            mesh.points[i] = rotated + mesh.position

    def show_over(self, pygIO: PygIO):
        mesh = self.mesh
        pygIO.draw_text(-500, 0,
                        f"Rotation Quaternion: X={mesh.rotation.x:.2f}, Y={mesh.rotation.y:.2f}, Z={mesh.rotation.z:.2f}",
                        20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-591, 30,
                        f"Opérations: {self.operation_count}",
                        20, pygame.Color(255, 255, 255))
