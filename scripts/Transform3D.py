from backwork.Quaternion import Quaternion
from backwork.Vector3D import Vector3D
from meshs.Mesh import Transform, Mesh


class Transform3D(Transform):
    rotation : Quaternion
    position : Vector3D
    scale : Vector3D

    def __init__(self):
        self.position = Vector3D.zero()
        self.rotation = Quaternion.identity()
        self.scale = Vector3D.one()

    def apply(self, mesh:Mesh) -> tuple[Vector3D]:

        # application de la position
        points : list[Vector3D] = [self.rotation.rotate_point(i)+self.position for i in mesh.points]
        return tuple(points)

    def copy(self):
        newCopy = Transform3D()
        newCopy.position = self.position
        newCopy.rotation = self.rotation
        newCopy.scale = self.scale
        return newCopy
