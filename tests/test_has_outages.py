import json
from datetime import datetime, date
from unittest import TestCase

from app.has_outages import has_outages, json_opener

#  Создание файла json
#  Название файла
json_file_name = f"data-{date.today()}.json"
#  Содержимое файла
list_of_outages = [{
    "address": "Курчатова",
    "houses": ["1"],
    "times": [
        [
            f"{date.today()} 08:00:00",
            f"{date.today()} 16:00:00"
        ]
    ]
},
    {
        "address": "Вакуленчука",
        "houses": ["22"],
        "times": [
            [
                f"{date.today()} 08:00:00",
                f"{date.today()} 16:00:00"
            ]
        ]
    }
]

#  Запись в файл
json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)
with open(json_file_name, "w", encoding="utf-8") as outfile:
    outfile.write(json_string)


class TestAddressToVerboseConverter(TestCase):

    def test_has_outages(self):
        address_from_zabbix = ("Вакуленчука", "22")
        valid = "Плановые работы СЭ: 08:00-16:00"

        json_file_content = json_opener(json_file_name)

        result = has_outages(address_from_zabbix, json_file_content)
        print(result)
        self.assertEqual(valid, result)

    def test_has_outages2(self):
        """
        Неверная дата

        """
        #  Создание файла json
        #  Название файла
        json_file_name = f"data-{date.today()}.json"
        #  Содержимое файла
        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [
                    [
                        "2024-02-20 08:00:00",
                        "2024-02-20 16:00:00"
                    ]
                ]
            }
        ]

        #  Запись в файл
        json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)
        with open(json_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(json_string)

        address_from_zabbix = ("Вакуленчука", "22")
        valid = ""

        json_file_content = json_opener(json_file_name)

        result = has_outages(address_from_zabbix, json_file_content)
        print(result)
        self.assertEqual(valid, result)

    def test_has_outages3(self):

        address_from_zabbix = ("рмпитанос т саа", "пмаирнеснс")
        valid = ""

        json_file_content = json_opener(json_file_name)

        result = has_outages(address_from_zabbix, json_file_content)
        print(result)
        self.assertEqual(valid, result)

    def test_has_outages4(self):

        address_from_zabbix = ("","")
        valid = ""

        json_file_content = json_opener(json_file_name)

        result = has_outages(address_from_zabbix, json_file_content)
        print(result)
        self.assertEqual(valid, result)

    def test_has_outages_village(self):
        #  Создание файла json
        #  Название файла
        json_file_name = f"data-{date.today()}.json"
        #  Содержимое файла
        list_of_outages = [{
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
                    f"{date.today()} 08:00:00",
                    f"{date.today()} 16:00:00"
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

        json_file_content = json_opener(json_file_name)
        result = has_outages(address_from_zabbix, json_file_content)
        print(result)
        self.assertEqual(valid, result)
