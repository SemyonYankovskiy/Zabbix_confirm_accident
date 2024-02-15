import re
from typing import Tuple

dr_dict = {
    "Aktybinsk": "Актюбинская",
    "Aktyubinsk": "Актюбинская",
    "Gorpisw": "Горпищенко",
    "Pobedi": "Победы",
    "GO": "Генерала Острякова",
    "Balt": "Балтийская",
    "Dionis": "Дионис",
    "GOstryak": "Генерала Острякова",
    "Hrust": "Хрусталева",
    "Industr": "Индустриальная",
    "Kamysh": "Камышовое шоссе",
    "Rudn": "Руднева",
    "Solov": "Соловьёва",
    "Tokar": "Токарева",
    "Ugolnaya": "Угольная",
    "Koshev": "Олега Кошевого",
    "Musyk": "Николая Музыки",
    "BMorsk": "Большая Морская",
    "Lenin": "Ленина",
    "AdOkt": "Адмирала Октябрьского",
    "Gogol": "Гоголя",
    "Ochak": "Очаковцев",
    "GP": "Генерала Петрова",
    "6Bastion": "6-я Бастионная",
    "GPetrova": "Генерала Петрова",
    "Karant": "Карантинная",
    "Kommun": "Коммунистическая",
    "Pozhar": "Пожарова",
    "Safron": "Сафронова",
    "Tolstogo": "Льва Толстого",
    "Vakulenchuka": "Вакуленчука",
    "Vakulench": "Вакуленчука",
    "Mensh": "Меньшикова",
    "Repin": "Репина",
    "Tulsk": "Тульская",
    "Gluh": "Глухова",
    "LChayk": "Лизы Чайкиной",
    "Sladk": "Сладкова",
    "GStalingr": "Героев Сталинграда",
    "Antichn": "Античный",
    "GBrest": "Героев Бреста",
    "Kesaev": "Астана Кесаева",
    "Mayach": "Маячная",
    "POR": "Октябрьской Революции",
    "Shevchenko": "Шевченко",
    "Fiolent": "Фиолентовское шоссе",
    "KPotap": "Комбрига Потапова",
    "Marines": "Александра Маринеско",
    "Shevch": "Тараса Шевченко",
    "HutLukomsk": "Лукомская",
    "Kosareva": "Косарева",
    "Kosar": "Косарева",
    "MolStroy": "Молодых Строителей",
    "Stepan": "Степаняна",
    "Krestovskogo": "Крестовского",
    "Aksut": "Аксютина",
    "Drapushko": "Драпушко",
    "Fizkult": "Физкультурная",
    "Krestovsk": "Крестовского",
    "Mira": "Мира",
    "Nevsk": "Невская",
    "Novik": "Новикова",
    "perFiz": "Физкультурный",
    "Raket": "Ракетная",
    "Solnech": "Солнечная",
    "Kolob": "ул. Колобова",
    "Fiol": "Фиолентовское шоссе",
    "Kolobova": "ул. Колобова",
    "Stolet": "Столетовский",
    "Raenko": "Раенко",
    "Primorsk": "Приморская",
    "BKazachia": "Казачья",
    "Ryb": "Рыбак",
    "Saturn": "Сатурн",
    "ZBbKamish": "Западный берег Камышовой бухты",
    "Ahtiar": "Ахтиар",
    "bKazachya": "Казачья",
    "Ligovsk": "Лиговская",
    "Pilot_Sev": "Пилот",
    "Vodok": "Водоканал-2",
    "Fadeeva": "Адмирала Фадеева",
    "Fiolentov": "Фиолентовское шоссе",
    "Otradn": "Отрадная",
    "Parkov": "Парковая",
    "Shitov": "Щитовая",
    "Korchag": "Павла Корчагина",
    "Ribakov": "Рыбаков",
    "Bluher": "Маршала Блюхера",
    "BMihail": "Бориса Михайлова",
    "MarKril": "Маршала Крылова",
    "Pravd": "Правды",
    "Proletar": "Пролетарская",
    "Proletarskaya": "Пролетарская",
    "Chelnok": "Челнокова",
    "GSev": "Героев Севастополя",
    "Istomin": "Истомина",
    "Mihailovskaya": "Михайловская",
    "Buryaka": "Буряка",
    "Gromov": "Громова",
    "Gvardeisk": "Гвардейская",
    "Machtov": "Мачтовая",
    "Mihaylovs": "Михайловская",
    "Simonka": "Симонка",
    "Simonok": "Симонка",
    "SosnR": "Сосновая роща",
    "SrednProezd": "Средний",
    "Yakornaya": "Якорная",
    "VoenStroit": "Военных строителей",
    "perRubeg": "Рубежный",
    "Pilot_Mys": "Пилот",
    "Pilot_UG": "Пилот",
    "Vstroitel": "Военных строителей",
    "GPodvodnikov": "Героев Подводников",
    "50let": "50-летия СССР",
    "DmUlyan": "Дмитрия Ульянова",
    "Drevn": "Древняя",
    "Dybenko": "Павла Дыбенко",
    "Erosh": "Ерошенко",
    "Gagarina": "Гагарина",
    "NOstrovs": "Надежды Островской",
    "Podvodn": "Героев Подводников",
    "Shostaka": "Шостака",
    "Vakul": "Вакуленчука",
    "Gorpischenko": "Горпищенко",
    "Gorpish": "Горпищенко",
    "Semipalat": "Семипалатинская",
    "Pobedy": "Победы",
    "Melnika": "Генерала Мельника",
    "Gelovani": "Геловани",
    # "RELE": " ",
    "Izumrud": "Изумруд",
    "LASPI": "Ласпи",
    "SZ_YUBK": "Севастопольская зона ЮБК",
    "IzumrudAdm": "Изумруд",
    # "Andreevka": "с. Андреевка",
    # "Solnechniy": "п. Солнечный",
    "Centralnaya": "Центральная",
    "Nevskaya": "Невская",
    # "Gollandia": " ",
    "Blyuhera": "Маршала Блюхера",
    "Flagman": "Флагманская",
    # "MaksDacha": " ",
    "Kalicha": "Калича",
    "Stroitelnaya": "Строительная",
    # "Ternovka": " ",
    "Rabochaya": "Рабочая",
    "Korabelnaya": "Корабельная",
    "Zhidilova": "Генерала Жидилова",
    "Makarova": "Адмирала Макарова",
    # "Orlinoe": " ",
    "Kedrovaya": "Кедровая",
    "Pahomova": "Ивана Пахомова",
    "Smotrovaya": "Смотровая площадка",
    "Volodarskogo": "Володарского",
    "Popova": "Попова",
    "Sovetskaya": "Советская",
    # "Kacha": " ",
    "Aviat": "Авиаторов",
    # "Komendat": " ",
    "Krasnoar": "Красноармейская",
    "Nesterova": "Нестерова",
    "Parusk": "Отель Парус",
    # "Orlovka": " ",
    # "Belbek": " ",
    "KachinskoeShosse": "Качинское шоссе",
    # "Lyubimovka": " ",
    "Shkolnaya": "Школьная",
    "VyazRoscha": "Вязовая роща",
    "STBereg": "Берег",
    # "Vavilovo": " ",
    "Parshina": "Паршина",
    # "Verhnesadovoe": " ",
    # "VerhnesadovoeAdm": " ",
    # "VerhnesadovoeBiblioteka": " ",
    "Bogdanova": "Богданова",
    # "BogdMarket": " ",
    # "SahGolovka": " ",
    "Angarskaya": "Ангарская",
    # "GRES": " ",
    "Shubikova": "Шубикова",
    "Timiryazeva": "Тимирязева",
    "Tolbuhina": "Толбухина",
    "Odesskaya": "Одесская",
    "GStal": "Героев Сталинграда",
    # "OMEGA": "Омега",
    "ParkPobedy": "Парк Победы",
    "Yumasheva": "Юмашева",
    # "Akvamarin": " ",
    "NOstr": "Надежды Островской",
    # "AhmatovaPark": " ",
    "DUlyanova": "Дмитрия Ульянова",
    "Efremova": "Ефремова",
    "Eroshenko": "Ерошенко",
    "FiolentSh": "Фиолентовское шоссе",
    "LChaikinoi": "Лизы Чайкиной",
    "Menshikova": "Меньшикова",
    "Repina": "Репина",
    "Universitet": "Университетская",
    "Konduktor": "Кондукторская",
    "Ohotskaya": "Охотская",
    # "10KM": "",
    "Dneprovskaya": "Днепровская",
    "GOstryakova": "Генерала Острякова",
    "Hrustaleva": "Хрусталёва",
    "Kievskaya": "Киевская",
    # "Sevenergo": " ",
    "Silaeva": "Силаева",
    "Gasforta": "Гасфорта",
    "Ind": "Индустриальная",
}
dr_dict_jr = {
    "Andreevka": (r'Андреевка(.+?)Центральная', '22'),
    "Solnechniy": (r'Солнечный(.+?)Андреевская', '21'),
    "Gollandia": ('Курчатова', '10'),
    "Ternovka": (r'Терновка(.+?)Ленина', '2'),
    "Orlinoe": (r'Орлиное(.+?)Тюкова', '66'),
    "Kacha": (r'Кача(.+?)Авиаторов', '9'),
    "Orlovka": (r'Осипенко(.+?)Сухий', '1'),
    "Lyubimovka": (r'Любимовка(.+?)Софьи Перовской', '66'),
    "Vavilovo": ('Дальнее', '1'),
    "Verhnesadovoe": (r'Верхнесадовое(.+?)Севастопольская', '66'),
    "VerhnesadovoeAdm": (r'Верхнесадовое(.+?)Севастопольская', '82'),
    "VerhnesadovoeBiblioteka": (r'Верхнесадовое(.+?)Севастопольская', '53'),
    "BogdMarket": ('Богданова', '15'),
    "SahGolovka": (r'Сахарная Головка(.+?)Трактористов', '9а'),
    "GRES": ('Яблочкова', '5'),
    "Akvamarin": ('Парковая', '11'),
    "10KM": ('пер. Новикова', '1'),
    "Sevenergo": ('Хрусталёва', '44'),
    "MaksDacha": ('Каштановая', '3'),
    "OMEGA": ('Челнокова', '10'),
    "AhmatovaPark": ('парк Анны Ахматовой', ''),

}


