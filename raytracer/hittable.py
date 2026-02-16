import math

from raytracer.vec3 import vec3, point3, dot
from raytracer.ray import Ray


class HitRecord:
    def __init__(self, p: point3 = None, normal: vec3 = None, t: float = None, front_face: bool = False):
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face

    def set_face_normal(self, ray: Ray, outward_normal: vec3):
        self.front_face = dot(ray.direction, outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable:
    def __init__(self):
        pass

    def hit(self, ray: Ray, ray_t_min: float, ray_t_max: float, hit_record: HitRecord) -> bool:
        return NotImplemented


class Sphere(Hittable):

    def __init__(self, center, radius):
        super().__init__()
        self.centre = center
        self.radius = max(0.0, radius)

    def hit(self, ray: Ray, ray_t_min: float, ray_t_max: float, hit_record: HitRecord) -> bool:
        oc = self.centre - ray.origin
        a = ray.direction.length_squared()
        h = dot(ray.direction, oc)
        c = oc.length_squared() - self.radius * self.radius

        discriminant = h * h - a * c

        if discriminant < 0:
            return False

        sqrtd = math.sqrt(discriminant)

        root = (h - sqrtd) / a
        if root <= ray_t_min or ray_t_max <= root:
            root = (h + sqrtd) / a
            if root <= ray_t_min or ray_t_max <= root:
                return False

        hit_record.t = root
        hit_record.p = ray.at(hit_record.t)
        hit_record.normal = (hit_record.p - self.centre) / self.radius

        outward_normal = (hit_record.p - self.centre) / self.radius
        hit_record.set_face_normal(ray, outward_normal)

        return True
