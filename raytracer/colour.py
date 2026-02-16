from raytracer.vec3 import vec3

colour = vec3

def write_colour(image_ppm, pixel_colour:colour):
    r = pixel_colour.x
    g = pixel_colour.y
    b = pixel_colour.z

    rbyte = int(255.999 * r)
    gbyte = int(255.999 * g)
    bbyte = int(255.999 * b)

    image_ppm.write(f"{rbyte} {gbyte} {bbyte}\n")
