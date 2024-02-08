import re
from typing import List, Tuple

from bs4.element import Tag


def address_divider(addresses: Tag) -> List[Tuple[str, str]]:
    """
    Находит в контейнере div адреса и приводит их к формату (адрес, перечень номеров домов)
    Учитывает, что в блоке может быть указан также посёлок.
    """

    result = []
    town = ""
    for paragraph in addresses.findAll("p"):
        if not isinstance(paragraph, Tag):
            continue

        if (
            "strong" in str(paragraph)
            and paragraph.text.strip()
            and not re.search(r"\d", paragraph.text)
        ):
            town = re.search(r"[а-яА-Я. ]+", paragraph.text).group(0)

        address, houses = divide_by_address_and_house_numbers(paragraph.text)
        if not (address and houses):
            continue

        if "padding-left" in str(paragraph.get_attribute_list("style")):
            address = town + ", " + address
        else:
            town = ""

        result.append((address, houses))
    return result


def divide_by_address_and_house_numbers(text: str) -> Tuple[str, str]:
    """
    Разделяет строку на адрес и нумерацию домов.

    >>> divide_by_address_and_house_numbers("зона ЮБК-24 21, 23, 22, 24;")
    ('зона ЮБК-24', '21, 23, 22, 24')

    >>> divide_by_address_and_house_numbers("пос. Ласпи53/134;")
    ('пос. Ласпи', '53/134')
    """

    match = re.match(r"(.+?)(?<![-\d])\s?(?=\d)(.+?);?$", text)
    if not match:
        return "", ""
    return match.group(1).strip(), match.group(2).strip()


def house_splitter(houses: str) -> List[str]:
    """
    Разделяет строку нумераций адресов в список фактических значений.
    С учетом (не)четности домов при указании диапазона:

    >>> house_splitter("2-6,19б/1,9-а")
    ['2', '4', '6', '19б/1', '9а']
    """

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

            start, stop = map(str, item.split("-"))
            if not start.isnumeric() or not stop.isnumeric():
                ext_address.append(item)
                continue
            for house_num in range(int(start), int(stop) + 1, 2):
                ext_address.append(f"{house_num}")
        else:
            ext_address.append(item)

    clean_ext_address = []
    for item in ext_address:
        item = item.replace("-", "")
        item = item.replace(" ", "")
        clean_ext_address.append(item)

    return clean_ext_address


def address_cleaner(address: str) -> str:
    """
    Очищает адрес от лишних символов и сокращений.

    >>> address_cleaner("СТ «Икар» кад.")
    'СТ Икар'
    """
    # Убираем кавычки и лишние символы.
    cleaned: str = re.sub(r"«|»|уч\.|кад\.", "", address).strip()

    # Форматируем садовые товарищества.
    cleaned = cleaned.replace("СТ-", "СТ ")
    cleaned = cleaned.replace("СНТ-", "СНТ ")

    return cleaned
