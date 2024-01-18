import re
from typing import List

from bs4.element import Tag


def address_convert(addresses: Tag):

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

        result.append([address,houses])

    return result


def house_splitter(houses: str) -> List[str]:
    print("GOT", houses)