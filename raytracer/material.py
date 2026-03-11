import math

from raytracer.ray import Ray
from raytracer.hittable import HitRecord
from raytracer.colour import colour
from raytracer.vec3 import vec3, random_unit_vector, reflect, unit_vector, dot, refract
from raytracer.utils import random_double

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
    def __init__(self, albedo: colour, fuzz: float):
        super().__init__()
        self._albedo = albedo
        self._fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> tuple[bool, colour, Ray | vec3]:
        r = reflect(ray_in.direction, hit_record.normal)
        reflected = unit_vector(r) + (self._fuzz * random_unit_vector())
        scattered = Ray(hit_record.p, reflected)
        did_scatter = (dot(scattered.direction, hit_record.normal) > 0)
        return did_scatter, self._albedo, scattered


class Dielectric(Material):
    def __init__(self, index_of_refraction: float):
        super().__init__()
        self._index_of_refraction = index_of_refraction

    def scatter(self, ray_in: Ray, hit_record: HitRecord) -> tuple[bool, colour, Ray]:
        attenuation = colour(1.0, 1.0, 1.0)
        ri = 1.0 / self._index_of_refraction if hit_record.front_face else self._index_of_refraction
        unit_direction = unit_vector(ray_in.direction)
        cos_theta = min(dot(-unit_direction, hit_record.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = ri * sin_theta > 1.0
        reflected = reflect(unit_direction, hit_record.normal)
        refracted = refract(unit_direction, hit_record.normal, ri)

        direction = (
            reflected
            if cannot_refract or self._reflectance(cos_theta) > random_double()
            else refracted
        )

        scattered = Ray(hit_record.p, direction)
        return True, attenuation, scattered

    def _reflectance(self, cosine: float):
        r0 = (1 - self._index_of_refraction) / (1 + self._index_of_refraction)
        r0 = r0 * r0
        return r0 + (1-r0)*pow((1-cosine), 5)