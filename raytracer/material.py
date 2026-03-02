from raytracer.ray import Ray
from raytracer.hittable import HitRecord
from raytracer.colour import colour
from raytracer.vec3 import vec3, random_unit_vector, reflect

class Material:
    def __init__(self):
        pass

    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> tuple[bool, colour, Ray]:
        raise NotImplementedError

class Lambertian(Material):

    def __init__(self, albedo: colour):
        super().__init__()
        self._albedo = albedo

    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> tuple[bool, colour, Ray]:
        scatter_direction = hit_record.normal + random_unit_vector()

        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        scattered = Ray(hit_record.p, scatter_direction)
        return True, self._albedo, scattered

class Metal(Material):
    def __init__(self, albedo: colour):
        super().__init__()
        self._albedo = albedo

    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> tuple[bool, colour, Ray | vec3]:
        reflected = reflect(ray_in.direction, hit_record.normal)
        scattered = Ray(hit_record.p, reflected)
        return True, self._albedo, scattered