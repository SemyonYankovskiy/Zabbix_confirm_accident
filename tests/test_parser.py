from datetime import datetime
from typing import ClassVar
from unittest import TestCase

from app.address_convert import address_cleaner, house_splitter
from app.datetime_convert import str_to_datetime_ranges, current_str_to_datetime_ranges
from app.parser import content_parser, get_planned_outage_data, get_current_outage_data


class TestParser(TestCase):
    url = None  # type: ClassVar[str]
    valid = None  # type: ClassVar[list]

    def test_parser(self):
        self.maxDiff = None
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
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/697.html")
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
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/696.html")
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
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/695.html")
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
                "address": "СНТ Ялтинское кольцо",
                "houses": [],
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
                "address": "СТ Рубин",
                "houses": [],
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
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/680.html")
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
                    (
                        datetime(2024, 1, 16, 8, 0),
                        datetime(2024, 1, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "ул. Щелкунова",
                "houses": ["1"],
                "times": [
                    (
                        datetime(2024, 1, 16, 11, 0),
                        datetime(2024, 1, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "пр. Гагарина",
                "houses": ["50", "41а", "25", "29"],
                "times": [
                    (
                        datetime(2024, 1, 16, 11, 0),
                        datetime(2024, 1, 16, 16, 0),
                    )
                ],
            },
        ]


class TestParser5(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/689.html")
        cls.valid = [
            {
                "address": "пос. Октябрь, ул. 19-го Партсъезда",
                "houses": [
                    "2",
                    "34",
                    "36",
                    "38",
                    "40",
                    "42",
                    "44",
                    "46",
                    "48",
                    "50",
                    "52",
                    "54",
                    "56",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "39",
                    "41",
                    "43",
                    "45",
                    "47",
                    "49",
                    "51",
                    "53",
                ],
                "times": [
                    (
                        datetime(2024, 1, 29, 8, 0),
                        datetime(2024, 1, 29, 16, 0),
                    )
                ],
            },
            {
                "address": "пос. Октябрь, ул. Парижской коммуны",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "40",
                    "42",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                ],
                "times": [
                    (
                        datetime(2024, 1, 29, 8, 0),
                        datetime(2024, 1, 29, 16, 0),
                    )
                ],
            },
            {
                "address": "пос. Октябрь, ул. Совхозная",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "1а",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                ],
                "times": [
                    (
                        datetime(2024, 1, 29, 8, 0),
                        datetime(2024, 1, 29, 16, 0),
                    )
                ],
            },
            {
                "address": "пос. Октябрь, ул. Узловая",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "40",
                    "42",
                    "44",
                    "46",
                    "48",
                    "50",
                    "52",
                    "54",
                    "56",
                    "58",
                    "60",
                    "62",
                    "64",
                    "66",
                    "68",
                    "70",
                    "72",
                    "74",
                    "76",
                    "78",
                    "80",
                    "82",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "35",
                    "37",
                    "39",
                    "41",
                    "43",
                    "45",
                    "47",
                    "49",
                    "51",
                    "53",
                    "55",
                    "57",
                    "59",
                    "61",
                    "63",
                    "65",
                    "67",
                    "69",
                    "71",
                ],
                "times": [
                    (
                        datetime(2024, 1, 29, 8, 0),
                        datetime(2024, 1, 29, 16, 0),
                    )
                ],
            },
            {
                "address": "пос. Октябрь, ул. Чернореченская",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "42",
                    "54",
                    "56",
                    "58",
                    "60",
                    "62",
                    "64",
                    "1а",
                    "1",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                ],
                "times": [
                    (
                        datetime(2024, 1, 29, 8, 0),
                        datetime(2024, 1, 29, 16, 0),
                    )
                ],
            },
        ]


