import json
from pathlib import Path
from typing import Tuple, Union


class GeoJSON:
    def __init__(self, **metadata):
        self._id = 1
        self._geojson = {
            "type": "FeatureCollection",
            "features": [],
        }
        if metadata:
            self._geojson["metadata"] = metadata

    def add_point(self, coordinates: Tuple[float, float], properties) -> None:
        self._geojson["features"].append(
            {
                "type": "Feature",
                "id": self._id,
                "geometry": {"coordinates": coordinates, "type": "Point"},
                "properties": properties,
            }
        )
        self._id += 1

    @property
    def geojson(self) -> dict:
        return self._geojson

    def create_file(self, file_path: Union[str, Path]) -> None:
        geojson_string = json.dumps(self._geojson, indent=2, ensure_ascii=True, default=str)
        with open(file_path, "w", encoding="utf-8") as outfile:
            outfile.write(geojson_string)

    def __len__(self):
        return len(self._geojson["features"])

    def __iter__(self):
        return iter(self._geojson["features"])

    @staticmethod
    def reverse_coordinates(geojson: dict):
        for feature in geojson["features"]:
            feature["geometry"]["coordinates"] = feature["geometry"]["coordinates"][::-1]
        return geojson
