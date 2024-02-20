import json
from datetime import datetime


def has_outages(input_address: tuple, json_file_name: str) -> str:
    """
    Сравнивает входной адрес с адресами из JSON-файла.

    Args:
        input_address: tuple: Входной адрес для сравнения.
        json_file_name: str : Путь к фалу (имя файла)

    Returns:
        str: Значение времени (times) в виде строки, если адрес найден, иначе пустая строка.
    """

    try:
        with open(json_file_name, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            for item in json_file:


            zabbix_input_address = f"{input_address[0]} {input_address[1]}"

            print("1)", address_from_json)
            print("2)", zabbix_input_address)

            if address_from_json and address_from_json == zabbix_input_address:
                # Адрес найден, возвращаем значение times как строку
                print("Адрес найден")
                times = data.get("times")
                if times:
                    return "Плановые работы СЭ: "+str(times)
            # Адрес не найден
            print("Адрес не найден")
            return ""
    except FileNotFoundError:
        return "Ошибка: JSON-файл не найден."
    except json.JSONDecodeError:
        return "Ошибка: Неверный формат JSON-файла."