class TestParser6(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/659.html")
        cls.valid = [
            {
                "address": "с. Орлиное, ул. Тюкова",
                "houses": ["87А/1"],
                "times": [
                    (
                        datetime(2023, 12, 15, 8, 0),
                        datetime(2023, 12, 15, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Орлиное, КСП Красный Октябрь",
                "houses": ["65", "уч524", "уч518"],
                "times": [
                    (
                        datetime(2023, 12, 15, 8, 0),
                        datetime(2023, 12, 15, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Орлиное, пер. Западный",
                "houses": ["638"],
                "times": [
                    (
                        datetime(2023, 12, 15, 8, 0),
                        datetime(2023, 12, 15, 16, 0),
                    )
                ],
            },
            {
                "address": "пос. Кача - ул. Ударная",
                "houses": ["58"],
                "times": [
                    (
                        datetime(2023, 12, 15, 8, 0),
                        datetime(2023, 12, 15, 16, 0),
                    )
                ],
            },
        ]


class TestParser7(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = ("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/706.html")
        cls.valid = [
            {
                "address": "Федюхины высоты (ООО Севастопольский военно-исторический клуб)",
                "houses": [],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Гагарина",
                "houses": ["2", "4", "6", "1", "3", "5", "7"],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Комсомольская",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "23",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Советская",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Горная",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "12",
                    "16",
                    "18",
                    "14",
                    "24",
                    "26",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "40",
                    "40а",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "41",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Молодежная",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "37",
                    "39",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Садовая",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "40",
                    "42",
                    "44",
                    "46",
                    "48",
                    "50",
                    "52",
                    "54",
                    "56",
                    "58",
                    "60",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "71а",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "39",
                    "41",
                    "43",
                    "45",
                    "47",
                    "49",
                    "51",
                    "53",
                    "55",
                    "57",
                    "59",
                    "61",
                    "63",
                    "65",
                    "67",
                    "69",
                    "71",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Королева",
                "houses": ["10", "1", "3", "5", "7", "9", "11"],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Чакыл-Мале",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "16",
                    "17",
                    "21",
                    "23",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Зелёная",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, пер. Конторский",
                "houses": ["2", "4", "3а", "1", "3", "5"],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Ленина",
                "houses": [
                    "2",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "142",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Балаклавская",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "1б",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Куйбышевская",
                "houses": ["1б"],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. Родниковая",
                "houses": ["6", "8", "12", "14", "11а", "1", "3", "5", "7", "9", "11"],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
            {
                "address": "с. Терновка, ул. КСП Память Ленина",
                "houses": [
                    "44",
                    "57",
                    "186",
                    "190",
                    "332",
                    "365",
                    "366",
                    "368",
                    "369",
                    "370",
                    "371",
                    "388",
                    "389",
                    "645",
                ],
                "times": [
                    (
                        datetime(2024, 2, 16, 11, 0),
                        datetime(2024, 2, 16, 16, 0),
                    )
                ],
            },
        ]


class TestCurrentParser(TestCase):
    def test_parser2(self):
        self.maxDiff = None
        res = []
        class_name = self.__class__.__name__

        time_range, content = get_current_outage_data(self.url)
        base_time_ranges = current_str_to_datetime_ranges(time_range)
        print(base_time_ranges)
        print(content)
        print("======================")
        parsed_content = content_parser(content, base_time_ranges)
        for item in parsed_content:
            print(item)
        print("======================")

        for address, houses, time_ranges in parsed_content:

            correct_address = address_cleaner(address)
            houses_list = house_splitter(houses)
            if len(correct_address) > 64:
                continue
            outages_json = {
                "address": correct_address,
                "houses": houses_list,
                "times": time_ranges,
            }
            res.append(outages_json)

        for item in res:
            print(item)

        self.assertEqual(self.valid, res)

    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/incident/otklyuchenie-elektroenergii-29-fevralya.html"
        cls.valid = [
            {
                "address": "ул. Героев Севастополя,",
                "houses": ["37"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Папанина,",
                "houses": ["7", "9", "11", "13"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Селенгинская,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Генерала Родионова,",
                "houses": ["10", "12", "14", "16", "18", "20", "22", "24"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Ромашковая,",
                "houses": [
                    "82А",
                    "80А",
                    "56",
                    "58",
                    "60",
                    "66",
                    "72",
                    "74",
                    "76",
                    "80",
                    "82",
                    "41",
                    "43",
                    "49",
                    "55",
                    "776",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Муромская,",
                "houses": ["182А", "188А"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ПКИЗ Подводник,",
                "houses": ["172/59", "271/158"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Горпищенко,",
                "houses": ["109/33", "109/34"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Маслиновая,",
                "houses": ["44а", "57", "171/58"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "пер. Крепостной,",
                "houses": ["7"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Партизанская,",
                "houses": ["16"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Частника,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "21А",
                    "1",
                    "3",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "пер. 1 Морской,",
                "houses": ["4", "6", "8", "3", "5"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "пер. 2 Морской,",
                "houses": ["5", "7"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "пер. 4 Морской,",
                "houses": ["3А", "1А", "1", "3"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Буряка,",
                "houses": ["4", "6", "8", "10", "12", "1"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Гвардейская,",
                "houses": ["4", "6", "5А", "1", "3", "5"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Димитрова,",
                "houses": ["3", "2", "4"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Рыбацкая,",
                "houses": ["10", "1"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "Старосеверная балка,",
                "houses": ["2", "4", "6"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "спуск Степана Разина,",
                "houses": ["4", "6", "8", "3"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Сторожевая,",
                "houses": ["2", "4", "10"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Якорная,",
                "houses": ["2", "4", "6", "12"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "пл. Захарова,",
                "houses": ["1Б"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Бирюзовая,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "1",
                    "3",
                    "5",
                    "7",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Изумрудная,",
                "houses": [
                    "2А",
                    "2б",
                    "2в",
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "10",
                    "13Б",
                    "13А",
                    "9Б",
                    "9А",
                    "7А",
                    "1",
                    "5",
                    "7",
                    "9",
                    "11",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Маковая,",
                "houses": ["4", "6"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Морпортовская,",
                "houses": [
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Полынная,",
                "houses": ["3А", "3"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Штурвальная,",
                "houses": ["4", "6", "8", "10", "12", "7", "9", "11", "13"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "Б. Античный,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "14А",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Адмирала Грейга,",
                "houses": [
                    "6",
                    "8",
                    "3",
                    "14",
                    "19А",
                    "17Б",
                    "17Б/1",
                    "19",
                    "23",
                    "10",
                    "5/4",
                    "9/8",
                    "5",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "СНТ Волга,",
                "houses": ["28", "уч50", "уч51", "уч95", "уч99"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Авиационная,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "9",
                    "11",
                    "13",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Ольховая,",
                "houses": ["4", "6"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Арцеулова,",
                "houses": ["14"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "СТ Ромашка,",
                "houses": ["32"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Готская,",
                "houses": [
                    "126Б",
                    "118А",
                    "120А",
                    "122А",
                    "124А",
                    "110",
                    "112",
                    "114",
                    "116",
                    "118",
                    "126",
                    "128",
                    "26А/15",
                    "26А/7",
                    "26А/1",
                    "26А/2",
                    "26А/4",
                    "26А/5",
                    "26А/8",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Фиолентовское шоссе,",
                "houses": [
                    "11",
                    "28",
                    "11А",
                    "18Б",
                    "18",
                    "28/1",
                    "42А/1",
                    "42А",
                    "18А",
                    "48А",
                    "42",
                    "9В/2",
                    "11Б",
                    "7",
                    "9Г/1",
                    "9А",
                ],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "Пятницкий проезд,",
                "houses": ["57"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
            {
                "address": "ул. Адмирала Фадеева,",
                "houses": ["1"],
                "times": [
                    (
                        datetime(2024, 2, 29, 9, 0),
                        datetime(2024, 2, 29, 11, 0),
                    )
                ],
            },
        ]

#
class CurrentParser2(TestCurrentParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/incident/otklyuchenie-elektroenergii-1-marta-2.html"
        cls.valid = [
            {
                "address": "пер. Перекомский,",
                "houses": ["23"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Подольцева,",
                "houses": [
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "39",
                    "41",
                    "43",
                    "45",
                    "47",
                    "49",
                    "51",
                    "53",
                    "55",
                    "57",
                    "59",
                    "61",
                    "63",
                    "65",
                    "67",
                    "69",
                    "71",
                    "73",
                    "75",
                    "77",
                    "79",
                    "81",
                    "83",
                    "85",
                    "87",
                    "89",
                    "91",
                    "93",
                    "95",
                    "97",
                    "99",
                    "101",
                    "103",
                    "105",
                    "107",
                    "109",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Ревякина,",
                "houses": [
                    "22А",
                    "24",
                    "5А",
                    "7Б",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "30А",
                    "26",
                    "17А",
                    "9А",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Грибоедова,",
                "houses": ["8", "7"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "туп. Каманина,",
                "houses": ["2", "4", "6", "8", "10", "12"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Кудюрова,",
                "houses": [
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Надежды Краевой,",
                "houses": [
                    "36/9",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "18",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "7",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Седова,",
                "houses": [
                    "22/5",
                    "28",
                    "30",
                    "32",
                    "34",
                    "36",
                    "38",
                    "40",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "19",
                    "21",
                    "23",
                    "25",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "39",
                    "41",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Каменистая,",
                "houses": ["1", "3", "5", "7", "9", "11", "13", "15", "17"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Карла Либкнехта,",
                "houses": ["84", "79А/14", "79Б", "79"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Жерве,",
                "houses": [
                    "2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "пер. Жерве,",
                "houses": ["2А", "2", "4", "6", "8", "10", "12", "14", "16", "3"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Гармаша,",
                "houses": ["141"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Силантьева,",
                "houses": ["21А", "21Б", "1", "3", "5", "17", "21"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Скалистая,",
                "houses": ["9А", "1", "3", "5", "7", "9"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "пер. Юферов,",
                "houses": ["16"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "пр- Каменистый,",
                "houses": ["10"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "СТ Сапун-гора,",
                "houses": ["622", "646", "615", "627", "651", "1469"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Григория Ивашкевича,",
                "houses": ["12", "30", "29А", "19", "29", "31"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Валентины Ходыревой,",
                "houses": ["15"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Тамары Смоленской,",
                "houses": ["1", "15"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Генерала Мельника,",
                "houses": [
                    "104А",
                    "108А",
                    "102А/2",
                    "6",
                    "104",
                    "106",
                    "341",
                    "кад325",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "пер. Генерала Мельника,",
                "houses": [
                    "110А",
                    "108А",
                    "кад326",
                    "10/2",
                    "4",
                    "6",
                    "8",
                    "10",
                    "12",
                    "1А",
                    "7А",
                    "кад341",
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "397",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Костомаровская,",
                "houses": ["22", "20", "22"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Щорса,",
                "houses": ["3", "5", "7", "9", "11", "13", "15", "17"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Частника,",
                "houses": [
                    "102",
                    "104",
                    "106",
                    "108",
                    "110",
                    "112",
                    "114",
                    "116",
                    "118",
                    "120",
                    "122",
                    "87",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Генерала Ракова,",
                "houses": [
                    "12",
                    "14",
                    "20",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "19",
                    "21",
                    "23",
                    "27",
                    "29",
                    "31",
                    "33",
                    "35",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Полетная,",
                "houses": ["18А", "4", "8", "10", "12", "16", "18"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Планерная,",
                "houses": [
                    "16А",
                    "16Б",
                    "12А",
                    "18Б",
                    "10А",
                    "10",
                    "12",
                    "1Б",
                    "1А",
                    "11",
                    "13",
                    "15",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Кедрина,",
                "houses": ["2Ж", "2А", "2Д", "2Г", "1", "3", "5", "11"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Парашютная,кад-600,",
                "houses": ["39", "41", "885"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Колодезная,",
                "houses": ["54"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "СНТ Фрегат,",
                "houses": [
                    "112А",
                    "4",
                    "6",
                    "8",
                    "12",
                    "22",
                    "34",
                    "46",
                    "54",
                    "72",
                    "74",
                    "87А",
                    "9",
                    "11",
                    "15",
                    "17",
                    "19",
                    "23",
                    "29",
                    "31",
                    "43",
                    "47",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "г. Инкерман, ул. Малиновского,",
                "houses": ["16", "3", "5", "7", "9", "11", "13", "4", "32"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "г. Инкерман, ул. Мудрика,",
                "houses": ["5", "7", "9", "11"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "г. Инкерман, ул. Шевкопляса,",
                "houses": ["4", "6", "8", "1", "5", "7", "7В"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "г. Инкерман, ул. Менжинского,",
                "houses": ["2"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Маршала Блюхера,",
                "houses": ["20А"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Героев Сталинграда,",
                "houses": ["26", "28", "28А", "24А", "32"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Бориса Михайлова,",
                "houses": ["2", "2/2"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Павла Корчагина,",
                "houses": ["8"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Казачья,",
                "houses": [
                    "6А",
                    "51/18Б",
                    "3906",
                    "51/13",
                    "51/17",
                    "51/12",
                    "51/3А",
                    "51/22",
                ],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Гоголя,",
                "houses": ["26А", "24", "26"],
                "times": [
                    (
                        datetime(2024, 3, 1, 9, 0),
                        datetime(2024, 3, 1, 17, 0),
                    )
                ],
            },
        ]


class CurrentParser3(TestCurrentParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/incident/otklyuchenie-elektroenergii-4-i-5-marta.html"
        cls.valid = []


class CurrentParser4(TestCurrentParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/incident/otklyuchenie-elektroenergii-2-i-3-marta.html"
        cls.valid = []


class CurrentParser5(TestCurrentParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/incident/otklyuchenie-elektroenergii-4-marta-4.html"
        cls.valid = []