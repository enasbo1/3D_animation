import pygame
import math
from backwork.Vector3D import Vector3D
from engine.render import Mesh, Face, Camera
from engine.worker import GameMaster, PygIO

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
    """Démontre la rotation d'un objet en utilisant des matrices"""
    
    def onCreate(self):
        # Création du cube avec des coordonnées plus éloignées (comme dans MainGame.py)
        self.original_points = [
            Vector3D(9, -0.5, -0.5),  
            Vector3D(9, 0.5, -0.5),   
            Vector3D(9, 0.5, 0.5),    
            Vector3D(9, -0.5, 0.5),   
            Vector3D(10, -0.5, -0.5), 
            Vector3D(10, 0.5, -0.5),  
            Vector3D(10, 0.5, 0.5),   
            Vector3D(10, -0.5, 0.5)   
        ]
        
        # Points actuels pour manipulation
        self.current_points = self.original_points.copy()
        
        self.faces = [
            Face(pointIndex=(0, 1, 2, 3), color=pygame.Color(255, 0, 0)),    # rouge
            Face(pointIndex=(4, 5, 6, 7), color=pygame.Color(0, 255, 0)),    # verte
            Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(0, 0, 255)),    # bleue
            Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(255, 255, 0)),  # jaune
            Face(pointIndex=(0, 3, 7, 4), color=pygame.Color(255, 0, 255)),  # magenta
            Face(pointIndex=(1, 2, 6, 5), color=pygame.Color(0, 255, 255)),  # cyan
        ]
        
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
        
        center = Vector3D(9.5, 0, 0)
        
        mat_x = MatrixRotation.rotation_x(self.angle_x)
        mat_y = MatrixRotation.rotation_y(self.angle_y)
        mat_z = MatrixRotation.rotation_z(self.angle_z)
        
        # Application des rotations à chaque point
        for i, original in enumerate(self.original_points):
            # Translater vers l'origine
            point = Vector3D(original.x - center.x, original.y - center.y, original.z - center.z)
            
            # Appliquer les rotations
            rotated = MatrixRotation.apply_matrix(point, mat_x)
            self.operation_count += 1
            
            rotated = MatrixRotation.apply_matrix(rotated, mat_y)
            self.operation_count += 1
            
            rotated = MatrixRotation.apply_matrix(rotated, mat_z)
            self.operation_count += 1
            
            # Ramener à la position d'origine
            self.current_points[i] = Vector3D(
                rotated.x + center.x, 
                rotated.y + center.y, 
                rotated.z + center.z
            )
        
        # Mise à jour du mesh
        self.mesh.points = tuple(self.current_points)

    def show_over(self, pygIO: PygIO):
        # Affichage d'informations
        pygIO.draw_text(1, 1, 
                       f"Rotation Matrice: X={self.angle_x:.2f}, Y={self.angle_y:.2f}, Z={self.angle_z:.2f}", 
                       20, pygame.Color(255, 255, 255))
        pygIO.draw_text(10, 40, 
                       f"Opérations: {self.operation_count}", 
                       20, pygame.Color(255, 255, 255))

    def fixedUpdate(self):
        pass 