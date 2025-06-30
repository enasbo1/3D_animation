import math

from backwork.Vector3D import Vector3D


class Quaternion:
    r: float
    i: float
    j: float
    k: float

    def __init__(self, r: float, i: float, j: float, k: float):
        self.r = r
        self.i = i
        self.j = j
        self.k = k

    @staticmethod
    def identity():
        return Quaternion(1, 0, 0, 0)

    def __eq__(self, other):
        if not isinstance(other, Quaternion):
            return NotImplemented
        return (math.isclose(self.r, other.r) and
                math.isclose(self.i, other.i) and
                math.isclose(self.j, other.j) and
                math.isclose(self.k, other.k))

    def __str__(self):
        return f"({round(self.r, 5)}, {round(self.i, 5)}, {round(self.j, 5)}, {round(self.k, 5)})"

    def __add__(self, other):
        return Quaternion(
            self.r + other.r,
            self.i + other.i,
            self.j + other.j,
            self.k + other.k
        )

    def __sub__(self, other):
        return Quaternion(
            self.r - other.r,
            self.i - other.i,
            self.j - other.j,
            self.k - other.k
        )

    def __mul__(self, other):
        return Quaternion(
            self.r * other.r - self.i * other.i - self.j * other.j - self.k * other.k,
            self.r * other.i + self.i * other.r + self.j * other.k - self.k * other.j,
            self.r * other.j - self.i * other.k + self.j * other.r + self.k * other.i,
            self.r * other.k + self.i * other.j - self.j * other.i + self.k * other.r
        )

    def __repr__(self):
        return f"Quaternion({round(self.r, 4)}, {self.i}, {self.j}, {self.k})"

    def conj(self):
        return Quaternion(self.r, -self.i, -self.j, -self.k)

    def norm(self):
        return math.sqrt(self.r**2 + self.i**2 + self.j**2 + self.k**2)

    def unit(self):
        n = self.norm()
        if n > 0:
            return Quaternion(self.r / n, self.i / n, self.j / n, self.k / n)

    def dot(self, other) -> float:
        return (self.r * other.r) + (self.i * other.i) + (self.j * other.j) + (self.k * other.k)

    @staticmethod
    def fromVector3D(vector: Vector3D):
        return Quaternion(0, vector.x, vector.y, vector.z)

    @staticmethod
    def fromMatrix4x4(matrix: [[float, float, float, float],
                               [float, float, float, float],
                               [float, float, float, float],
                               [float, float, float, float]]):
        return Quaternion(matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0])

    def toMatrix4x4(self):
        r, i, j, k = self.r, self.i, self.j, self.k
        return [
            [r, -i, -j, -k],
            [i, r, -k, j],
            [j, k, r, i],
            [k, -j, i, r]
        ]

    def toV3Matrix(self) -> list[list[float]]:
        r, i, j, k = self.r, self.i, self.j, self.k
        return [
            [
                1 - 2 * (j * j + k * k),
                2 * (i * j - k * r),
                2 * (i * k + j * r)
            ],
            [
                2 * (i * j + k * r),
                1 - 2 * (i * i + k * k),
                2 * (j * k - i * r)
            ],
            [
                2 * (i * k - j * r),
                2 * (j * k + i * r),
                1 - 2 * (i * i + j * j)
            ]
        ]

    @staticmethod
    def fromV3Matrix(matrix):
        m00, m01, m02 = matrix[0]
        m10, m11, m12 = matrix[1]
        m20, m21, m22 = matrix[2]

        trace = m00 + m11 + m22

        if trace > 0:
            # s: intermediate scale factor,
            # avoid dividing by 0 and precision loss,
            # normalize the quaternion
            s = 0.5 / math.sqrt(trace + 1.0)
            r = 0.25 / s
            i = (m21 - m12) * s
            j = (m02 - m20) * s
            k = (m10 - m01) * s
        elif (m00 > m11) and (m00 > m22):
            s = 2.0 * math.sqrt(1.0 + m00 - m11 - m22)
            r = (m21 - m12) / s
            i = 0.25 * s
            j = (m01 + m10) / s
            k = (m02 + m20) / s
        elif m11 > m22:
            s = 2.0 * math.sqrt(1.0 + m11 - m00 - m22)
            r = (m02 - m20) / s
            i = (m01 + m10) / s
            j = 0.25 * s
            k = (m12 + m21) / s
        else:
            s = 2.0 * math.sqrt(1.0 + m22 - m00 - m11)
            r = (m10 - m01) / s
            i = (m02 + m20) / s
            j = (m12 + m21) / s
            k = 0.25 * s

        return Quaternion(r, i, j, k)
    
    @staticmethod
    def rotation(axis: Vector3D, angle: float):
        # Normalize axis
        axis_norm = axis.norm
        if axis_norm > 0:
            axis = axis / axis_norm
        else:
            return Quaternion(1, 0, 0, 0)  # Identity quaternion
        
        half_angle = angle / 2
        cos_a = math.cos(half_angle)
        sin_a = math.sin(half_angle)
        
        return Quaternion(cos_a, sin_a * axis.x, sin_a * axis.y, sin_a * axis.z)
    
    def rotate_point(self, point: Vector3D) -> Vector3D:
        p = Quaternion(0, point.x, point.y, point.z)
        q_conj = self.conj()
        rotated = self * p * q_conj
        
        return Vector3D(rotated.i, rotated.j, rotated.k)
