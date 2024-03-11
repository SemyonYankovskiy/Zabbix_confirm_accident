import re
from typing import List, Tuple


def divide_by_address_and_house_numbers(text: str) -> Tuple[str, str]:
    """
    Разделяет строку на адрес и нумерацию домов.

    >>> divide_by_address_and_house_numbers("зона ЮБК-24 21, 23, 22, 24;")
    ('зона ЮБК-24', '21, 23, 22, 24')

    >>> divide_by_address_and_house_numbers("пос. Ласпи53/134;")
    ('пос. Ласпи', '53/134')
    """

    match = re.match(
        r"((?:пос\.|пл\.|площадь|ул\.|пер\.|туп\.)?.{3,}?),?(?<![-\d])\s?(\d.*?)?[;,.]?$",
        text,
    )
    if not match:
        return "", ""
    return (match.group(1) or "").strip(), (match.group(2) or "").strip()


def house_splitter(houses: str) -> List[str]:
    """
    Разделяет строку нумераций адресов в список фактических значений.
    С учетом (не)четности домов при указании диапазона:

    >>> house_splitter("2-6,19б/1,9-а")
    ['2', '4', '6', '19б/1', '9а']
    """

    houses = re.sub(r"\(.*?\)", "", houses)
    arr = list(houses.split(","))
    clean_address = []
    for item in arr:
        item = item.replace("(чет)", "")
        item = item.replace("(нечет)", "")
        item = item.replace(".", "")
        item = item.strip()
        clean_address.append(item)

    ext_address = []
    for item in clean_address:
        if "-" in item:
            start, stop = item.split("-", 1)
            if not start.isnumeric() or not stop.isnumeric():
                ext_address.append(item)
                continue
            if start.isnumeric() and stop.isnumeric():
                start = int(start)
                stop = int(stop)
                if start > stop:
                    start, stop = stop, start
                if stop > 600:
                    stop = 600
                for house_num in range(start, stop + 1, 2):
                    ext_address.append(f"{house_num}")
        else:
            ext_address.append(item)

    clean_ext_address = []
    for item in ext_address:
        item = item.replace("-", "")
        item = item.replace(" ", "")

        clean_ext_address.append(item)

    return [num for num in clean_ext_address if num]


def address_cleaner(address: str) -> str:
    """
    Очищает адрес от лишних символов и сокращений.

    >>> address_cleaner("СТ «Икар» кад.")
    'СТ Икар'
    """
    # Убираем кавычки и лишние символы.
    cleaned: str = re.sub(r"«|»|уч\.|кад\.|тер |д\.", "", address).strip()

    # Форматируем садовые товарищества.
    cleaned = cleaned.replace("ТСН СНТ", "СНТ")
    cleaned = cleaned.replace("СТ-", "СТ ")
    cleaned = cleaned.replace("СНТ-", "СНТ ")
    cleaned = cleaned.replace("ТСН-", "СНТ ")
    cleaned = cleaned.replace("ТСН ", "СНТ ")

    return cleaned
