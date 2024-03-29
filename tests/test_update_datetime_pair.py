from datetime import datetime
from unittest import TestCase

from app.datetime_convert import update_datetime_pair


class TestUpdateDateTimePair(TestCase):

    def test_update_datetime_pair_from_08_16_to_09_16(self):
        """Был диапазон времени 08-16, должен получиться 09-16"""
        times = (
            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )

        new_times = update_datetime_pair(times, "с 09:00 до 16:00")

        self.assertTupleEqual(
            (
                datetime.strptime("2024-02-06 09:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            new_times,
        )

    def test_update_datetime_pair_from_08_16_to_08_11(self):
        """Был диапазон времени 08-16, должен получиться 08-11"""
        times = (
            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )

        new_times = update_datetime_pair(times, "с 08:00 до 11:00")

        self.assertTupleEqual(
            (
                datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2024-02-06 11:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            new_times,
        )

    def test_update_datetime_pair_from_08_16_to_10_12(self):
        """Был диапазон времени 08-16, должен получиться 10-12"""
        times = (
            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )

        new_times = update_datetime_pair(times, "с 10:00 до 12:00")

        self.assertTupleEqual(
            (
                datetime.strptime("2024-02-06 10:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2024-02-06 12:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            new_times,
        )

    def test_update_datetime_pair_from_08_16_to_10_22(self):
        """Был диапазон времени 08-16, должен получиться 10-22"""
        times = (
            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )

        new_times = update_datetime_pair(times, "с 10:00 до 22:00")

        self.assertTupleEqual(
            (
                datetime.strptime("2024-02-06 10:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2024-02-06 22:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            new_times,
        )

    def test_update_datetime_pair_with_new_date(self):
        times = (
            datetime.strptime("2024-02-06 08:00:00", "%Y-%m-%d %H:%M:%S"),
            datetime.strptime("2024-02-06 16:00:00", "%Y-%m-%d %H:%M:%S"),
        )

        new_times = update_datetime_pair(times, "с 10:00 до 22:00")

        self.assertTupleEqual(
            (
                datetime.strptime("2024-02-06 10:00:00", "%Y-%m-%d %H:%M:%S"),
                datetime.strptime("2024-02-06 22:00:00", "%Y-%m-%d %H:%M:%S"),
            ),
            new_times,
        )
