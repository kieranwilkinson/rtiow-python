from raytracer.camera import Camera
from raytracer.colour import colour
from raytracer.hittable_list import HittableList
from raytracer.material import Dielectric, Lambertian, Metal
from raytracer.sphere import Sphere
from raytracer.utils import random_double
from raytracer.vec3 import point3, vec3


def render_demo_scene():
    world = HittableList()

    material_ground = Lambertian(colour(0.5, 0.5, 0.5))
    world.add(Sphere(point3(0, -1000, 0), 1000, material_ground))

    for a in range(-11, 11):
        for b in range(-11, 11):

            choose_material = random_double()
            centre = point3(a + 0.9 * random_double(), 0.2, b + 0.9 * random_double())

            if (centre - point3(4, 0.2, 0)).length() > 0.9:
                if choose_material < 0.8:
                    # diffuse
                    albedo = colour.random() * colour.random()
                    material = Lambertian(albedo)
                    world.add(Sphere(centre, 0.2, material))
                elif choose_material < 0.95:
                    # metal
                    albedo = colour.random(0.5, 1)
                    fuzz = random_double(0, 0.5)
                    material = Metal(albedo, fuzz)
                    world.add(Sphere(centre, 0.2, material))
                else:
                    # glass
                    material = Dielectric(1.5)
                    world.add(Sphere(centre, 0.2, material))

    material_dielectric = Dielectric(1.5)
    world.add(Sphere(point3(0, 1, 0), 1.0, material_dielectric))
    material_lambertian = Lambertian(colour(0.4, 0.2, 0.1))
    world.add(Sphere(point3(-4, 1, 0), 1.0, material_lambertian))
    material_metal = Metal(colour(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(point3(4, 1, 0), 1.0, material_metal))

    camera = Camera(16.0 / 9.0, 24)
    camera.samples_per_pixel = 5
    camera.max_depth = 5

    camera.vertical_fov = 20
    camera.look_from = point3(13, 2, 3)
    camera.look_at = point3(0, 0, 0)
    camera.vup = vec3(0, 1, 0)

    camera.defocus_angle = 0.6
    camera.focal_distance = 10

    camera.render(world)