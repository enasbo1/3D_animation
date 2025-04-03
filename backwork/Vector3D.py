import math

class Vector3D:
    def __init__(self, x, y, z):
        self.__coord:tuple[float, float, float] = (x, y, z)


    @staticmethod
    def zero():
            return Vector3D(0, 0, 0)

    @staticmethod
    def from_exp(axis, angle:float):
        """ crée un vecteur 3D à partir d'un axe de rotation (vecteur unitaire) et d'un angle en radians. utilise la rotation autour de l'axe donné """
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        x, y, z = axis.x, axis.y, axis.z
        
        return Vector3D(
            cos_a + (1-cos_a)*x*x,
            (1-cos_a)*x*y - sin_a*z,
            (1-cos_a)*x*z + sin_a*y
        )

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
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

    def __set_exp(self, exp:tuple["Vector3D", float]):
        """
            définit le vecteur en utilisant un axe de rotation et un angle.
            exp = (axe, angle)
        """
        axis, angle = exp
        new_vector = Vector3D.from_exp(axis, angle)
        self.__coord = new_vector.coord

    def __get_exp(self)->tuple["Vector3D", float]:
        """
            la forme exponentielle est un tuple(angle, norme);
            /!\ set & get la forme exponentielle est à faire avec moderation

            ici, __get_exp retourne un axe unitaire et l'angle associé avec une approximation basée sur le profuit scalaire
        """
        norm = self.__get_norm()
        if norm == 0:
            return Vector3D(1, 0, 0), 0 # axe x pris par défaut
        
        axis = Vector3D(self.x/norm, self.y/norm, self.z/norm)
        reference = Vector3D(1, 0, 0) if abs(axis.x) < 0.99 else Vector3D(0, 1, 0) # si x proche de 1, on évite l'angle 0 en prenant (0, 1, 0) comme vecteur unitaire
        dot_product = axis.dot(reference)

        angle = math.acos(dot_product)
        return axis, angle
    
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
    exponential:tuple["Vector3D", float] = property(__get_exp, __set_exp)