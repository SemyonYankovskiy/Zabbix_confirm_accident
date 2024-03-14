import json
import re
from datetime import datetime, timedelta
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


def has_outages(input_address: Tuple[str, str], check_datetime: datetime, json_file_content: list) -> str:
    """
    Сравнивает входной адрес с адресами из JSON-файла.

    Args:
        input_address: tuple: Входной адрес для сравнения.
        check_datetime: datetime: Дата и время которая должна быть в промежутке отключений.
        json_file_content: list : Содержимое JSON-файла.

    Returns:
        str: Значение времени (times) в виде строки, если адрес найден, иначе пустая строка.
    """

    street = input_address[0]
    house = input_address[1]

    for item in json_file_content:
        has_street: bool = bool(street and re.search(street, item.get("address", "")))
        has_house: bool = house in item.get("houses", [])

        if not has_house:
            house_match = re.search(r"\d+", house)
            if house_match is not None:
                has_house = house_match.group(0) in item.get("houses", [])

        if not (has_street and has_house):
            continue

        for datetime_range in item.get("times", []):
            dt_from: datetime = datetime.strptime(datetime_range[0], "%Y-%m-%d %H:%M:%S")
            dt_to: datetime = datetime.strptime(datetime_range[1], "%Y-%m-%d %H:%M:%S")
            if dt_from - timedelta(minutes=15) <= check_datetime <= dt_to + timedelta(minutes=15):

                verbose_format = (
                    "%H:%M" if dt_from.date() == dt_to.date() == check_datetime.date() else "%d.%m.%Y %H:%M"
                )
                verbose = "Плановые работы СЭ: с "
                verbose += dt_from.strftime(verbose_format)
                verbose += " до "
                verbose += dt_to.strftime(verbose_format)
                return verbose

    return ""
