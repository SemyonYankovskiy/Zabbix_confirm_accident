import json
from datetime import datetime
from unittest import TestCase

import bs4

from app.address_convert import address_divider, address_converter, house_splitter
from app.parser import connect_and_get_resp, planned_parser
from app.when_convert import str_to_datetime


class TestParser(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/697.html"
        cls.valid = [
                {
                    "address": "ул. Севастопольская зона ЮБК",
                    "houses": [
                        "5",
                        "19",
                        "19а",
                        "53/118",
                        "53/131",
                        "53/111",
                        "53/136",
                        "53/69",
                        "53/100",
                        "53/95",
                        "53/99",
                        "111",
                        "136",
                        "53/143",
                        "1607"
                    ],
                    "times": [
                        [
                            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S")
                        ]
                    ]
                },
                {
                    "address": "пос. Ласпи",
                    "houses": [
                        "53/134"
                    ],
                    "times": [
                        [
                            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S")
                        ]
                    ]
                },
                {
                    "address": "зона ЮБК-24",
                    "houses": [
                        "21",
                        "23",
                        "22",
                        "24"
                    ],
                    "times": [
                        [
                            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S")
                        ]
                    ]
                },
                {
                    "address": "Южнобережное шоссе",
                    "houses": [
                        "40"
                    ],
                    "times": [
                        [
                            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S")
                        ]
                    ]
                },
                {
                    "address": "ЮБК-6",
                    "houses": [
                        "40",
                        "42",
                        "44",
                        "41",
                        "43",
                        "45"
                    ],
                    "times": [
                        [
                            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S")
                        ]
                    ]
                }
            ]

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

        self.assertEqual(self.valid, res)