def get_info_from_zabbix_node(name: str) -> Tuple[str, str]:
    res = []
    street = ""
    house = ""

    match = re.search(
        r"(?:SVSL|FTTB|MSAN)[-_](?:\d+[-_])?(\d{0,2}[a-z_A-Z]+)(\d+[abvwgdeABVWGDE\d]{0,2})?([k\-.]\d{1,2})?\S*", name,
        flags=re.IGNORECASE)
    if match:
        res.append(match.groups())
        # тут разделение на все 3 интересующие нас группы улицу, дом и корпус
        street_zabbix = match.group(1)
        house_zabbix = match.group(2)
        korpus_zabbix = match.group(3)

        # костыль, чтобы не менять регулярку
        if street_zabbix == "GOstryakova_" or street_zabbix == "GStalingr_":
            street_zabbix = street_zabbix.replace("_", "")
        # тут так надо, тот, кто удалит - лох
        if "Saturn2" in name:
            return 'Сатурн-2', ''
        if name == "SVSL-811-Kalicha-ASW1":
            return 'Калича', '15'

        if house_zabbix is None:
            house_zabbix = ""

        if korpus_zabbix is None:
            korpus_zabbix = ""

        house = f"{house_zabbix + korpus_zabbix}"
        house = house.lower()
        house = replace_english_with_russian(house)

        street = dr_dict.get(street_zabbix)  # Проверяем улицу в первом словаре dr_dict
        if street is None:  # Если в первом словаре нет, то берем данные из второго словаря dr_dict_jr
            res = dr_dict_jr.get(street_zabbix)
            if res:
                return res
            else:
                return '', ''

    return street, house


def replace_english_with_russian(text: str) -> str:
    # Создаем словарь для замены символов
    translation_dict = {
        'a': 'а',
        'b': 'б',
        'v': 'в',
        'g': 'г',
        'd': 'д',
        'e': 'е',

        'k': '/',
        '.': '/',
        '-': '/',
    }

    # Проходим по каждому символу в строке и заменяем его, если он есть в словаре
    result = ''
    for char in text:
        if char.lower() in translation_dict:
            result += translation_dict[char.lower()]
        else:
            result += char

    return result
