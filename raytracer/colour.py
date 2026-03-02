import math

from raytracer.vec3 import vec3
from raytracer.interval import Interval

colour = vec3


def linear_to_gamma(linear_component: float):
    return math.sqrt(linear_component) if linear_component > 0 else 0


def write_colour(image_ppm, pixel_colour: colour):
    r = pixel_colour.x
    g = pixel_colour.y
    b = pixel_colour.z

    intensity = Interval(0.000, 0.999)
    rbyte = int(255.999 * intensity.clamp(linear_to_gamma(r)))
    gbyte = int(255.999 * intensity.clamp(linear_to_gamma(g)))
    bbyte = int(255.999 * intensity.clamp(linear_to_gamma(b)))

    image_ppm.write(f"{rbyte} {gbyte} {bbyte}\n")
