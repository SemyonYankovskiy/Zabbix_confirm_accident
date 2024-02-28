import json
import re
from datetime import date
from typing import List, Tuple


def json_opener(json_file_name: str) -> List[dict]:
    try:
        with open(json_file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print("Ошибка: JSON-файл не найден.")
        return []
    except json.JSONDecodeError:
        print("Ошибка: Неверный формат JSON-файла.")
        return []


def has_outages(input_address: Tuple[str, str], json_file_content: list) -> str:
    """
    Сравнивает входной адрес с адресами из JSON-файла.

    Args:
        input_address: tuple: Входной адрес для сравнения.
        json_file_content: list : Содержимое JSON-файла

    Returns:
        str: Значение времени (times) в виде строки, если адрес найден, иначе пустая строка.
    """

    # pattern = street
    street = input_address[0]

    for item in json_file_content:

        times = item.get("times")
        street_match = re.search(street, item.get("address", ""))
        house_match = input_address[1] in item.get("houses", "")
        date_match = re.search(str(date.today()), str(item.get("times")))

        if not house_match:
            house = re.search(r"(\d+)", input_address[1]).group(0)
            house_match = house in item.get("houses", "")

        if street_match and house_match and date_match:
            # Адрес найден, возвращаем значение times как строку
            print(f"{input_address} Адреc, дом, дата - ОК")
            time_str = f"{times[0][0][11:16]}-{times[0][1][11:16]}"

            return "Плановые работы СЭ: " + time_str

        # Адрес не найден
        continue
    return ""
