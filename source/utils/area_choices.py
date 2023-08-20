from typing import Iterable, Optional
from geo.models import City, AreaOrCenter



def get_area_center_choices(city_id: Optional[int] = None) -> Iterable[tuple]:
    if city_id is None:
        return []

    try:
        city_instance = City.objects.get(pk=city_id)
        areas_centers = city_instance.areaorcenter_set.all()
        choices = [(area.id, area.area_or_center) for area in areas_centers]
        return choices
    except City.DoesNotExist:
        return []