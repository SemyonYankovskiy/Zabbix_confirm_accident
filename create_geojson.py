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


def find_address_and_append(address: str, time_range: str, marker_color: str, geojson: GeoJSON):
    try:
        ya = YaMap()
        print(address)
        loc = ya.get_coords(address)
    except Exception as exc:
        print(address, exc)
        return
    if not loc:
        return
    geojson.add_point(
        (loc[1], loc[0]),
        properties={
            "iconCaption": time_range,
            "description": address + "\n" + time_range,
            "marker-color": marker_color,
        },
    )


def run():
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

            for time in item["times"]:
                time_from = datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S")
                time_to = datetime.strptime(time[1], "%Y-%m-%d %H:%M:%S")
                # Обрабатываем только отключения, которые активны сейчас.
                if time_from.date() != now.date():
                    continue

                time_range = f"с {time_from.strftime('%H:%M')} до {time_to.strftime('%H:%M')}"
                marker_color = "#FF0000" if item["type"] == "current" else "#FF6800"

                if not item.get("houses"):
                    address = "Севастополь, " + item["address"]
                    executor.submit(find_address_and_append, address, time_range, marker_color, geojson)
                    continue

                for house in item["houses"]:
                    address = "Севастополь, " + item["address"] + ", " + house
                    executor.submit(find_address_and_append, address, time_range, marker_color, geojson)

    geojson.create_file(f"outages/{date.today()}.geojson")


if __name__ == "__main__":
    run()
