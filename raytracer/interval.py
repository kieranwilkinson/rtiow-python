from raytracer.const import INFINITY


class Interval:
    def __init__(self, min=INFINITY, max=-INFINITY) -> None:
        self.min = min
        self.max = max

    def size(self) -> float:
        return self.max - self.min

    def contains(self, x) -> bool:
        return self.min <= x <= self.max

    def surrounds(self, x) -> bool:
        return self.min < x < self.max

    def clamp(self, x) -> float:
        return max(self.min, min(x, self.max))


Interval.empty = Interval(INFINITY, -INFINITY)
Interval.universe = Interval(-INFINITY, INFINITY)
