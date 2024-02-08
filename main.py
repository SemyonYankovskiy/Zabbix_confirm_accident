import json
import logging

from app.address_convert import house_splitter, address_cleaner
from app.parser import get_planned_outage_data, get_planned_outages_urls, content_parser
from app.when_convert import str_to_datetime_ranges

logging.basicConfig(
    level=logging.DEBUG,
    filename="py_log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logging.debug("===============\nSTART main.py")


def main():
    list_of_outages = []

    for url in get_planned_outages_urls("https://sevenergo.net"):
        time_range, content = get_planned_outage_data(url)
        base_time_ranges = str_to_datetime_ranges(time_range)

        parsed_content = content_parser(content, base_time_ranges)

        for address, houses, time_ranges in parsed_content:
            correct_address = address_cleaner(address)
            houses_list = house_splitter(houses)
            outages_json = {
                "address": correct_address,
                "houses": houses_list,
                "times": time_ranges,
            }
            list_of_outages.append(outages_json)

    # indent для красивого форматирования
    json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False)
    # Выводим JSON-строку
    print(json_string)


if __name__ == "__main__":
    main()
