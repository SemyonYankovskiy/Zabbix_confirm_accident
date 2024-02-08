import re
from datetime import datetime
from typing import List, Tuple, Sequence


def update_datetime_pair(
    pair: Sequence[datetime], time_correction: str
) -> List[datetime]:
    """
    Обновляет диапазон времени через переданную строку, в которой находится уточнение временного диапазона.
    :param pair: Пара дат.
    :param time_correction: Строка поправки времени для пары.
    :return: Пара новых дат.
    """

    match = re.search(r"с\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", time_correction)
    if not match:
        return list(pair)

    new_pair: List[datetime] = []
    time_from, time_to = match.groups()

    correction_time: List[Tuple[int, int]] = []
    for time in (time_from, time_to):
        hour, minutes = time.split(":")
        correction_time.append((int(hour), int(minutes)))

    for i, (d, (new_hour, new_minute)) in enumerate(zip(pair, correction_time)):
        d: datetime
        # Всегда указываем день такой же как и в начале, чтобы не было перехода через ночь аварии
        new_pair.append(
            datetime(
                year=d.year,
                month=d.month,
                day=pair[0].day,
                hour=new_hour,
                minute=new_minute,
            )
        )
    return new_pair


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
        item = re.sub(r"\(.*\)", "", item)
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
