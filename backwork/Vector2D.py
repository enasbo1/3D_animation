import math

class Vector2D:
    def __init__(self, x, y):
        self.__coord:tuple[float, float] = (x, y)


    @staticmethod
    def zero():
        return Vector2D(0, 0)

    @staticmethod
    def from_exp(angle:float, norm:float):
        n = Vector2D(0, 0)
        n.exponential = angle, norm
        return n

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, value:float|int):
        return Vector2D(self.x * value, self.y * value)

    def __truediv__(self, value):
        return Vector2D(self.x / value, self.y / value)

    def __str__(self):
        return f'Vector2({self.coord})'

    def __get_coord(self)->tuple[float, float]:
        return self.__coord

    def __get_x(self)->float:
        return self.__coord[0]

    def __get_y(self)->float:
        return self.__coord[1]

    def __set_x(self, x:float):
        self.__coord = (x, self.y);

    def __set_y(self, y:float):
        self.__coord = (self.x, y);

    def __get_angle(self)->float:
        return math.atan2(self.__coord[1], self.__coord[0])

    def __get_norm(self)->float:
        return math.sqrt(self.__get_x()**2+self.__get_y()**2)

    def __set_angle(self, angle:float):
        norm = self.__get_norm()
        self.__coord = (norm*math.cos(angle), norm*math.sin(angle))

    def __set_norm(self, norm:float):
        fact = norm/self.__get_norm()
        self.__coord = (self.__get_x() * fact, self.__get_y() * fact)

    def __set_exp(self, exp:tuple[float, float]):
        """
            la forme exponentielle est un tuple(angle, norme);
            /!\ set & get la forme exponentielle est à faire avec moderation
        """
        self.__coord = (exp[1]*math.cos(exp[0]), exp[1]*math.sin(exp[0]))

    def __get_exp(self)->tuple[float, float]:
        """
            la forme exponentielle est un tuple(angle, norme);
            /!\ set & get la forme exponentielle est à faire avec moderation
        """
        return self.__get_angle(), self.__get_norm()

    coord:tuple[float, float] = property(__get_coord)
    x:float = property(__get_x, __set_x)
    y:float = property(__get_y, __set_y)
    angle:float = property(__get_angle, __set_angle)
    norm:float = property(__get_norm, __set_norm)
    exponential:tuple[float, float] = property(__get_exp, __set_exp)
