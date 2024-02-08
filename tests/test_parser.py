import json
from unittest import TestCase

import bs4

from app.address_convert import address_divider, address_converter, house_splitter
from app.parser import connect_and_get_resp, planned_parser
from app.when_convert import str_to_datetime


class TestParser(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/697.html"

    def test_parser(self):
        outage = planned_parser(connect_and_get_resp(self.url))
        res = []

        list_of_times = str_to_datetime(outage[1])
        addresses = address_divider(bs4.BeautifulSoup(str(outage[2]), "lxml"))
        for address, houses in addresses:
            correct_address = address_converter(address)
            houses_list = house_splitter(houses)
            outages_json = {
                "address": correct_address,
                "houses": houses_list,
                "times": list_of_times,
            }
            res.append(outages_json)

        print(json.dumps(res, indent=2, ensure_ascii=False, default=str))
