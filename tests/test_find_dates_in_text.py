from datetime import datetime, date
from unittest import TestCase

from app.datetime_convert import find_dates_in_text


class TestFindDatesInText(TestCase):

    def test_find_dates_in_text1(self):
        """17 и 18 февраля"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 2, 17), date(current_year, 2, 18)],
            find_dates_in_text("Отключение электроэнергии 17 и 18 февраля"),
        )

    def test_find_dates_in_text2(self):
        """18 февраля"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 2, 18)],
            find_dates_in_text("18 февраля"),
        )

    def test_find_dates_in_text3(self):
        """12, 13, 14 февраля"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 2, 12), date(current_year, 2, 13), date(current_year, 2, 14)],
            find_dates_in_text("Отключение электроэнергии 12, 13, 14 февраля (обновлено 13.02 в 14.40)"),
        )

    def test_find_dates_in_text4(self):
        """8 февраля (обновлено 07 февраля)"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 2, 8)],
            find_dates_in_text("Отключение электроэнергии 8 февраля (обновлено 07 февраля в 16.20)"),
        )

    def test_find_dates_in_text5(self):
        """с 12 по 14 февраля"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 2, 12), date(current_year, 2, 13), date(current_year, 2, 14)],
            find_dates_in_text("Отключение электроэнергии с 12 по 14 февраля"),
        )

    def test_find_dates_in_text6(self):
        """25.01.2024г"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 1, 25)],
            find_dates_in_text(
                "В сети 6000 В 25.01.2024г. с 08:00 до 17:00 будет прекращена подача электроэнергии"
            ),
        )

    def test_find_dates_in_text7(self):
        """В 04.03.2024г и 05.03.2024г"""
        current_year = datetime.now().year
        self.assertListEqual(
            [date(current_year, 3, 4), date(current_year, 3, 5)],
            find_dates_in_text("В 04.03.2024г. и 05.03.2024г. ежедневно с 09:00 до 16:00 "),
        )
