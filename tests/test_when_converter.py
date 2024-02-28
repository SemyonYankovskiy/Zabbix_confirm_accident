from datetime import datetime
from unittest import TestCase

from app.datetime_convert import str_to_datetime_ranges, current_str_to_datetime_ranges


class TestWhenConverter(TestCase):

    def test_when_converter_from_datetime_to_time(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n19.01.2024 08:00 - 16:00\n"),
            [
                (
                    datetime.strptime("08:00:00 19.01.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("16:00:00 19.01.2024", "%H:%M:%S %d.%m.%Y"),
                )
            ],
        )

    def test_when_converter_from_datetime_to_datetime(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n01.11.2023 08:00 - 03.11.2023 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_when_converter_from_date_to_datetime(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n01.11.2023 - 03.11.2023 08:00 - 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n01-03.11.2023 08:00 - 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 02.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 03.11.2023", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

        self.assertListEqual(
            str_to_datetime_ranges("06.07.2023 по 14.07.2023 с 08:30 до 17:30"),
            [
                (
                    datetime.strptime("08:30:00 06.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 06.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 07.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 07.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 08.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 08.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 09.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 09.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 10.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 10.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 11.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 11.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 12.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 12.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 13.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 13.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:30:00 14.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:30:00 14.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_when_converter_thought_night_time_range(self):
        self.assertListEqual(
            str_to_datetime_ranges("с 23:00 03.07.2023г. до 06:00 04.07.2023г."),
            [
                (
                    datetime.strptime("23:00:00 03.07.2023", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("06:00:00 04.07.2023", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_when_converter_above_month(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n31.01.2024 08:00 - 02.02.2024 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 31.01.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 31.01.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 01.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 02.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 02.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_when_converter_above_month_28_days(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n28.02.2024 08:00 - 01.03.2024 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 28.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 28.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 29.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 29.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 01.03.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.03.2024", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_when_converter_above_year(self):
        self.assertListEqual(
            str_to_datetime_ranges("Дата\n\n30.12.2024 08:00 - 01.01.2025 17:00\n"),
            [
                (
                    datetime.strptime("08:00:00 30.12.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 30.12.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 31.12.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 31.12.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 01.01.2025", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 01.01.2025", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def next_test_current_time(self):
        self.assertListEqual(
            current_str_to_datetime_ranges("Отключение электроэнергии с 20 по 23 февраля"),
            [
                (
                    datetime.strptime("08:00:00 20.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 20.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 21.02.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 21.02.2024", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 22.02.2025", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 22.02.2025", "%H:%M:%S %d.%m.%Y"),
                ),
                (
                    datetime.strptime("08:00:00 23.02.2025", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 23.02.2025", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )

    def test_current_time1(self):
        self.assertListEqual(
            current_str_to_datetime_ranges("Отключение электроэнергии 28 января"),
            [
                (
                    datetime.strptime("08:00:00 28.01.2024", "%H:%M:%S %d.%m.%Y"),
                    datetime.strptime("17:00:00 28.01.2024", "%H:%M:%S %d.%m.%Y"),
                ),
            ],
        )
