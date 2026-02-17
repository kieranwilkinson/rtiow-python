from raytracer.vec3 import vec3
from raytracer.interval import Interval
colour = vec3

def write_colour(image_ppm, pixel_colour:colour):
    r = pixel_colour.x
    g = pixel_colour.y
    b = pixel_colour.z

    intensity = Interval(0.000, 0.999)
    rbyte = int(255.999 * intensity.clamp(r))
    gbyte = int(255.999 * intensity.clamp(g))
    bbyte = int(255.999 * intensity.clamp(b))

    image_ppm.write(f"{rbyte} {gbyte} {bbyte}\n")