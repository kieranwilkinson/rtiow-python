from raytracer.material import Lambertian, Metal
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

    material_ground = Lambertian(colour(0.8, 0.8, 0.0))
    material_centre = Lambertian(colour(0.1, 0.2, 0.5))
    material_left = Metal(colour(0.8, 0.8, 0.8))
    material_right = Metal(colour(0.8, 0.6, 0.2))

    world.add(Sphere(point3(0.0, -100.5, -1.0), 100.0, material=material_ground))
    world.add(Sphere(point3(0.0, 0.0, -1.2), 0.5, material=material_centre))
    world.add(Sphere(point3(-1.0, 0.0, -1.0), 0.5, material=material_left))
    world.add(Sphere(point3(1.0, 0.0, -1.0), 0.5, material=material_right))

    aspect_ratio = 16.0 / 9.0
    image_width = 600
    camera = Camera(aspect_ratio, image_width)
    camera.render(world)