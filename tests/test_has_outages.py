import json
from datetime import datetime, date
from unittest import TestCase

from app.has_outages import has_outages, json_opener


class TestAddressToVerboseConverter(TestCase):

    def test_has_outages(self):

        #  Создание файла json
        #  Название файла
        json_file_name = f"data-{date.today()}.json"
        #  Содержимое файла
        list_of_outages =   [            {
            "address": "Курчатова",
            "houses": ["1"],
            "times": [
            [
            "2024-02-21 08:00:00",
            "2024-02-21 16:00:00"
            ]
            ]
            },
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [
                    [
                        "2024-02-21 08:00:00",
                        "2024-02-21 16:00:00"
                    ]
                ]
            }
        ]

        #  Запись в файл
        json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)
        with open(json_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(json_string)


        address_from_zabbix = ("Вакуленчука","22")
        valid = "Плановые работы СЭ: 08:00-16:00"


        json_file_content = json_opener(json_file_name)

        self.assertEqual(valid, has_outages(address_from_zabbix, json_file_content))

    def test_has_outages_village(self):

        #  Создание файла json
        #  Название файла
        json_file_name = f"data-{date.today()}.json"
        #  Содержимое файла
        list_of_outages =   [           {
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
                    [
                        "2024-02-21 08:00:00",
                        "2024-02-21 16:00:00"
                    ]
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
                    [
                        "2024-02-21 08:00:00",
                        "2024-02-21 16:00:00"
                    ]
                ],
            }
        ]

        #  Запись в файл
        json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)
        with open(json_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(json_string)


        address_from_zabbix = (r'Терновка(.+?)Ленина', '2')
        valid = "Плановые работы СЭ: 08:00-16:00"

        self.assertEqual(valid, has_outages(address_from_zabbix, json_file_name))