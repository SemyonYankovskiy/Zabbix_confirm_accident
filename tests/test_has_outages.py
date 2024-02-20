import json
from datetime import datetime, date
from unittest import TestCase

from app.has_outages import has_outages


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
            "2024-02-20 08:00:00",
            "2024-02-20 16:00:00"
            ]
            ]
            }]

        #  Запись в файл
        json_string = json.dumps(list_of_outages, indent=2, ensure_ascii=False, default=str)
        with open(json_file_name, "w", encoding="utf-8") as outfile:
            outfile.write(json_string)
        print(json_string)

        address_from_zabbix = ("Курчатова","1")
        valid = "Плановые работы СЭ: 2024-02-20 08:00-16:00"

        self.assertEqual(valid, has_outages(address_from_zabbix, json_file_name))
