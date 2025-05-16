from backwork.Quaternion import Quaternion
from backwork.Vector3D import Vector3D
from meshs.Mesh import Transform, Mesh


class Transform3D(Transform):
    rotation : Quaternion
    position : Vector3D
    scale : Vector3D


    def apply(self, mesh:Mesh) -> tuple[Vector3D]:

        # application de la position
        points : list[Vector3D] = [i+self.position for i in mesh]
        return tuple(points)

