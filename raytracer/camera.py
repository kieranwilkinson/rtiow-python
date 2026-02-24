from raytracer.hittable import Hittable, HitRecord
from raytracer.interval import Interval
from raytracer.const import INFINITY
from raytracer.ray import Ray
from raytracer.colour import write_colour, colour
from raytracer.vec3 import vec3, unit_vector, point3, random_unit_vector, random_on_hemisphere
from raytracer.utils import deg_to_rad, random_double

import logging

logger = logging.getLogger(__name__)


class Camera:

    def __init__(self, aspect_ratio, image_width):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = 5
        self.max_depth = 10

        self.pixel_sample_scale = 1.0 / self.samples_per_pixel

        ih = int(self.image_width / self.aspect_ratio)
        self.image_height = ih if ih > 1 else 1

        self.camera_centre = point3(0.0, 0.0, 0.0)

        # Camera
        self.focal_length = 1.0
        self.viewport_height = 2.0
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        self.viewport_u = vec3(self.viewport_width, 0.0, 0.0)
        self.viewport_v = vec3(0.0, -self.viewport_height, 0.0)

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        self.viewport_upper_left = self.camera_centre - vec3(0.0, 0.0, self.focal_length) - (self.viewport_u / 2) - (
                self.viewport_v / 2)
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)

    def render(self, world: Hittable):
        with open('image.ppm', 'w') as image_ppm:
            image_ppm.write(f"P3\n{self.image_width} {self.image_height}\n255\n")

            for j in range(self.image_height):
                for i in range(self.image_width):
                    pixel_colour = colour(0, 0, 0)
                    for sample in range(self.samples_per_pixel):
                        r = self._get_ray(i, j)
                        pixel_colour += self._ray_colour(ray=r, depth=self.max_depth, world=world)
                    write_colour(image_ppm, self.pixel_sample_scale * pixel_colour)

    def _ray_colour(self, ray: Ray, depth: int, world: Hittable) -> colour:
        if depth <= 0:
            return colour(0, 0, 0)

        hit_record = HitRecord()

        if world.hit(ray, Interval(0.001, INFINITY), hit_record):
            direction = random_on_hemisphere(hit_record.normal)
            return 0.5 * self._ray_colour(ray=Ray(hit_record.p, direction), depth=depth-1, world=world)

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * colour(1.0, 1.0, 1.0) + a * colour(0.5, 0.7, 1.0)

    def _get_ray(self, i: int, j: int):
        offset = self._sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + (
                    (j + offset.y) * self.pixel_delta_v)

        ray_origin = self.camera_centre
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    @staticmethod
    def _sample_square():
        return vec3(random_double() - 0.5, random_double() - 0.5, 0)
