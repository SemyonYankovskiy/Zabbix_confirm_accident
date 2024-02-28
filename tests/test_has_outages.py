from datetime import date, datetime, timedelta
from typing import ClassVar
from unittest import TestCase

from app.has_outages import has_outages


class TestAddressToVerboseConverter(TestCase):
    outages = None  # type: ClassVar[list]
    dt_format = None  # type: ClassVar[str]
    check_date = None  # type: ClassVar[datetime]

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
        cls.dt_format = "%Y-%m-%d %H:%M:%S"
        cls.check_date = datetime.strptime(f"{date.today()} 10:00:00", cls.dt_format)

    def test_has_outages1(self):
        """Верные данные"""
        address_from_zabbix = ("Вакуленчука", "22")
        valid = "Плановые работы СЭ: с 08:00 до 16:00"
        result = has_outages(address_from_zabbix, self.check_date, self.outages)
        self.assertEqual(valid, result)

    def test_has_outages2(self):
        """Дата не совпадает"""
        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [["2000-02-20 08:00:00", "2000-02-20 16:00:00"]],
            }
        ]

        address_from_zabbix = ("Вакуленчука", "22")
        valid = ""

        result = has_outages(address_from_zabbix, self.check_date, list_of_outages)
        self.assertEqual(valid, result)

    def test_has_outages3(self):
        """Отключение ещё не началось"""
        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [
                    [
                        (self.check_date + timedelta(hours=1)).strftime(self.dt_format),
                        (self.check_date + timedelta(hours=2)).strftime(self.dt_format),
                    ]
                ],
            }
        ]

        address_from_zabbix = ("Вакуленчука", "22")
        valid = ""

        result = has_outages(address_from_zabbix, self.check_date, list_of_outages)
        self.assertEqual(valid, result)

    def test_has_outages4(self):
        """Отключение закончится в следующий день"""
        time_from = datetime.strptime(f"2024-02-28 08:00:00", self.dt_format)
        time_to = datetime.strptime(f"2024-02-29 17:00:00", self.dt_format)
        # За 12 минут до начала работ, но это в пределах обработки.
        check_time = datetime.strptime(f"2024-02-28 11:00:00", self.dt_format)

        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [[time_from.strftime(self.dt_format), time_to.strftime(self.dt_format)]],
            }
        ]

        address_from_zabbix = ("Вакуленчука", "22")
        valid = "Плановые работы СЭ: с 28.02.2024 08:00 до 29.02.2024 17:00"

        result = has_outages(address_from_zabbix, check_time, list_of_outages)
        self.assertEqual(valid, result)

    def test_has_outages5(self):
        """Отключение скоро начнется ~10 мин"""
        time_from = datetime.strptime(f"2024-02-28 10:00:00", self.dt_format)
        time_to = datetime.strptime(f"2024-02-28 12:00:00", self.dt_format)
        # За 12 минут до начала работ, но это в пределах обработки.
        check_time = datetime.strptime(f"2024-02-28 09:48:00", self.dt_format)

        list_of_outages = [
            {
                "address": "Вакуленчука",
                "houses": ["22"],
                "times": [[time_from.strftime(self.dt_format), time_to.strftime(self.dt_format)]],
            }
        ]

        address_from_zabbix = ("Вакуленчука", "22")
        valid = "Плановые работы СЭ: с 10:00 до 12:00"

        result = has_outages(address_from_zabbix, check_time, list_of_outages)
        self.assertEqual(valid, result)

    def test_has_outages6(self):
        """Неверный адрес"""
        address_from_zabbix = ("рмпитанос т саа", "пмаирнеснс")
        valid = ""

        result = has_outages(address_from_zabbix, self.check_date, self.outages)
        self.assertEqual(valid, result)

    def test_has_outages7(self):
        """Пустой адрес"""
        address_from_zabbix = ("", "")
        valid = ""

        result = has_outages(address_from_zabbix, self.check_date, self.outages)
        self.assertEqual(valid, result)

    def test_has_outages8_village(self):
        """Проверка адреса с селом"""
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
        valid = "Плановые работы СЭ: с 08:00 до 16:00"

        result = has_outages(address_from_zabbix, datetime.now(), list_of_outages)
        self.assertEqual(valid, result)
