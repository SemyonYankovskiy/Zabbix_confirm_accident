from datetime import datetime
from unittest import TestCase

from app.address_convert import address_cleaner, house_splitter
from app.parser import content_parser, get_planned_outage_data
from app.when_convert import str_to_datetime_ranges


class TestParser(TestCase):

    def test_parser(self):
        res = []
        class_name = self.__class__.__name__

        time_range, content = get_planned_outage_data(self.url)
        print(f"{class_name} time_range: {time_range} content: {content}")
        base_time_ranges = str_to_datetime_ranges(time_range)
        print(f"{class_name} base_time_ranges: {base_time_ranges}")

        parsed_content = content_parser(content, base_time_ranges)
        print(f"{class_name} parsed_content: {parsed_content}")

        for address, houses, time_ranges in parsed_content:
            correct_address = address_cleaner(address)
            houses_list = house_splitter(houses)
            outages_json = {
                "address": correct_address,
                "houses": houses_list,
                "times": time_ranges,
            }
            res.append(outages_json)

        print(f"{class_name} {res}")

        self.assertEqual(self.valid, res)

    @classmethod
    def setUpClass(cls) -> None:
        cls.url = (
            "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/697.html"
        )
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
                    "1607",
                ],
                "times": [
                    (
                        datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
                    )
                ],
            },
            {
                "address": "пос. Ласпи",
                "houses": ["53/134"],
                "times": [
                    (
                        datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
                    )
                ],
            },
            {
                "address": "зона ЮБК-24",
                "houses": ["21", "23", "22", "24"],
                "times": [
                    (
                        datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
                    )
                ],
            },
            {
                "address": "Южнобережное шоссе",
                "houses": ["40"],
                "times": [
                    (
                        datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
                    )
                ],
            },
            {
                "address": "ЮБК-6",
                "houses": ["40", "42", "44", "41", "43", "45"],
                "times": [
                    (
                        datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                        datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
                    )
                ],
            },
        ]


class TestParser2(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = (
            "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/696.html"
        )
        cls.valid = [
            {
                "address": "ул. Колобова",
                "houses": ["21Б", "21В", "21Г"],
                "times": [
                    (
                        datetime(2024, 2, 5, 8, 0),
                        datetime(2024, 2, 5, 16, 0),
                    )
                ],
            }
        ]


class TestParser3(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = (
            "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/695.html"
        )
        cls.valid = [
            {
                "address": "ул. Сапунгорская",
                "houses": [
                    "2",
                    "3Б/4",
                    "5/1Б",
                    "7А",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "28",
                ],
                "times": [
                    (
                        datetime(2024, 2, 5, 8, 0),
                        datetime(2024, 2, 5, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 6, 8, 0),
                        datetime(2024, 2, 6, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 7, 8, 0),
                        datetime(2024, 2, 7, 17, 0),
                    ),
                ],
            },
            {
                "address": "СТ Полет",
                "houses": ["12"],
                "times": [
                    (
                        datetime(2024, 2, 5, 8, 0),
                        datetime(2024, 2, 5, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 6, 8, 0),
                        datetime(2024, 2, 6, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 7, 8, 0),
                        datetime(2024, 2, 7, 17, 0),
                    ),
                ],
            },
            {
                "address": "СТ Икар",
                "houses": ["434"],
                "times": [
                    (
                        datetime(2024, 2, 5, 8, 0),
                        datetime(2024, 2, 5, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 6, 8, 0),
                        datetime(2024, 2, 6, 17, 0),
                    ),
                    (
                        datetime(2024, 2, 7, 8, 0),
                        datetime(2024, 2, 7, 17, 0),
                    ),
                ],
            },
        ]


class TestParser4(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = (
            "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/680.html"
        )
        cls.valid = [
            {
                "address": "пр. Генерала Острякова",
                "houses": [
                    "155б",
                    "171б",
                    "161",
                    "187",
                    "193",
                    "207",
                    "209",
                    "211",
                    "213",
                ],
                "times": [
                    [
                        datetime(2024, 1, 16, 8, 0),
                        datetime(2024, 1, 16, 16, 0),
                    ]
                ],
            },
            {
                "address": "ул. Щелкунова",
                "houses": ["1"],
                "times": [
                    [
                        datetime(2024, 1, 16, 11, 0),
                        datetime(2024, 1, 16, 16, 0),
                    ]
                ],
            },
            {
                "address": "пр. Гагарина",
                "houses": ["50", "41а", "25", "29"],
                "times": [
                    [
                        datetime(2024, 1, 16, 11, 0),
                        datetime(2024, 1, 16, 16, 0),
                    ]
                ],
            },
        ]
