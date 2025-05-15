from operator import concat

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D
from backwork.affichage import per_point, _per_point_dirCam
from backwork.mathAddOn import somme
from engine.pygio import PygIO, pyg

class Face:
    pointIndex:tuple[int, int, int]
    color:pyg.Color
    camDist:float
    pointPers:tuple[Vector2D,]

    def __init__(self, pointIndex:tuple[int, int, int] = tuple(), color:pyg.Color = pyg.Color(150,150,150)):
        self.color = color
        self.pointIndex = pointIndex;

class Transform:
    def apply(self, mesh)->tuple[Vector3D]:
        return mesh.points

class Mesh:
    transform:Transform
    points:tuple[Vector3D, ...]
    faces:tuple[Face, ...]

    def __init__(self, points:tuple[Vector3D, ...]=None, faces:tuple[Face, ...]=None, transform:Transform = Transform()):
        self.points = points if points is not None else []
        self.faces = faces if faces is not None else []
        self.transform = transform


    transformedPoints = property(lambda self:self.transform.apply(self))


class Camera(Vector3D):
    d:float = 0.
    v:float = 0.

class Render:
    mesh : list[Mesh]

    def __init__(self, mesh : list[Mesh] = None):
        self.mesh = mesh if mesh is not None else []

    def show(self, cam: Camera, pygio : PygIO, vertice:bool = False, edge:bool = False):
        a_points  = []
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


