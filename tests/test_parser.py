from datetime import datetime
from typing import ClassVar
from unittest import TestCase

from app.address_convert import address_cleaner, house_splitter
from app.datetime_convert import str_to_datetime_ranges
from app.parser import content_parser, get_planned_outage_data


class TestParser(TestCase):
    url = None  # type: ClassVar[str]
    valid = None  # type: ClassVar[list]

    def test_parser(self):
        self.maxDiff = None
        res = []
        class_name = self.__class__.__name__

        time_range, content = get_planned_outage_data(self.url)
        # print(f"{class_name} time_range: {time_range} content: {content}")
        base_time_ranges = str_to_datetime_ranges(time_range)
        # print(f"{class_name} base_time_ranges: {base_time_ranges}")

        parsed_content = content_parser(content, base_time_ranges)
        # print(f"{class_name} parsed_content: {parsed_content}")

        for address, houses, time_ranges in parsed_content:
            correct_address = address_cleaner(address)
            houses_list = house_splitter(houses)
            outages_json = {
                "address": correct_address,
                "houses": houses_list,
                "times": time_ranges,
            }
            res.append(outages_json)

        # print(f"{class_name} {res}")

        self.assertEqual(self.valid, res)

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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/696.html"
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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/695.html"
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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/680.html"
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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/689.html"
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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/659.html"
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
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/706.html"
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


class TestParser8(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/724.html"
        cls.valid = [
            {
                "address": "Доковая балка – СНТ Садоводческий",
                "houses": [],
                "times": [
                    (
                        datetime(2024, 3, 14, 8, 0),
                        datetime(2024, 3, 14, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Хрусталева",
                "houses": ["179", "181", "183"],
                "times": [
                    (
                        datetime(2024, 3, 14, 8, 0),
                        datetime(2024, 3, 14, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Степаняна",
                "houses": ["2А", "4/1", "4/2", "4/3", "кад275", "4309"],
                "times": [
                    (
                        datetime(2024, 3, 14, 8, 0),
                        datetime(2024, 3, 14, 17, 0),
                    )
                ],
            },
        ]


class TestParser9(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = (
            "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/725.html"
        )
        cls.valid = [
            {
                "address": "ул. Песочная",
                "houses": ["33"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Земляничная",
                "houses": ["14", "14А", "16", "18", "20", "24А", "26", "28", "30"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Аланская",
                "houses": ["25", "33", "35", "37", "39", "45", "47", "51"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Легионная",
                "houses": [
                    "3",
                    "7",
                    "8",
                    "12",
                    "13",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                ],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Генерала Витмера",
                "houses": ["17", "25"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Строительная – ГК Сокол",
                "houses": [],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "ул. Вакуленчука",
                "houses": ["41/1", "41/3"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
            {
                "address": "Фиолентовское шоссе",
                "houses": ["1В"],
                "times": [
                    (
                        datetime(2024, 3, 15, 8, 0),
                        datetime(2024, 3, 15, 17, 0),
                    )
                ],
            },
        ]


class TestParser10(TestParser):
    @classmethod
    def setUpClass(cls):
        cls.url = "https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/729.html"
        cls.valid = [
            {
                "address": "КСП Память Ленина",
                "houses": [
                    "1",
                    "62",
                    "74",
                    "75",
                    "149",
                    "150",
                    "180",
                    "183",
                    "185",
                    "405",
                    "468",
                    "469",
                    "470",
                    "474",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Шафрановая",
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
                    "24",
                    "26",
                    "16а",
                    "16б",
                    "16г",
                    "24а",
                    "26б",
                    "26г",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Камышовое шоссе",
                "houses": ["16в/3", "16в/1", "16в/6", "16в/4", "16в/5", "16/6а", "16В/11А", "16", "20"],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "СНТ Восход",
                "houses": [],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, СНТ Эдельвейс",
                "houses": [],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, СТ Медик-7",
                "houses": ["1", "7", "18", "20", "24", "28", "кад637"],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, ул. Ирисовая",
                "houses": [
                    "2а",
                    "4а",
                    "10а",
                    "14а",
                    "2",
                    "4",
                    "6",
                    "10",
                    "12",
                    "18",
                    "20",
                    "22",
                    "24",
                    "26",
                    "28",
                    "15в",
                    "15г",
                    "21а",
                    "21б",
                    "1",
                    "3",
                    "7",
                    "9",
                    "11",
                    "13",
                    "21",
                    "23",
                    "23б",
                    "24/2",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, ул. Сапфирная",
                "houses": [
                    "1",
                    "3",
                    "5",
                    "7",
                    "9",
                    "11",
                    "13",
                    "15",
                    "17",
                    "8",
                    "10",
                    "12",
                    "2а",
                    "2б",
                    "2в",
                    "2б/1",
                    "2г",
                    "9а",
                    "11а",
                    "21",
                    "22",
                    "25",
                    "26",
                    "26/1",
                    "30б",
                    "30",
                    "31",
                    "32",
                    "33",
                    "36",
                    "43",
                    "43а",
                    "43б",
                    "45",
                    "45а",
                    "45б",
                    "51",
                    "53",
                    "53а",
                    "55",
                    "61",
                    "63",
                    "65/61",
                    "кад707",
                    "806",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, ул. Амет-Хана Султана",
                "houses": [
                    "2",
                    "3",
                    "4",
                    "8",
                    "9",
                    "11",
                    "13",
                    "15",
                    "21",
                    "12",
                    "14",
                    "16",
                    "18",
                    "20",
                    "22",
                    "26",
                    "28",
                    "34",
                    "38",
                    "23",
                    "25",
                    "27",
                    "35",
                    "37",
                    "39",
                    "37/1",
                    "37/2",
                    "37/4",
                    "37/5",
                    "37/6",
                    "37/7",
                    "37/8",
                    "37/9",
                    "37/10",
                    "39а",
                    "48",
                    "48А",
                    "54",
                    "54А",
                    "58",
                    "60",
                    "62",
                    "64",
                    "66",
                    "68",
                    "70",
                    "кад697",
                    "1063",
                    "1067",
                    "1199",
                    "1253",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "х. Отрадный, ул. Согласия",
                "houses": [
                    "1",
                    "1в",
                    "1в/2",
                    "1б",
                    "5",
                    "7",
                    "9",
                    "11",
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
                    "34",
                    "38",
                    "40",
                    "44",
                    "46",
                    "48",
                    "50",
                    "52",
                    "54",
                    "19",
                    "21",
                    "23",
                    "25",
                    "29",
                    "31",
                    "33",
                    "35",
                    "37",
                    "58",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Кольцевая",
                "houses": [
                    "12а",
                    "14А",
                    "4",
                    "14",
                    "20",
                    "1в",
                    "23а",
                    "1",
                    "5",
                    "7",
                    "10",
                    "13",
                    "21",
                    "27",
                    "29",
                    "31",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Яхонтовая",
                "houses": [
                    "1",
                    "2",
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
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Агатовая",
                "houses": [
                    "1",
                    "3",
                    "4",
                    "8",
                    "10",
                    "12",
                    "16",
                    "18",
                    "20",
                    "24",
                    "26",
                    "28",
                    "32",
                    "33",
                    "55",
                    "69",
                    "71",
                    "кад681",
                ],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
            {
                "address": "ул. Эдельвейсовая",
                "houses": ["37"],
                "times": [(datetime(2024, 3, 21, 8, 0), datetime(2024, 3, 21, 16, 0))],
            },
        ]
