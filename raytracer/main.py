from raytracer.vec3 import vec3, point3, unit_vector, dot, cross
from raytracer.colour import write_colour, colour
from raytracer.ray import Ray
from raytracer.hittable import HitRecord, Hittable
from raytracer.sphere import Sphere
from raytracer.hittable_list import HittableList
from raytracer.interval import Interval
from raytracer.const import INFINITY, PI
from raytracer.utils import deg_to_rad, random_double
from raytracer.camera import Camera

import math

def render_world():
    world = HittableList()
    world.add(Sphere(point3(0.0, 0.0, -1.0), 0.5))
    world.add(Sphere(point3(0.0, -100.5, -1.0), 100))

    aspect_ratio = 16.0 / 9.0
    image_width = 600
    camera = Camera(aspect_ratio, image_width)
    camera.render(world)