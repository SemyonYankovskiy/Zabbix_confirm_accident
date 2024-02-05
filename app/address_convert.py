import re
from typing import List, Tuple

from bs4.element import Tag

def address_divider(addresses: Tag) -> List[Tuple[str, str]]:
    result = []
    town = ""
    for paragraph in addresses.findAll("p"):
        if not isinstance(paragraph, Tag):
            continue

        if "strong" in str(paragraph) and paragraph.text.strip() and not re.search(r"\d", paragraph.text):
            town = re.search(r"[а-яА-Я\. ]+", paragraph.text).group(0)

        match = re.match(r"(.+?)\s?(?=\d)(.+?);?$", paragraph.text)

        if not match:
            continue

        address = match.group(1)
        houses = match.group(2)

        if "padding-left" in str(paragraph.get_attribute_list("style")):
            address = town + ", " + address
        else:
            town = ""

        result.append((address, houses))
    return result


def house_splitter(houses: str) -> List[str]:
    arr = list(houses.split(","))
    clean_address = []
    for item in arr:
        item = item.replace("(чет)", "")
        item = item.replace("(нечет)", "")
        item = item.strip()
        clean_address.append(item)

    ext_address = []
    for item in clean_address:
        if '-' in item:

            start, stop = map(str, item.split('-'))
            if not start.isnumeric() or not stop.isnumeric():
                ext_address.append(item)
                continue
            for house_num in range(int(start), int(stop) + 1, 2):
                ext_address.append(f'{house_num}')
        else:
            ext_address.append(item)

    return ext_address


def adress_converter(address: str) -> str:
    # Убираем кавычки и лишние символы
    cleaned_adress = address.replace("«", "").replace("»", "").replace("уч.", "").replace("кад.", "")

    # Проверяем, какой тип адреса
    if "СТ" in cleaned_adress:
        return cleaned_adress.replace("СТ-", "СТ ").strip()
    elif "ул." in cleaned_adress:
        return cleaned_adress.replace("ул.", "ул.").strip()
    elif "туп." in cleaned_adress:
        return cleaned_adress.replace("туп.", "туп.").strip()
    elif "с/з" in cleaned_adress:
        return cleaned_adress.replace("с/з", "с/з").strip()
    elif "СНТ" in cleaned_adress:
        return cleaned_adress.replace("СНТ-", "СНТ ").strip()
    else:
        return cleaned_adress