from operator import concat

from backwork.Vector2D import Vector2D
from backwork.Vector3D import Vector3D
from backwork.affichage import per_point, _per_point_dirCam
from backwork.mathAddOn import somme
from engine.pygio import PygIO, pyg

class Face:
    pointIndex:tuple[int]
    color:pyg.Color
    camDist:float
    pointPers:tuple[Vector2D,]

    def __init__(self, pointIndex:tuple[int,] = tuple(), color:pyg.Color = pyg.Color(150,150,150)):
        self.color = color
        self.pointIndex = pointIndex;

class Transform:
    def apply(self, mesh)->tuple[Vector3D]:
        return mesh.points

class Mesh:
    transform:Transform
    points:tuple[Vector3D,]
    faces:tuple[Face,]

    def __init__(self, points:tuple[Vector3D,]=None, faces:tuple[Face,]=None, transform:Transform = Transform()):
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

    def showFaces(self, cam: Camera, pygio : PygIO):
        for m in self.mesh:
            points = tuple(per_point(pygio.width, pygio.height, cam, cam.d, cam.v, p) for p in m.transformedPoints)
            for f in m.faces:
                f.camDist = _per_point_dirCam.scalar(
                    somme(*tuple(m.points[i] for i in f.pointIndex)) / len(f.pointIndex)
                )
                f.pointPers = tuple(points[i] for i in f.pointIndex)

        if len(self.mesh)==0: return;

        if len(self.mesh)==1:
            faces:list[Face] = list(self.mesh[0].faces)
        else:
            faces:list[Face] = list(concat(*[m.faces for m in self.mesh]))

        faces.sort(key = lambda x:x.camDist, reverse=True)

        for f in faces:
            if f.camDist>0:
                pygio.draw_poly(tuple(p.coord for p in f.pointPers), f.color)



