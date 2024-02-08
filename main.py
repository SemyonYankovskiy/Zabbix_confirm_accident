import json
import logging

import bs4

from app.address_convert import address_divider, house_splitter, address_cleaner
from app.parser import get_planned_outages
from app.when_convert import str_to_datetime

logging.basicConfig(
    level=logging.DEBUG,
    filename="py_log.txt",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logging.debug("===============\nSTART main.py")
text = get_planned_outages()
list_of_outages = []
logging.info(f"Result of parsing {text}")
for outages in text:
    list_of_times = str_to_datetime(outages[1])
    logging.debug("str_to_datetime - Done")
    addresses = address_divider(bs4.BeautifulSoup(str(outages[2]), "lxml"))
    houses_list = []
    address = ""

    for address, houses in addresses:
        correct_address = address_cleaner(address)
        houses_list = house_splitter(houses)
        outages_json = {
            "address": correct_address,
            "houses": houses_list,
            "times": list_of_times,
        }
        list_of_outages.append(outages_json)


json_string = json.dumps(
    list_of_outages, indent=2, ensure_ascii=False
)  # indent для красивого форматирования

# Выводим JSON-строку
print(json_string)
