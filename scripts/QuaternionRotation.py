import pygame
import math
from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from engine.render import Mesh, Face, Camera
from engine.worker import GameMaster, PygIO
from scripts.Transform3D import Transform3D
from scripts.Cube import Cube

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
        camera = self.worker.activeCamera
        cube = Cube()
        
        # Convertir les points du cube et les mettre à l'échelle
        scale = 1 # Taille du cube
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
        
        # Position du cube devant la caméra (plus éloigné pour mieux le voir)
        self.cube_position = Vector3D(10, 0, 0)  # Placer le cube sur l'axe X, dans le sens où la caméra regarde
        
        # Création du mesh directement avec les points et les faces
        self.mesh = Mesh(
            points=tuple(self.current_points),
            faces=tuple(self.faces)
        )
        
        # Ajout au renderer
        self.worker.renderer.mesh.append(self.mesh)
        
        # Angles de rotation
        self.angle_x = math.pi/4
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

    def fixedUpdate(self):
        pass 