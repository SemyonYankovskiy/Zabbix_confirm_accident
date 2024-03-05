import json
import logging
import pathlib
from datetime import date
from typing import Tuple, List

from bs4 import Tag

from app.address_convert import house_splitter, address_cleaner
from app.datetime_convert import str_to_datetime_ranges
from app.parser import (
    get_planned_outage_data,
    get_planned_outages_urls,
    get_current_outages_urls,
    get_current_outage_data,
    content_parser,
)

logging.basicConfig(
    level=logging.DEBUG,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logging.debug("===============\nSTART")


def precess_article_data(data: Tuple[str, Tag]) -> List[dict]:
    time_range, content = data
    base_time_ranges = str_to_datetime_ranges(time_range)

    parsed_content = content_parser(content, base_time_ranges)
    outages = []
    for address, houses, time_ranges in parsed_content:
        correct_address = address_cleaner(address)
        houses_list = house_splitter(houses)
        outages_json = {
            "address": correct_address,
            "houses": houses_list,
            "times": time_ranges,
        }
        outages.append(outages_json)
    return outages


def main():
    list_of_outages = []

    for url in get_planned_outages_urls("https://sevenergo.net"):
        data = get_planned_outage_data(url)
        if data is None:
            continue
        list_of_outages.extend(precess_article_data(data))

    for url in get_current_outages_urls():
        data = get_current_outage_data(url)
        if data is None:
            continue
        list_of_outages.extend(precess_article_data(data))

    json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)

    folder = pathlib.Path(__file__).parent / "outages"
    folder.mkdir(exist_ok=True, parents=True)

    with (folder / f"{date.today()}.json").open("w", encoding="utf-8") as outfile:
        outfile.write(json_string)


if __name__ == "__main__":
    # Каждые 2 часа запускаем скрипт
    # schedule.every(2).hours.do(main)
    main()
