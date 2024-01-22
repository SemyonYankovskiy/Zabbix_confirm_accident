from datetime import datetime
from unittest import TestCase

from app.when_convert import str_to_datetime


class TestWhenConverter(TestCase):

    def test_when_converter_from_datetime_to_time(self):
        self.assertListEqual(
            str_to_datetime("Дата\n\n19.01.2024 08:00 - 16:00\n"),
            [
                datetime(2024, 1, 19, 8, 0, 0, 0),
                datetime(2024, 1, 19, 16, 0, 0, 0),
            ]
        )

    def test_when_converter_from_datetime_to_datetime(self):
        self.assertListEqual(
            str_to_datetime("Дата\n\n01.11.2023 08:00 - 03.11.2023 17:00\n"),
            [
                datetime(2023, 11, 1, 8, 0, 0, 0),
                datetime(2023, 11, 1, 17, 0, 0, 0),
                datetime(2023, 11, 2, 8, 0, 0, 0),
                datetime(2023, 11, 2, 17, 0, 0, 0),
                datetime(2023, 11, 3, 8, 0, 0, 0),
                datetime(2023, 11, 3, 17, 0, 0, 0),
            ]
        )

    def test_when_converter_from_date_to_datetime(self):
        self.assertListEqual(
            str_to_datetime("Дата\n\n01.11.2023 - 03.11.2023 08:00 - 17:00\n"),
            [
                datetime(2023, 11, 1, 8, 0, 0, 0),
                datetime(2023, 11, 1, 17, 0, 0, 0),
                datetime(2023, 11, 2, 8, 0, 0, 0),
                datetime(2023, 11, 2, 17, 0, 0, 0),
                datetime(2023, 11, 3, 8, 0, 0, 0),
                datetime(2023, 11, 3, 17, 0, 0, 0),
            ]
        )

        self.assertListEqual(
            str_to_datetime("06.07.2023 по 14.07.2023 с 08:30 до 17:30"),
            [
                datetime(2023, 7, 6, 8, 30, 0, 0),
                datetime(2023, 7, 6, 17, 30, 0, 0),

                datetime(2023, 7, 7, 8, 30, 0, 0),
                datetime(2023, 7, 7, 17, 30, 0, 0),

                datetime(2023, 7, 8, 8, 30, 0, 0),
                datetime(2023, 7, 8, 17, 30, 0, 0),

                datetime(2023, 7, 9, 8, 30, 0, 0),
                datetime(2023, 7, 9, 17, 30, 0, 0),

                datetime(2023, 7, 10, 8, 30, 0, 0),
                datetime(2023, 7, 10, 17, 30, 0, 0),

                datetime(2023, 7, 11, 8, 30, 0, 0),
                datetime(2023, 7, 11, 17, 30, 0, 0),

                datetime(2023, 7, 12, 8, 30, 0, 0),
                datetime(2023, 7, 12, 17, 30, 0, 0),

                datetime(2023, 7, 13, 8, 30, 0, 0),
                datetime(2023, 7, 13, 17, 30, 0, 0),

                datetime(2023, 7, 14, 8, 30, 0, 0),
                datetime(2023, 7, 14, 17, 30, 0, 0),
            ]
        )

    def test_when_converter_thought_night_time_range(self):
        self.assertListEqual(
            str_to_datetime("с 23:00 03.07.2023г. до 06:00 04.07.2023г."),
            [
                datetime(2023, 7, 3, 23, 0, 0, 0),
                datetime(2023, 7, 4, 6, 0, 0, 0),
            ]
        )
