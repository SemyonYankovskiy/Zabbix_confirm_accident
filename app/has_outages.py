import json
import re
from datetime import datetime, date


def has_outages(input_address: tuple, json_file_name: str) -> str:
    """
    Сравнивает входной адрес с адресами из JSON-файла.

    Args:
        input_address: tuple: Входной адрес для сравнения.
        json_file_name: str : Путь к фалу (имя файла)

    Returns:
        str: Значение времени (times) в виде строки, если адрес найден, иначе пустая строка.
    """

    street = input_address[0]
    pattern = street
    print(pattern)
    try:
        with open(json_file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
        for item in data:
            print(item)
            times = item.get("times")
            street_match = re.search(street, str(item.values()))
            house_match = any(input_address[1] in x for x in item.get("houses"))
            date_match = re.search(str(date.today()), str(item.get("times")))
            print(str(date.today()), str(item.get("times")))
            if street_match and house_match and date_match:

                print("Адрес, дом, дата - ОК")
                # Адрес найден, возвращаем значение times как строку
                time_str = f"{times[0][0][11:16]}-{times[0][1][11:16]}"

                return "Плановые работы СЭ: "+time_str

            # Адрес не найден
            print("Адрес не найден")
            return ""
    except FileNotFoundError:
        return "Ошибка: JSON-файл не найден."
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON-файла."



