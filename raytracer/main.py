from raytracer.vec3 import vec3, point3, unit_vector, dot, cross
from raytracer.colour import write_colour, colour
from raytracer.ray import Ray

import math


def hit_sphere(centre: point3, radius: float, ray: Ray):
    oc = centre - ray.origin
    a = ray.direction.length_squared()
    h = dot(ray.direction, oc)
    c = oc.length_squared() - radius * radius
    discriminant = h * h - a * c

    if discriminant < 0:
        return -1.0
    else:
        return (h - math.sqrt(discriminant)) / a


def ray_colour(ray: Ray) -> colour:
    t = hit_sphere(point3(0.0, 0.0, -1.0), 0.5, ray)

    if t > 0.0:
        N = unit_vector(ray.at(t) - vec3(0.0, 0.0, -1.0))
        return 0.5 * colour(N.x+1.0, N.y+1.0, N.z+1.0)

    unit_direction = unit_vector(ray.direction)
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * colour(1.0, 1.0, 1.0) + a * colour(0.5, 0.7, 1.0)


def ppm():
    # Image
    aspect_ratio = 16.0 / 9.0
    image_width = 400
    ih = int(image_width / aspect_ratio)
    image_height = ih if ih > 1 else 1

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * (image_width / image_height)
    camera_centre = point3(0.0, 0.0, 0.0)

    # Calculate the vectors across the horizontal and down the vertical viewport edges.
    viewport_u = vec3(viewport_width, 0.0, 0.0)
    viewport_v = vec3(0.0, -viewport_height, 0.0)

    # Calculate the horizontal and vertical delta vectors from pixel to pixel.
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    # Calculate the location of the upper left pixel.
    viewport_upper_left = camera_centre - vec3(0.0, 0.0, focal_length) - (viewport_u / 2) - (viewport_v / 2)
    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    with open('image.ppm', 'w') as image_ppm:
        image_ppm.write(f"P3\n{image_width} {image_height}\n255\n")

        for j in range(image_height):
            for i in range(image_width):
                pixel_center = pixel00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_centre  # type: ignore
                ray = Ray(camera_centre, ray_direction)
                pixel_colour = ray_colour(ray)

                write_colour(image_ppm, pixel_colour)
