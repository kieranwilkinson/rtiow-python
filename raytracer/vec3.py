import math

from raytracer.utils import random_double


class vec3:
    def __init__(self, e0=0.0, e1=0.0, e2=0.0) -> None:
        self.e = [e0, e1, e2]

    @property
    def x(self) -> float:
        return self.e[0]

    @property
    def y(self) -> float:
        return self.e[1]

    @property
    def z(self) -> float:
        return self.e[2]

    def __getitem__(self, i) -> float:
        return self.e[i]

    def __setitem__(self, i, value) -> None:
        self.e[i] = value

    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __add__(self, v) -> "vec3":
        return vec3(self.e[0] + v.e[0], self.e[1] + v.e[1], self.e[2] + v.e[2])

    def __iadd__(self, v: "vec3") -> "vec3":
        self.e[0] += v.e[0]
        self.e[1] += v.e[1]
        self.e[2] += v.e[2]
        return self

    def __sub__(self, v: "vec3") -> "vec3":
        return vec3(self.e[0] - v.e[0], self.e[1] - v.e[1], self.e[2] - v.e[2])

    def __isub__(self, v: "vec3") -> "vec3":
        self.e[0] -= v.e[0]
        self.e[1] -= v.e[1]
        self.e[2] -= v.e[2]
        return self

    def __mul__(self, v: "vec3 | float") -> "vec3":
        if isinstance(v, vec3):  # vector
            return vec3(self.e[0] * v.e[0], self.e[1] * v.e[1], self.e[2] * v.e[2])

        return vec3(self.e[0] * v, self.e[1] * v, self.e[2] * v)  # scalar

    def __imul__(self, t: float) -> "vec3":
        self.e[0] *= t
        self.e[1] *= t
        self.e[2] *= t
        return self

    def __rmul__(self, v: "vec3 | float") -> "vec3":
        return self.__mul__(v)

    def __truediv__(self, t: float) -> "vec3":
        return self.__mul__(1 / t)

    def __itruediv__(self, t: float) -> "vec3":
        return self.__imul__(1 / t)

    def length(self) -> float:
        return math.sqrt(self.length_squared())

    def length_squared(self) -> float:
        return self.e[0] * self.e[0] + self.e[1] * self.e[1] + self.e[2] * self.e[2]

    def near_zero(self) -> bool:
        return all(math.fabs(e) < 1e-8 for e in self.e)

    @classmethod
    def random(cls, min_val: float = 0.0, max_val: float = 1.0) -> "vec3":
        return cls(
            random_double(min_val, max_val),
            random_double(min_val, max_val),
            random_double(min_val, max_val),
        )


point3 = vec3


def dot(u: vec3, v: vec3) -> float:
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]


def cross(u: vec3, v: vec3) -> vec3:
    return vec3(
        u.e[1] * v.e[2] - u.e[2] * v.e[1],
        u.e[2] * v.e[0] - u.e[0] * v.e[2],
        u.e[0] * v.e[1] - u.e[1] * v.e[0],
    )


def unit_vector(v: vec3) -> vec3:
    return v / v.length()


def random_unit_vector() -> vec3:
    while True:
        p = vec3.random(-1, 1)
        lensg = p.length_squared()
        if 1e-160 < lensg <= 1:
            return p / math.sqrt(lensg)


def random_in_unit_disk() -> vec3:
    while True:
        p = vec3(random_double(-1, 1), random_double(-1, 1), 0)
        if p.length_squared() < 1:
            return p


def random_on_hemisphere(normal: vec3) -> vec3:
    on_unit_sphere = random_unit_vector()
    if dot(on_unit_sphere, normal) > 0.0:
        return on_unit_sphere

    return -on_unit_sphere


def reflect(v: vec3, n: vec3) -> vec3:
    return v - 2 * dot(v, n) * n


def refract(uv: vec3, n: vec3, etai_over_etat: float) -> vec3:
    cos_theta = min(dot(-uv, n), 1.0)
    r_out_perpendicular = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -math.sqrt(abs(1.0 - r_out_perpendicular.length_squared())) * n
    return r_out_perpendicular + r_out_parallel
