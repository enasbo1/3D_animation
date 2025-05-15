import pygame

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D
from engine.render import Mesh, Face
from engine.worker import GameMaster, PygIO


class Menu(GameMaster):
    testMesh: Mesh

    def onCreate(self):
        pass

    def start(self):
        pass

    def update(self):
        pass

    def show(self, pygIO: PygIO):
        boxPos = -pygIO.width // 2
        pygIO.draw_rect(boxPos, 20, 500, 2000, "#000000")
        pygIO.draw_text(boxPos, 60, "Exemple to display:", 30, "#FFFFFF")
        pygIO.draw_text(boxPos, 100, "0: Display Test", 30, "#FFFFFF")
        pygIO.draw_text(boxPos, 140, "1: Point rotation", 30, "#FFFFFF")
        pygIO.draw_text(boxPos, 180, "2: Matrice rotation", 30, "#FFFFFF")
        pygIO.draw_text(boxPos, 220, "3: Quaternion rotation", 30, "#FFFFFF")
        pygIO.draw_text(boxPos, 260, "4: Not Centered Rotation", 30, "#FFFFFF")


        pass

    def fixedUpdate(self):
        pass
