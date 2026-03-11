import math

from raytracer.utils import random_double


class vec3:
    def __init__(self, e0=0.0, e1=0.0, e2=0.0):
        self.e = [e0, e1, e2]

    @property
    def x(self):
        return self.e[0]

    @property
    def y(self):
        return self.e[1]

    @property
    def z(self):
        return self.e[2]

    def __getitem__(self, i):
        return self.e[i]

    def __setitem__(self, i, value):
        self.e[i] = value

    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __add__(self, v):
        return vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])

    def __iadd__(self, v):
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self

    def __sub__(self, v):
        return vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])

    def __isub__(self, v):
        self.e[0] -= v.e[0]
        self.e[1] -= v.e[1]
        self.e[2] -= v.e[2]
        return self  # Added missing return

    def __mul__(self, v):
        if isinstance(v, vec3):  # vector
            return vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])
        else:  # scalar
            return vec3(self.e[0] * v, self.e[1] * v, self.e[2] * v)

    def __imul__(self, t):
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self

    def __rmul__(self, v):
        return self.__mul__(v)

    def __truediv__(self, t):
        return self.__mul__(1 / t)

    def __itruediv__(self, t):
        return self.__imul__(1 / t)

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def near_zero(self):
        s = 1e-8
        return all(math.fabs(e) < s for e in self.e)

    @classmethod
    def random(cls, min_val=0.0, max_val=1.0):
        return cls(random_double(min_val, max_val), random_double(min_val, max_val), random_double(min_val, max_val))


point3 = vec3


def dot(u, v):
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]


def cross(u, v) -> vec3:
    return vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0]
    )


def unit_vector(v):
    return v / v.length()


def random_unit_vector():
    while True:
        p = vec3.random(-1, 1)
        lensg = p.length_squared()
        if 1e-160 < lensg <= 1:
            return p / math.sqrt(lensg)


def random_on_hemisphere(normal: vec3):
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere


def reflect(v: vec3, n: vec3) -> vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: vec3, n: vec3, etai_over_etat: float) -> vec3:
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perpendicular = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perpendicular.length_squared())) * n
    return r_out_perpendicular + r_out_parallel
