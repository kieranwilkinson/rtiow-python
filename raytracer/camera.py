import math
import sys
import time
from pathlib import Path

from raytracer.colour import colour, write_colour
from raytracer.const import INFINITY
from raytracer.hittable import HitRecord, Hittable
from raytracer.interval import Interval
from raytracer.ray import Ray
from raytracer.utils import deg_to_rad, random_double
from raytracer.vec3 import cross, point3, random_in_unit_disk, unit_vector, vec3


class Camera:
    def __init__(self, aspect_ratio: float, image_width: int) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = 5
        self.max_depth = 10
        self.vertical_fov = 90
        self.look_from = point3(0, 0, 0)
        self.look_at = point3(0, 0, -1)
        self.vup = vec3(0, 1, 0)
        self.defocus_angle = 0
        self.focal_distance = 10

    def _initialize(self) -> None:
        self.pixel_sample_scale = 1.0 / self.samples_per_pixel

        ih = int(self.image_width / self.aspect_ratio)
        self.image_height = ih if ih > 1 else 1

        self.camera_centre = self.look_from

        # Camera
        self.focal_length = (self.look_from - self.look_at).length()
        theta = deg_to_rad(self.vertical_fov)
        h = math.tan(theta / 2)
        self.viewport_height = 2.0 * h * self.focal_distance
        self.viewport_width = self.viewport_height * (self.image_width / self.image_height)

        # Calculate the u,v,w unit basis vectors for the camera coordinate frame.
        w = unit_vector(self.look_from - self.look_at)
        u = unit_vector(cross(self.vup, w))
        v = cross(w, u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        self.viewport_u = self.viewport_width * u
        self.viewport_v = self.viewport_height * -v

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        # Calculate the location of the upper left pixel.
        self.viewport_upper_left = (
            self.camera_centre
            - (self.focal_distance * w)
            - self.viewport_u / 2
            - self.viewport_v / 2
        )
        self.pixel00_loc = self.viewport_upper_left + 0.5 * (
            self.pixel_delta_u + self.pixel_delta_v
        )

        # Calculate the camera defocus disk basis vectors.
        self.defocus_radius = self.focal_distance * math.tan(deg_to_rad(self.defocus_angle) / 2)
        self.defocus_disk_u = self.defocus_radius * u
        self.defocus_disk_v = self.defocus_radius * v

    def render(self, world: Hittable, output_path: Path = Path("output") / "image.ppm") -> None:
        self._initialize()

        with open(output_path, "w") as image_ppm:
            image_ppm.write(f"P3\n{self.image_width} {self.image_height}\n255\n")

            for j in range(self.image_height):
                for i in range(self.image_width):
                    pixel_colour = colour(0, 0, 0)
                    for _sample in range(self.samples_per_pixel):
                        r = self._get_ray(i, j)
                        pixel_colour += self._ray_colour(ray=r, depth=self.max_depth, world=world)
                    write_colour(image_ppm, self.pixel_sample_scale * pixel_colour)
                    print(f"{j=}, {i=}")

    def _ray_colour(self, ray: Ray, depth: int, world: Hittable) -> colour:
        if depth <= 0:
            return colour(0, 0, 0)

        hit_record = HitRecord()

        if world.hit(ray, Interval(0.001, INFINITY), hit_record):
            did_scatter, attenuation, scattered = hit_record.material.scatter(ray, hit_record)
            return (
                attenuation * self._ray_colour(ray=scattered, depth=depth - 1, world=world)
                if did_scatter
                else colour(0, 0, 0)
            )

        unit_direction = unit_vector(ray.direction)
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * colour(1.0, 1.0, 1.0) + a * colour(0.5, 0.7, 1.0)

    def _get_ray(self, i: int, j: int) -> Ray:
        # Construct a camera ray originating from the defocus disk and directed at a randomly
        # sampled point around the pixel location i, j.
        offset = self._sample_square()
        pixel_sample = (
            self.pixel00_loc
            + ((i + offset.x) * self.pixel_delta_u)
            + ((j + offset.y) * self.pixel_delta_v)
        )

        ray_origin = self.camera_centre if self.defocus_angle <= 0 else self.defocus_disk_sample()
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    @staticmethod
    def _sample_square() -> vec3:
        return vec3(random_double() - 0.5, random_double() - 0.5, 0)

    def defocus_disk_sample(self) -> point3:
        p = random_in_unit_disk()
        return self.camera_centre + (p[0] * self.defocus_disk_u) + (p[1] * self.defocus_disk_v)
