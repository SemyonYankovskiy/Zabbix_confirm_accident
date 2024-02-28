import re
from datetime import datetime, timedelta
from typing import List, Tuple


def str_to_datetime_ranges(text: str) -> List[Tuple[datetime, datetime]]:
    # Выбор паттерна для обработки даты.
    # Используется исключительно для случаев когда дата задана форматом 01-04.12.24.
    datetime_match = re.search(r"(\d{2})-(\d{2})\.(\d{2}\.\d{4}) (\d{2}:\d{2}) - (\d{2}:\d{2})", text)

    if datetime_match:
        # Извлекаем данные из совпадения
        day_start, day_end, month_year, time_start, time_end = datetime_match.groups()
        # Преобразуем формат даты
        start_date = f"{day_start}.{month_year}"
        end_date = f"{day_end}.{month_year}"

        dates: List[str] = [start_date, end_date]
        times: List[str] = [time_start, time_end]

    else:
        # Для всех остальных случаев
        dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", text)
        times = re.findall(r"\d{2}:\d{2}", text)

    ranges: List[Tuple[datetime, datetime]] = []

    if len(times) >= 2 and len(dates) >= 2 and times[0] > times[1]:
        add_datetime_pair_to(ranges, f"{dates[0]} {times[0]}", f"{dates[1]} {times[1]}")
        return ranges

    if len(dates) > 1:
        dates = add_intermediate_dates(dates)

    for item_date in dates:
        add_datetime_pair_to(ranges, f"{item_date} {times[0]}", f"{item_date} {times[1]}")

    return ranges


def add_datetime_pair_to(pair_list: List[Tuple[datetime, datetime]], dt_start: str, dt_end: str) -> None:
    try:
        pair_list.append(
            (
                datetime.strptime(dt_start, "%d.%m.%Y %H:%M"),
                datetime.strptime(dt_end, "%d.%m.%Y %H:%M"),
            )
        )
    except ValueError:
        pass


def add_intermediate_dates(dates: List[str]) -> List[str]:
    """
    Функция заполнения дат между начальной и конечной датами

    :param dates: ['30.12.2024', '01.01.2025']
    :return: all_dates: ['30.12.2024', '31.12.2024', '01.01.2025']
    """
    start_date = [int(i) for i in dates[0].split(".")]
    end_date = [int(i) for i in dates[1].split(".")]
    all_dates = []

    while start_date != end_date:
        all_dates.append(".".join([str(i).zfill(2) for i in start_date]))
        if start_date[0] < 31:
            start_date[0] += 1
        elif start_date[1] < 12:
            start_date[0] = 1
            start_date[1] += 1
        else:
            start_date[0] = 1
            start_date[1] = 1
            start_date[2] += 1

    all_dates.append(".".join([str(i).zfill(2) for i in end_date]))
    print(all_dates)
    return all_dates


def update_datetime_pair(pair: Tuple[datetime, datetime], time_correction: str) -> Tuple[datetime, datetime]:
    """
    Обновляет диапазон времени через переданную строку, в которой находится уточнение временного диапазона.
    :param pair: Пара дат.
    :param time_correction: Строка поправки времени для пары.
    :return: Пара новых дат.
    """

    match = re.search(r"с\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", time_correction)
    if not match:
        return pair

    correction_time: List[Tuple[int, int]] = []
    for time in match.groups():
        hour, minutes = time.split(":")
        correction_time.append((int(hour), int(minutes)))

    new_time_from = None
    new_time_to = None

    for i, (d, (new_hour, new_minute)) in enumerate(zip(pair, correction_time)):
        # Всегда указываем день такой же как и в начале, чтобы не было перехода через ночь аварии
        res = datetime(
            year=d.year,
            month=d.month,
            day=pair[0].day,
            hour=new_hour,
            minute=new_minute,
        )
        if i == 0:
            new_time_from = res
        elif i == 1:
            new_time_to = res

    if new_time_from and new_time_to:
        return new_time_from, new_time_to

    return pair


def current_str_to_datetime_ranges(input_str):
    months = {
        "января": 1, "февраля": 2, "марта": 3, "апреля": 4,
        "мая": 5, "июня": 6, "июля": 7, "августа": 8,
        "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12
    }

    current_year = datetime.now().year

    parts = input_str.split()
    start_day = int(parts[-2])
    start_month = months[parts[-1]]
    start_date = datetime(current_year, start_month, start_day, 8, 0, 0)
    end_date = datetime(current_year, start_month, start_day, 17, 0, 0)

    if "по" in parts:
        end_day = int(parts[parts.index("по") + 1])
        # end_month = months[parts[parts.index("по") + 2]]

    date_ranges = [(start_date, end_date)]
    if "по" in parts:
        days = end_day - start_day + 1
        for i in range(1, days):
            new_start = start_date + timedelta(days=i)
            new_end = end_date + timedelta(days=i)
            date_ranges.append((new_start, new_end))

    return date_ranges
