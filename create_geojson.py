import json
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from typing import Tuple

from geopy import Nominatim, Location

from geo_map.geojson_formatter import GeoJSON
from geo_map.ya_map import YaMap


def get_coordinates(address: str) -> Tuple[float, float]:
    geolocator = Nominatim(user_agent=str(uuid.uuid4()))
    loc: Location = geolocator.geocode(address, timeout=30)
    return loc.latitude, loc.longitude


def find_address_and_append(address: str, geojson: GeoJSON):
    try:
        ya = YaMap()
        loc = ya.get_coords(address)
    except Exception as exc:
        print(address, exc)
        return
    if not loc:
        return
    geojson.add_point((loc[1], loc[0]), properties={"description": address, "marker-color": "#ed4543"})


def main():
    """
    Открывает файл `data-YYYY-MM-DD.json` текущего дня и преобразует отключения,
    которые в данный момент актуальны в метки с координатами и создает
    новый файл `outages-YYYY-DD-MM.geojson`
    """
    try:
        data = json.load(open(f"outages/{date.today()}.json", encoding="utf-8"))
    except FileNotFoundError as exc:
        print(exc)
        return

    geojson = GeoJSON()
    now = datetime.now()

    with ThreadPoolExecutor(max_workers=200) as executor:
        for item in data:
            address = "Севастополь, " + item["address"]

            for time in item["times"]:
                # Обрабатываем только отключения, которые активны сейчас.
                if not (
                    datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S")
                    <= now
                    <= datetime.strptime(time[1], "%Y-%m-%d %H:%M:%S")
                ):
                    continue

                if not item.get("houses"):
                    executor.submit(find_address_and_append, address, geojson)
                    continue

                for house in item["houses"]:
                    address += ", " + house
                    executor.submit(find_address_and_append, address, geojson)
                    break

    geojson.create_file(f"outages/{date.today()}.geojson")


if __name__ == "__main__":
    main()
