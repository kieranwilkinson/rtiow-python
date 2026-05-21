from raytracer.hittable import Hittable, HitRecord
from raytracer.ray import Ray
from raytracer.interval import Interval


class HittableList(Hittable):
    def __init__(self) -> None:
        super().__init__()

        self.hittable_list = []

    def add(self, hittable) -> None:
        self.hittable_list.append(hittable)

    def remove(self, hittable) -> None:
        self.hittable_list.remove(hittable)

    def clear(self) -> None:
        self.hittable_list.clear()

    def hit(self, ray: Ray, ray_t: Interval, hit_record: HitRecord) -> bool:
        temp_hit_record = HitRecord()
        hit_anything = False
        closest_so_far = ray_t.max

        for hittable in self.hittable_list:
            if hittable.hit(ray, Interval(ray_t.min, closest_so_far), temp_hit_record):
                hit_anything = True
                closest_so_far = temp_hit_record.t
                hit_record.t = temp_hit_record.t
                hit_record.p = temp_hit_record.p
                hit_record.normal = temp_hit_record.normal
                hit_record.front_face = temp_hit_record.front_face
                hit_record.material = temp_hit_record.material

        return hit_anything
