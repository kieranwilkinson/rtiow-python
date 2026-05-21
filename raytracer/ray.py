from raytracer.vec3 import vec3, point3

class Ray:
    def __init__(self, origin=None, direction=None):
        self._origin = origin if origin is not None else point3()
        self._direction = direction if direction is not None else vec3()

    @property
    def origin(self) -> point3:
        return self._origin

    @property
    def direction(self) -> vec3:
        return self._direction

    def at(self, t: float) -> vec3:
        return self._origin + t * self._direction