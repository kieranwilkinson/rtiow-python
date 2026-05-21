import math

from raytracer.hittable import Hittable, HitRecord
from raytracer.interval import Interval
from raytracer.ray import Ray
from raytracer.vec3 import dot


class Sphere(Hittable):

    def __init__(self, center, radius, material) -> None:
        super().__init__()
        self.centre = center
        self.radius = max(0.0, radius)
        self.material = material

    def hit(self, ray: Ray, ray_t: Interval, hit_record: HitRecord) -> bool:
        oc = self.centre - ray.origin
        a = ray.direction.length_squared()
        h = dot(ray.direction, oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c

        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        root = (h - sqrtd) / a
        if not ray_t.surrounds(root):
            root = (h + sqrtd) / a
            if not ray_t.surrounds(root):
                return False

        hit_record.t = root
        hit_record.p = ray.at(hit_record.t)
        hit_record.normal = (hit_record.p - self.centre) / self.radius

        outward_normal = (hit_record.p - self.centre) / self.radius
        hit_record.set_face_normal(ray, outward_normal)
        hit_record.material = self.material
        return True