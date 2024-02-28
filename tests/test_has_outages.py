from datetime import date
from typing import ClassVar
from unittest import TestCase

from app.has_outages import has_outages


class TestAddressToVerboseConverter(TestCase):
    outages = None  # type: ClassVar[list]

    @classmethod
    def setUpClass(cls):
        cls.outages = [
            {
                "address": "Курчатова",
                "houses": ["1"],
                "times": [[f"{date.today()} 08:00:00", f"{date.today()} 16:00:00"]],
            },
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [[f"{date.today()} 08:00:00", f"{date.today()} 16:00:00"]],
            },
        ]

    def test_has_outages(self):
        address_from_zabbix = ("Вакуленчука", "22")
        valid = "Плановые работы СЭ: 08:00-16:00"

        result = has_outages(address_from_zabbix, self.outages)
        print(result)
        self.assertEqual(valid, result)

    def test_has_outages2(self):
        """Неверная дата"""
        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [["2024-02-20 08:00:00", "2024-02-20 16:00:00"]],
            }
        ]

        address_from_zabbix = ("Вакуленчука", "22")
        valid = ""

        result = has_outages(address_from_zabbix, list_of_outages)
        self.assertEqual(valid, result)

    def test_has_outages3(self):

        address_from_zabbix = ("рмпитанос т саа", "пмаирнеснс")
        valid = ""

        result = has_outages(address_from_zabbix, self.outages)
        self.assertEqual(valid, result)

    def test_has_outages4(self):

        address_from_zabbix = ("", "")
        valid = ""

        result = has_outages(address_from_zabbix, self.outages)
        self.assertEqual(valid, result)

    def test_has_outages_village(self):
        #  Содержимое файла
        list_of_outages = [
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
                "times": [[f"{date.today()} 08:00:00", f"{date.today()} 16:00:00"]],
            }
        ]

        address_from_zabbix = (r"Терновка(.+?)Ленина", "2")
        valid = "Плановые работы СЭ: 08:00-16:00"

        result = has_outages(address_from_zabbix, list_of_outages)
        self.assertEqual(valid, result)
