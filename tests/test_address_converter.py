from unittest import TestCase

from app.address_convert import house_splitter, address_converter


FULL_ADDRESS_DATA = """
    Отключение электроэнергии 10 октября

    В связи с производством неотложных работ в сетях, связанных с улучшением качества электроснабжения, 10.10.2023г. будет прекращена подача электроэнергии по следующим адресам:

    с 09:00 до 13:00

    с. Верхнесадовое

    ул. Одинцова2-12,16-24,17-А,9-А,1-19;

    ул. Паршина16,24, 29-В,29-Б,29-А,17-33;

    пер. Подгорный1-21;

    ул. Севастопольская 2-36,35-Б,1-35,40-52;

    ул. Фильченкова 3-27;

    ул. Пирогова 2-22,1-9;

    ул. Титова 2;

    пер. Мирный 2-10



    с 12:00 до 16:00

    ул. Богданова 1,2-8,1-А, 9-А,9-Б,7-А,7-Б,3,7;

    ул. Дорофея Кошубы 7-21;

    ул. Циолковского 1-А,1,3-5;

    ул. Челюскинцев 65,86-А,58-А,38-94;

    Екатерининская миля ;



    с 09:00 до 17:00

    ул. Романтиков 1-15,2-22;

    ул. Липранди 2-4,5-7,11,15-23;

    ул. Рыбальченко 2-12;

    ул. Марсовая 17-19,25;

    проезд Вербеновый 34-36;

    проезд Лавандовый 15-19



    «СТ-Швейник» 22/2,2-4,9-2,1-2,8;

    ул. Лесхозная 74/4;

    «СТ-Южное» 380,381



    «СТ-Вагонник» 60-А,12-14,18,24-34,40-44,50-5,1-5,9-11, 15,19-23,27-29,33,37;

    «СНТ-Статистик-2» 50,218



    «СТ-Незабудка» 9



    Максимова дача 40,11;

    ул. Летчика Корзунова 19;

    «СТ-Черноморец-2» 313,709



    с. Верхнесадовое

    ул. Гагарина 2-14,5/2,1-29;

    пер. Дорожный 1-11;

    ул. Севастопольская 86-90

    с/з Софьи Перовской 14 ,6,20,24,28,42,42,46,62-64,1,1,7,23-27,31-35,43,49, 53,59



    ул. Павла Корчагина 16



     с 08:30 до 17:30

    п. Пироговка

    ул. Урожайная 22-а,2-а,2-б,2-24,28-32,1-25,29,37;

    ул. Рабочая 2-20,422,1-А,3,13-21,167,421;

    ул. Льва Толстого 170;

    пер. Горина,7-15;

    туп. Озерный ;

    ул. Пальметная 2-36,11-В,1-Б,1-15,39;

    ул Угловая 6,3-5; ул. Рабочая 1-11;

    ул. Льва Толстого 2-24,1-15;

    ул. Озерная 2-12;

    пер. Сельский 2,1-3;

    ул. Тенистая 2-а,2,6;

    пер. Озерный 4-12



    пр. Кипарисовый 2-10,1-7;

    ул. Абрикосовая 2-42,9-А,1,5-9, 13-37,43;

    ул. Мореходная 2-60,19б/1,9-а,135-Г,19б/2,1-19,131;

    туп. Обрывистый 10,1-19;

    туп. Сливовый 1-7;

    ул. Гранатная 17-а
"""


class TestAddressConverter(TestCase):
    def test_address(self):
        self.assertEqual(
            "СТ Полет",
            address_converter("СТ «Полет» уч.")
        )

    def test_address1(self):
        self.assertEqual(
            "ул. Льва Толстого",
            address_converter("ул. Льва Толстого")
        )

    def test_address2(self):
        self.assertEqual(
            "туп. Обрывистый",
            address_converter("туп. Обрывистый")
        )

    def test_address3(self):
        self.assertEqual(
            "с/з Софьи Перовской",
            address_converter("с/з Софьи Перовской")
        )

    def test_address4(self):
        self.assertEqual(
            "СТ Черноморец-2",
            address_converter("«СТ-Черноморец-2»")
        )

    def test_address5(self):
        self.assertEqual(
            "СТ Незабудка",
            address_converter("«СТ-Незабудка»")
        )

    def test_address6(self):
        self.assertEqual(
            "СТ Икар",
            address_converter("СТ «Икар» кад.")
        )

    def test_address7(self):
        self.assertEqual(
            "СНТ Статистик-2",
            address_converter("«СНТ-Статистик-2»")
        )

class TestHouseSplitter(TestCase):

    def test_houses1(self):
        self.assertListEqual(
            house_splitter("2-12,16-24,17-А,9-А,1-19,122"),
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
                "17-А",
                "9-А",
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
                "122"
            ],
        )

    def test_houses2(self):
        self.assertListEqual(
            house_splitter("16,24, 29-В,29-Б,29-А,17-33"),
            ["16", "24", "29-В", "29-Б", "29-А", "17", "19", "21", "23", "25", "27", "29", "31", "33"]
        )

    def test_houses3(self):
        self.assertListEqual(
            house_splitter("2-60,19б/1,9-а,135-Г,19б/2,1-19,131"),
            ["2", "4", "6", "8", "10", "12", "14", "16", "18", "20", "22", "24", "26", "28", "30", "32", "34",
             "36", "38", "40", "42", "44", "46", "48", "50", "52", "54", "56", "58", "60", "19б/1", "9-а", "135-Г",
             "19б/2", "1", "3", "5", "7", "9", "11", "13", "15", "17", "19", "131"]
        )

    def test_houses4(self):
        self.assertListEqual(
            house_splitter("50,218"),
            ["50", "218"]
        )

    def test_houses_empty(self):
        self.assertListEqual(
            house_splitter(""),
            [""]
        )

    def test_houses5(self):
        self.assertListEqual(
            house_splitter("3-Б, 111, 22, 1 Б, 3-Б/4, 5/1-Б, 7-А"),
            ["3Б", "111", "22", "1Б", "3Б/4", "5/1Б", "7А"]
        )
