import pygame
import math

from backwork.Vector3D import Vector3D
from engine.worker import PygIO
from meshs.Mesh import Mesh


class MatrixRotation:
    """Classe utilitaire pour les rotations par matrices"""

    @staticmethod
    def rotation_x(angle):
        """Matrice de rotation autour de l'axe X (roulis)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [1, 0, 0],
            [0, cos_a, -sin_a],
            [0, sin_a, cos_a]
        ]

    @staticmethod
    def rotation_y(angle):
        """Matrice de rotation autour de l'axe Y (tangage)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [cos_a, 0, sin_a],
            [0, 1, 0],
            [-sin_a, 0, cos_a]
        ]

    @staticmethod
    def rotation_z(angle):
        """Matrice de rotation autour de l'axe Z (lacet)"""
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return [
            [cos_a, -sin_a, 0],
            [sin_a, cos_a, 0],
            [0, 0, 1]
        ]

    @staticmethod
    def apply_matrix(point, matrix):
        """Applique une matrice 3x3 à un point Vector3D"""
        x = point.x * matrix[0][0] + point.y * matrix[0][1] + point.z * matrix[0][2]
        y = point.x * matrix[1][0] + point.y * matrix[1][1] + point.z * matrix[1][2]
        z = point.x * matrix[2][0] + point.y * matrix[2][1] + point.z * matrix[2][2]
        return Vector3D(x, y, z)


class ObjectRotationMatrix:
    mesh: Mesh
    rotation_speed: float
    operation_count: float

    def init(self, mesh):
        self.mesh = mesh

        self.rotation_speed = 0.005
        self.operation_count = 0

    def update(self):
        mesh = self.mesh

        # update rotation angles
        mesh.rotation.x += self.rotation_speed
        mesh.rotation.y += self.rotation_speed / 2
        mesh.rotation.z += self.rotation_speed / 3

        self.operation_count = 0

        # Create les matrices de rotation
        mat_x = MatrixRotation.rotation_x(mesh.rotation.x)
        mat_y = MatrixRotation.rotation_y(mesh.rotation.y)
        mat_z = MatrixRotation.rotation_z(mesh.rotation.z)

        # Combiner les matrices (multiplication matricielle)
        combined_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        # Multipliez d'abord X par Y
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    combined_matrix[i][j] += mat_x[i][k] * mat_y[k][j]
                    self.operation_count += 1

        # Multipliez le résultat par Z
        final_matrix = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

        for i in range(3):
            for j in range(3):
                for k in range(3):
                    final_matrix[i][j] += combined_matrix[i][k] * mat_z[k][j]
                    self.operation_count += 1

        # Appliquer la matrice de rotation à tous les points
        for i, original in enumerate(mesh.pointsOrigin):
            # Appliquer la rotation par matrice
            rotated = MatrixRotation.apply_matrix(original, final_matrix)
            self.operation_count += 1

            # Move to final pos
            mesh.points[i] = rotated + mesh.position

    def show_over(self, pygIO: PygIO):
        mesh = self.mesh
        print(mesh.points[0].x, mesh.points[0].y, mesh.points[0].z)
        print(mesh.pointsOrigin[0].x, mesh.pointsOrigin[0].y, mesh.pointsOrigin[0].z)
        pygIO.draw_text(-500, 0,
                        f"Rotation Matrice: X={mesh.rotation.x:.2f}, Y={mesh.rotation.y:.2f}, Z={mesh.rotation.z:.2f}",
                        20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-580, 30,
                        f"Opérations: {self.operation_count}",
                        20, pygame.Color(255, 255, 255))
