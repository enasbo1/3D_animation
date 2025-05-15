import math

from backwork.Vector2D import Vector2D
from backwork.dddirection import avixyz

class IVector3D:
    x:float
    y:float
    z:float

class Vector3D(IVector3D):
    def __init__(self, x:float, y:float, z:float):
        self.__coord:tuple[float, float, float] = (x, y, z)


    @staticmethod
    def zero():
        return Vector3D(0, 0, 0)

    @staticmethod
    def from_polar(d:float, v:float, norm:float = 1.):
        return Vector3D(*avixyz(norm, d, v))

    def scalar(self, other:IVector3D)->float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def project_h(self) -> Vector2D:
        return Vector2D(self.x, self.y)

    def __add__(self, other:IVector3D):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other:IVector3D):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, value:float|int):
        return Vector3D(self.x * value, self.y * value, self.z * value)

    def __truediv__(self, value):
        return Vector3D(self.x / value, self.y / value, self.z / value)

    def __str__(self):
        return f'Vector3({self.coord})'

    def __get_coord(self)->tuple[float, float, float]:
        return self.__coord

    def __get_x(self)->float:
        return self.__coord[0]

    def __get_y(self)->float:
        return self.__coord[1]
    
    def __get_z(self)->float:
        return self.__coord[2]

    def __set_x(self, x:float):
        self.__coord = (x, self.y, self.z);

    def __set_y(self, y:float):
        self.__coord = (self.x, y, self.z);
    
    def __set_z(self, z:float):
        self.__coord = (self.x, self.y, z);

    def __get_norm(self)->float:
        return math.sqrt(self.__get_x()**2+self.__get_y()**2+self.__get_z()**2)

    def __set_norm(self, norm:float):
        current_norm = self.__get_norm()
        if current_norm == 0:
            return # si le vecteur est nul, impossible de le normaliser. ici on évite la division par 0
        
        fact = norm/self.__get_norm()
        self.__coord = (self.__get_x() * fact, self.__get_y() * fact, self.__get_z() * fact)
    
    def dot(self, other)->float:
        """ produit scalaire entre deux vecteurs """
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross(self, other):
        """ produit vectoriel entre deux vecteurs """ 
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    coord:tuple[float, float] = property(__get_coord)
    x:float = property(__get_x, __set_x)
    y:float = property(__get_y, __set_y)
    z:float = property(__get_z, __set_z)
    norm:float = property(__get_norm, __set_norm)