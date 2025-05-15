import pygame
import math
from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from engine.render import Mesh, Face, Camera
from engine.worker import GameMaster, PygIO

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

class ObjectRotationQuaternion(GameMaster):
    """Démontre la rotation d'un objet avec des quaternions"""
    
    def onCreate(self):
        # Exemple : Création d'un cube
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
        
        self.current_points = self.original_points.copy()
        
        # Définition des faces
        self.faces = [
            Face(pointIndex=(0, 1, 2, 3), color=pygame.Color(255, 0, 0)),    # rouge
            Face(pointIndex=(4, 5, 6, 7), color=pygame.Color(0, 255, 0)),    # vert
            Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(0, 0, 255)),    # bleu
            Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(255, 255, 0)),  # jaune
            Face(pointIndex=(0, 3, 7, 4), color=pygame.Color(255, 0, 255)),  # magenta
            Face(pointIndex=(1, 2, 6, 5), color=pygame.Color(0, 255, 255)),  # cyan
        ]
        
        # Création du mesh
        self.mesh = Mesh(
            points=tuple(self.current_points),
            faces=tuple(self.faces)
        )
        
        # Ajout au renderer
        self.worker.renderer.mesh.append(self.mesh)
        
        # Angles de rotation
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        # Vitesse de rotation
        self.rotation_speed = 0.005
        
        # Compteur d'opérations pour comparaison
        self.operation_count = 0
        
        # Affichage d'informations
        self.worker.show_over = self.show_over

    def start(self):
        pass

    def update(self):
        # Mise à jour des angles de rotation
        self.angle_x += self.rotation_speed
        self.angle_y += self.rotation_speed / 2
        self.angle_z += self.rotation_speed / 3
        
        # Réinitialisation du compteur d'opérations
        self.operation_count = 0
        
        # Calcul du centre du cube
        center = Vector3D(9.5, 0, 0)
        
        # Création des quaternions de rotation pour chaque axe
        qx = QuaternionRotation.rotation_quaternion(Vector3D(1, 0, 0), self.angle_x)
        qy = QuaternionRotation.rotation_quaternion(Vector3D(0, 1, 0), self.angle_y)
        qz = QuaternionRotation.rotation_quaternion(Vector3D(0, 0, 1), self.angle_z)
        
        # Création du quaternion composé pour la rotation totale
        q_total = qz * qy * qx
        self.operation_count += 3
        
        # Application des rotations à chaque point
        for i, original in enumerate(self.original_points):
            # Translater vers l'origine
            point = Vector3D(original.x - center.x, original.y - center.y, original.z - center.z)
            
            # Appliquer la rotation par quaternion
            rotated = QuaternionRotation.rotate_point(point, q_total)
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
        pygIO.draw_text(10, 10, 
                       f"Rotation Quaternion: X={self.angle_x:.2f}, Y={self.angle_y:.2f}, Z={self.angle_z:.2f}", 
                       20, pygame.Color(255, 255, 255))
        pygIO.draw_text(10, 40, 
                       f"Opérations: {self.operation_count}", 
                       20, pygame.Color(255, 255, 255))

    def fixedUpdate(self):
        pass 