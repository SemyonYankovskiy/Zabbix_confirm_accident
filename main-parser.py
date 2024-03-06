import json
import logging
import pathlib
import time
from datetime import date, datetime
from typing import Tuple, List

import schedule
from bs4 import Tag

from app.address_convert import house_splitter, address_cleaner
from app.datetime_convert import str_to_datetime_ranges, current_str_to_datetime_ranges
from app.misc import get_environ
from app.parser import (
    get_planned_outage_data,
    get_planned_outages_urls,
    get_current_outages_urls,
    get_current_outage_data,
    content_parser,
)
from geo_map.api import API

logging.basicConfig(
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logging.debug("===============\nSTART")


def get_parsed_data(content: Tag, base_time_ranges: List[Tuple[datetime, datetime]], extra) -> List[dict]:
    parsed_content = content_parser(content, base_time_ranges)
    outages = []
    for address, houses, time_ranges in parsed_content:
        if "неотложных работ" in address:
            continue
        correct_address = address_cleaner(address)
        houses_list = house_splitter(houses)
        outages_json = {
            "address": correct_address,
            "houses": houses_list,
            "times": time_ranges,
            **extra,
        }
        outages.append(outages_json)
    return outages


def parse_outages():
    list_of_outages = []

    # Плановые отключения.
    for url in get_planned_outages_urls("https://sevenergo.net"):
        data = get_planned_outage_data(url)
        if data is None:
            continue
        time_range, content = data
        base_time_ranges = str_to_datetime_ranges(time_range)
        list_of_outages.extend(get_parsed_data(data[1], base_time_ranges, extra={"type": "planned"}))

    # Текущие отключения.
    for url in get_current_outages_urls():
        data = get_current_outage_data(url)
        if data is None:
            continue
        base_time_ranges = current_str_to_datetime_ranges(data[0])
        list_of_outages.extend(get_parsed_data(data[1], base_time_ranges, extra={"type": "current"}))

    json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)

    folder = pathlib.Path(__file__).parent / "outages"
    folder.mkdir(exist_ok=True, parents=True)

    with (folder / f"{date.today()}.json").open("w", encoding="utf-8") as outfile:
        outfile.write(json_string)


def main():
    parse_outages()
    api = API(
        url=get_environ("ECSTASY_API_URL"),
        username=get_environ("ECSTASY_API_USERNAME"),
        password=get_environ("ECSTASY_API_PASSWORD"),
    )
    api.update_layer("Отключения Севэнерго", "outages/2024-03-05.geojson")


if __name__ == "__main__":
    # Каждые 2 часа запускаем скрипт
    schedule.every(2).hours.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
