from abc import ABC, abstractmethod

from raytracer.interval import Interval
from raytracer.ray import Ray
from raytracer.vec3 import dot, point3, vec3


class HitRecord:
    def __init__(
        self,
        p: point3 | None = None,
        normal: vec3 | None = None,
        t: float | None = None,
        front_face: bool = False,
        material = None,
    ) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.material = material

    def set_face_normal(self, ray: Ray, outward_normal: vec3) -> None:
        self.front_face = dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, ray: Ray, interval: Interval, hit_record: HitRecord) -> bool:
        raise NotImplementedError