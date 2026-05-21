
from raytracer.camera import Camera
from raytracer.colour import colour
from raytracer.hittable_list import HittableList
from raytracer.material import Dielectric, Lambertian, Metal
from raytracer.sphere import Sphere
from raytracer.vec3 import point3, vec3


def render_demo_scene():
    world = HittableList()

    material_ground = Lambertian(colour(1.0, 0.0, 0.5))
    material_centre = Lambertian(colour(0.1, 0.2, 0.5))
    material_left = Dielectric(1.5)
    material_bubble = Dielectric(1.00 / 1.5)
    material_right = Metal(colour(0.8, 0.6, 0.2), 1.0)

    world.add(Sphere(point3(0.0, -100.5, -1.0), 100.0, material=material_ground))
    world.add(Sphere(point3(0.0, 0.0, -1.2), 0.5, material=material_centre))
    world.add(Sphere(point3(-1.0, 0.0, -1.0), 0.5, material=material_left))
    world.add(Sphere(point3(-1.0, 0.0, -1.0), 0.4, material=material_bubble))
    world.add(Sphere(point3(1.0, 0.0, -1.0), 0.5, material=material_right))

    aspect_ratio = 16.0 / 9.0
    image_width = 1080

    camera = Camera(aspect_ratio, image_width)
    camera.vertical_fov = 35
    camera.look_from = point3(-2, 2, 1)
    camera.look_at = point3(0, 0, -1)
    camera.vup = vec3(0, 1, 0)
    camera.defocus_angle = 10
    camera.focal_distance = 3.4
    camera.render(world)
