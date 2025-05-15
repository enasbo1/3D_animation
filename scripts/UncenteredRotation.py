import pygame
import math
from backwork.Vector3D import Vector3D
from backwork.Quaternion import Quaternion
from engine.render import Mesh, Face, Camera
from engine.worker import GameMaster, PygIO
from scripts.Transform3D import Transform3D
from scripts.Cube import Cube

class UncenteredRotation:
    """Classe utilitaire pour les rotations décentrées (autour d'un point autre que l'origine)"""
    
    @staticmethod
    def rotation_quaternion(axis: Vector3D, angle: float):
        """Crée un quaternion pour une rotation autour d'un axe"""
        return Quaternion.rotation(axis, angle)

class ObjectUncenteredRotation(GameMaster):
    """Démontre la rotation d'un objet autour d'un centre arbitraire"""
    
    def onCreate(self):
        camera = self.worker.activeCamera
        cube = Cube()
        
        # Convertir les points du cube et les mettre à l'échelle
        scale = 1  # Taille du cube
        self.original_points = [Vector3D(p[0], p[1], p[2]) for p in cube.points]
        
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
        self.cube_position = Vector3D(10, 0, 0)  # Position globale du cube
        
        # Centre de rotation décentré (en coordonnées locales - par rapport au cube)
        # Par exemple, rotation autour d'un coin du cube
        self.rotation_center = Vector3D(0.5, 0.5, 0.5)
        
        # Position du centre de rotation dans l'espace global
        self.global_rotation_center = self.rotation_center + self.cube_position
        
        # Création du Transform3D avec position et échelle
        self.transform = Transform3D(
            position=self.cube_position,
            scale=Vector3D(scale, scale, scale)
        )
        
        # Création du mesh avec le Transform3D
        self.mesh = Mesh(
            points=tuple(self.original_points),
            faces=tuple(self.faces),
            transform=self.transform
        )
        
        # Ajout au renderer
        self.worker.renderer.mesh.append(self.mesh)
        
        # Ajout d'un petit indicateur pour le centre de rotation
        center_marker_points = []
        marker_size = 0.05
        for dx in [-marker_size, marker_size]:
            for dy in [-marker_size, marker_size]:
                for dz in [-marker_size, marker_size]:
                    center_marker_points.append(Vector3D(dx, dy, dz))
        
        # Transformation pour le marqueur
        self.marker_transform = Transform3D(
            position=self.global_rotation_center
        )
        
        self.marker_mesh = Mesh(
            points=tuple(center_marker_points),
            faces=(
                Face(pointIndex=(0, 1, 3, 2), color=pygame.Color(255, 255, 255)),
                Face(pointIndex=(4, 5, 7, 6), color=pygame.Color(255, 255, 255)),
                Face(pointIndex=(0, 1, 5, 4), color=pygame.Color(255, 255, 255)),
                Face(pointIndex=(2, 3, 7, 6), color=pygame.Color(255, 255, 255)),
                Face(pointIndex=(0, 2, 6, 4), color=pygame.Color(255, 255, 255)),
                Face(pointIndex=(1, 3, 7, 5), color=pygame.Color(255, 255, 255)),
            ),
            transform=self.marker_transform
        )
        self.worker.renderer.mesh.append(self.marker_mesh)
        
        # Angles de rotation
        self.angle_x = 0
        self.angle_y = 0
        self.angle_z = 0
        
        # Vitesse de rotation
        self.rotation_speed = 0.01
        
        # Compteur d'opérations pour comparaison
        self.operation_count = 0
        
        # Affichage d'informations
        self.worker.show_over = self.show_over

    def start(self):
        pass

    def update(self):
        # Mise à jour des angles
        self.angle_x += self.rotation_speed
        self.angle_y += self.rotation_speed / 2
        self.angle_z += self.rotation_speed / 3
        
        # Création du quaternion de rotation
        qx = Quaternion.rotation(Vector3D(1, 0, 0), self.angle_x)
        qy = Quaternion.rotation(Vector3D(0, 1, 0), self.angle_y)
        qz = Quaternion.rotation(Vector3D(0, 0, 1), self.angle_z)
        q_total = qz * qy * qx
        
        self.operation_count += 3

        # Rotation manuelle autour du centre
        rotated_points = []
        for point in self.original_points:
            # 1. Appliquer l'échelle locale
            scaled = Vector3D(
                point.x * self.transform.scale.x,
                point.y * self.transform.scale.y,
                point.z * self.transform.scale.z
            )
            
            # 2. Déplacer vers le centre de rotation global
            translated = scaled - self.rotation_center
            
            # 3. Appliquer la rotation
            rotated = q_total.rotate_point(translated)
            
            # 4. Replacer + position globale
            final_point = rotated + self.global_rotation_center
            rotated_points.append(final_point)
        
        # Mise à jour directe du mesh
        self.mesh.points = tuple(rotated_points)

    def show_over(self, pygIO: PygIO):
        pygIO.draw_text(-500, 0, 
                       f"Rotation Décentrée: X={self.angle_x:.2f}, Y={self.angle_y:.2f}, Z={self.angle_z:.2f}", 
                       20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-570, 30, 
                       f"Centre: ({self.rotation_center.x:.1f}, {self.rotation_center.y:.1f}, {self.rotation_center.z:.1f})", 
                       20, pygame.Color(255, 255, 255))
        pygIO.draw_text(-591, 60, 
                       f"Opérations: {self.operation_count}", 
                       20, pygame.Color(255, 255, 255))

    def fixedUpdate(self):
        pass 