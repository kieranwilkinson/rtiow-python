from raytracer.const import PI

import random


def deg_to_rad(degrees):
    return degrees * PI / 180.0


def random_double(min_val=0.0, max_val=1.0):
    return random.uniform(min_val, max_val)