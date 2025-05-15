import pygame
import math
from backwork.Vector3D import Vector3D
from engine.render import Mesh, Face, Camera, Transform
from engine.worker import GameMaster, PygIO
from scripts.Cube import Cube

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

class ObjectRotationMatrix(GameMaster):    
    def onCreate(self):
        camera = self.worker.activeCamera
        
        cube = Cube()
        # Convertir les points du cube et les mettre à l'échelle
        scale = 1  # Taille du cube
        self.original_points = [Vector3D(p[0] * scale, p[1] * scale, p[2] * scale) for p in cube.points]
        self.current_points = self.original_points.copy()  # Points après rotation
        
        # Définition des faces avec des couleurs bien contrastées
        self.faces = [
            Face(pointIndex=(0, 1, 2, 3), color=pygame.Color(255, 0, 0)),      # Rouge
            Face(pointIndex=(4, 5, 6, 7), color=pygame.Color(0, 255, 0)),      # Vert
            Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(0, 0, 255)),      # Bleu
            Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(255, 255, 0)),    # Jaune
            Face(pointIndex=(0, 3, 7, 4), color=pygame.Color(255, 0, 255)),    # Magenta
            Face(pointIndex=(1, 2, 6, 5), color=pygame.Color(0, 255, 255)),    # Cyan
        ]
        
        # Position du cube devant la caméra
        self.cube_position = Vector3D(10, 0, 0)  # Placer le cube sur l'axe X
        
        # Création du mesh directement avec les points et les faces
        self.mesh = Mesh(
            points=tuple(self.current_points),
            faces=tuple(self.faces)
        )
        
        self.worker.renderer.mesh.append(self.mesh)
        
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        self.rotation_speed = 0.005
        self.operation_count = 0
        self.worker.show_over = self.show_over

    def start(self):
        pass

    def update(self):
        self.angle_x += self.rotation_speed
        self.angle_y += self.rotation_speed / 2
        self.angle_z += self.rotation_speed / 3
        
        self.operation_count = 0
        
        # Créer les matrices de rotation
        mat_x = MatrixRotation.rotation_x(self.angle_x)
        mat_y = MatrixRotation.rotation_y(self.angle_y)
        mat_z = MatrixRotation.rotation_z(self.angle_z)
        
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
        for i, original in enumerate(self.original_points):
            # Appliquer la rotation par matrice
            rotated = MatrixRotation.apply_matrix(original, final_matrix)
            self.operation_count += 1
            
            # Déplacer à la position finale
            self.current_points[i] = rotated + self.cube_position
        
        # Mettre à jour le mesh avec les points tournés
        self.mesh.points = tuple(self.current_points)

    def show_over(self, pygIO: PygIO):
        # Affichage d'informations
        pygIO.draw_text(-500, 0, 
                       f"Rotation Matrice: X={self.angle_x:.2f}, Y={self.angle_y:.2f}, Z={self.angle_z:.2f}", 
                       20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-580, 30, 
                       f"Opérations: {self.operation_count}", 
                       20, pygame.Color(255, 255, 255))

    def fixedUpdate(self):
        pass 