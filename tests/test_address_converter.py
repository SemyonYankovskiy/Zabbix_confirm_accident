from unittest import TestCase

from app.address_convert import (
    house_splitter,
    address_cleaner,
    divide_by_address_and_house_numbers,
)


class TestAddressDivider(TestCase):

    def test_divider1(self):
        self.assertEqual(
            ("ул. Севастопольская зона ЮБК", "5, 19, 19а"),
            divide_by_address_and_house_numbers(
                "ул. Севастопольская зона ЮБК 5, 19, 19а"
            ),
        )

    def test_divider2(self):
        self.assertEqual(
            ("пос. Ласпи", "53/134"),
            divide_by_address_and_house_numbers("пос. Ласпи53/134;"),
        )

    def test_divider3(self):
        self.assertEqual(
            ("ул. 19-го Партсъезда", "2, 34-56 (чет), 13-53 (нечет)"),
            divide_by_address_and_house_numbers(
                "ул. 19-го Партсъезда 2, 34-56 (чет), 13-53 (нечет);"
            ),
        )

    def test_divider4(self):
        self.assertEqual(
            ("пор", "24, 25, 36, 33"),
            divide_by_address_and_house_numbers("пор 24, 25, 36, 33"),
        )

    def test_divider5(self):
        self.assertEqual(
            ("площадь 50-летия СССР", "5/3"),
            divide_by_address_and_house_numbers("площадь 50-летия СССР 5/3"),
        )

    def test_divider6(self):
        self.assertEqual(
            ("пл.50 летия СССР", "5/3, 1, 2, 3, 4"),
            divide_by_address_and_house_numbers("пл.50 летия СССР 5/3, 1, 2, 3, 4"),
        )

    def test_divider7(self):
        self.assertEqual(
            ("1 Мая площадь", "1, 2"),
            divide_by_address_and_house_numbers("1 Мая площадь 1, 2"),
        )

    def test_divider8(self):
        self.assertEqual(
            ("1-я Бастионная улица", "10-12"),
            divide_by_address_and_house_numbers("1-я Бастионная улица 10-12"),
        )

    def test_divider_no_numbers1(self):
        self.assertEqual(
            ("ТСН ЖСТИЗ «Колобовский»", ""),
            divide_by_address_and_house_numbers("ТСН ЖСТИЗ «Колобовский»;"),
        )

    def test_divider_no_numbers2(self):
        self.assertEqual(
            ("ТСН СНТ «Горняк-2»", ""),
            divide_by_address_and_house_numbers("ТСН СНТ «Горняк-2»;"),
        )


class TestAddressCleaner(TestCase):
    def test_address(self):
        self.assertEqual("СТ Полет", address_cleaner("СТ «Полет» уч."))

    def test_address1(self):
        self.assertEqual("ул. Льва Толстого", address_cleaner("ул. Льва Толстого"))

    def test_address2(self):
        self.assertEqual("туп. Обрывистый", address_cleaner("туп. Обрывистый"))

    def test_address3(self):
        self.assertEqual("с/з Софьи Перовской", address_cleaner("с/з Софьи Перовской"))

    def test_address4(self):
        self.assertEqual("СТ Черноморец-2", address_cleaner("«СТ-Черноморец-2»"))

    def test_address5(self):
        self.assertEqual("СТ Незабудка", address_cleaner("«СТ-Незабудка»"))

    def test_address6(self):
        self.assertEqual("СТ Икар", address_cleaner("СТ «Икар» кад."))

    def test_address7(self):
        self.assertEqual("СНТ Статистик-2", address_cleaner("«СНТ-Статистик-2»"))

    def test_address8(self):
        self.assertEqual("СНТ Горняк-2", address_cleaner("ТСН СНТ «Горняк-2»"))


class TestHouseSplitter(TestCase):

    def test_houses1(self):
        self.assertListEqual(
            house_splitter("2-12,16-24,17-А,9-А,1-19,122."),
            [
                "2",
                "4",
                "6",
                "8",
                "10",
                "12",
                "16",
                "18",
                "20",
                "22",
                "24",
                "17А",
                "9А",
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
                "122",
            ],
        )

    def test_houses2(self):
        self.assertListEqual(
            house_splitter("16,24, 29-В,29-Б,29-А,17-33"),
            [
                "16",
                "24",
                "29В",
                "29Б",
                "29А",
                "17",
                "19",
                "21",
                "23",
                "25",
                "27",
                "29",
                "31",
                "33",
            ],
        )

    def test_houses3(self):
        self.assertListEqual(
            house_splitter("2-60,19б/1,9-а,135-Г,19б/2,1-19,131"),
            [
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
                "19б/1",
                "9а",
                "135Г",
                "19б/2",
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
                "131",
            ],
        )

    def test_houses4(self):
        self.assertListEqual(house_splitter("50,218"), ["50", "218"])

    def test_houses_empty(self):
        self.assertListEqual(house_splitter(""), [])

    def test_houses5(self):
        self.assertListEqual(
            house_splitter("3-Б, 111, 22, 1 Б, 3-Б/4, 5/1-Б, 7-А"),
            ["3Б", "111", "22", "1Б", "3Б/4", "5/1Б", "7А"],
        )

    def test_houses6(self):
        self.assertListEqual(
            house_splitter("55,84, (лишнее)"),
            ["55", "84"],
        )

    def test_houses7(self):
        self.assertListEqual(
            house_splitter("2-16(чет),1-б,1-17 (нечет)"),
            [
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
        )
