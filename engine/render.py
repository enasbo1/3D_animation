from operator import concat

from backwork.Vector3D import Vector3D
from backwork.affichage import per_point, _per_point_dirCam
from backwork.mathAddOn import somme
from engine.pygio import PygIO

from meshs.Mesh import Mesh, Face

class Camera(Vector3D):
    d:float = 0.
    v:float = 0.

class Render:
    mesh: list[Mesh]

    def __init__(self, mesh : list[Mesh] = None):
        self.mesh = mesh if mesh is not None else []

    def show(self, cam: Camera, pygio : PygIO, vertice:bool = False, edge:bool = False):
        a_points = []
        for m in self.mesh:
            points = tuple(per_point(pygio.width, pygio.height, cam, cam.d, cam.v, p) for p in m.transformedPoints)
            for f in m.faces:
                f.camDist = _per_point_dirCam.scalar(
                    somme(*tuple(m.points[i] for i in f.pointIndex)) / len(f.pointIndex)
                )
                f.pointPers = tuple(points[i] for i in f.pointIndex)
            a_points.extend(points)

        if len(self.mesh)==0: return;

        if len(self.mesh)==1:
            _faces:list[Face] = list(self.mesh[0].faces)
        else:
            _faces:list[Face] = list(concat(*[m.faces for m in self.mesh]))

        _faces.sort(key = lambda x:x.camDist, reverse=True)

        for f in _faces:
            if f.camDist>0:
                pygio.draw_poly(tuple(p.coord for p in f.pointPers), f.color)
        if edge:
            for f in _faces:
                if f.camDist>0:
                    pygio.draw_poly(tuple(p.coord for p in f.pointPers), "#333333", width = 2)
        if vertice:
            for p in a_points:
                pygio.draw_cross(p.coord, 7, "#aa0000")


