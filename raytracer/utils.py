import random

from raytracer.const import PI


def deg_to_rad(degrees) -> float:
    return degrees * PI / 180.0


def random_double(min_val=0.0, max_val=1.0) -> float:
    return random.uniform(min_val, max_val)
