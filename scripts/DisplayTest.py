from backwork.Vector2D import Vector2D
from meshs.Mesh import Mesh
from engine.worker import Worker, PygIO


class DisplayTest:
    worker: Worker
    mesh: Mesh

    def __init__(self, worker):
        self.worker = worker

    def init(self, mesh):
        self.mesh = mesh

    def update(self):
        origin = Vector2D(9.5,0)
        for i in self.mesh.points:
            a, n = (i.project_h()-origin).exponential
            a += self.worker.deltaTime
            v = Vector2D.from_exp(a, n)+origin
            i.x = v.x
            i.y = v.y

    def show_over(self, pygIO: PygIO):
        pass
