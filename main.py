import datetime

import bs4
from app.parser import get_planned_outages
from app.address_convert import address_divider, house_splitter, adress_converter
from app.when_convert import str_to_datetime
import json
import logging

logging.basicConfig(level=logging.DEBUG, filename="py_log.txt",filemode="a",
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

logging.debug("===============\nSTART main.py")
text = get_planned_outages()
list_of_outages = []
logging.info(f"Result of parsing {text}")
for outages in text:
    list_of_time = str_to_datetime(outages[1])

    list_of_time = list(filter(lambda d: d.date() == datetime.date.today(), list_of_time))

    print(datetime.date.today())
    logging.debug("str_to_datetime - Done")
    addresses = address_divider(bs4.BeautifulSoup(str(outages[2]), 'lxml'))
    houses_list = []
    address = ""

    for address, houses in addresses:
        correct_address = adress_converter(address)
        houses_list = house_splitter(houses)
        outages_json = {
            "address": correct_address,
            "houses": houses_list,
            "time_from": str(list_of_time[0]),
            "time_to": str(list_of_time[1]),
        }
        list_of_outages.append(outages_json)



json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False)  # indent для красивого форматирования

# Выводим JSON-строку
print(json_string)
