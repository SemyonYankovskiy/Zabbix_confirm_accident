import re
from datetime import datetime, date
from typing import List, Tuple


MONTH_VERBS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}


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

    match = re.search(r"[сc]\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", time_correction, re.IGNORECASE)
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


def current_str_to_datetime_ranges(input_str: str) -> List[Tuple[datetime, datetime]]:
    ranges: List[Tuple[datetime, datetime]] = []

    current_year = datetime.now().year

    day_and_months = re.search(
        r"(\d.*?) +(января|февраля|марта|апреля|мая|июня|июля|августа|сентрября|октября|ноября|декабря)",
        input_str,
    )
    day = day_and_months.group(1) if day_and_months else ""

    simple_day = re.match(r"^\d+$", day)
    few_days = re.match(r"^\d+(,\d+)+(\sи\s\d+)?$", day)
    range_days_verb = re.match(r"^(\d+)\sи\s(\d+)?$", day)
    range_days_symbol = re.match(r"^\d+-\d+$", day)

    if simple_day:
        # print(f"Простая дата: {simple_day.group(0)}")
        days = extract_numbers_from_string(simple_day.group(0))
    elif few_days:
        # print(f"Несколько дат: {few_days.group(0)}")
        days = extract_numbers_from_string(few_days.group(0))
    elif range_days_verb:
        # print(f"Диапазон дат: {range_days_verb.group(0)}")
        days = extract_numbers_from_string(range_days_verb.group(0))
    elif range_days_symbol:
        # print(f"Диапазон дат через тире: {range_days_symbol.group(0)}")
        days = extract_numbers_from_string(range_days_symbol.group(0))
    else:
        return ranges
        # print(f"Некорректный формат: {day}")

    month_verb: str = day_and_months.group(2) if day_and_months else ""
    month_num: int = MONTH_VERBS.get(month_verb, -1)

    dates = []
    for day_number in days:
        if is_valid_date(day_number, month_num):
            # print(f"Дата {day}.{month_num} валидна")
            dates.append(f"{day_number}.{month_num}.{current_year}")

        else:
            # print(f"Дата {day}.{month_num} невалидна")
            return ranges

    if range_days_verb or range_days_symbol:
        dates = add_intermediate_dates(dates)

    for item_date in dates:
        add_datetime_pair_to(ranges, f"{item_date} 08:00", f"{item_date} 17:00")

    return ranges


def is_valid_date(day: int, month: int) -> bool:
    # Проверка корректности номера месяца
    if month < 1 or month > 12:
        return False

    # Месяцы с 30 днями
    months_with_30_days = [4, 6, 9, 11]
    if month in months_with_30_days:
        return 1 <= day <= 30

    # Месяцы с 31 днем
    months_with_31_days = [1, 3, 5, 7, 8, 10, 12]
    if month in months_with_31_days:
        return 1 <= day <= 31

    # Февраль
    if month == 2:
        # Проверка на високосный год
        def is_leap_year(year):
            return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

        current_year = datetime.now().year
        return 1 <= day <= 29 if is_leap_year(current_year) else 1 <= day <= 28

    return False


def extract_numbers_from_string(input_string):
    """
    Извлекает все числа из строки и возвращает их в виде списка.
    :param input_string: Входная строка, содержащая числа.
    :return: Список чисел.
    """

    # Используем регулярное выражение для поиска чисел в строке
    numbers = re.findall(r"\d+", input_string)
    return [int(num) for num in numbers]


def get_days_list(days: str) -> List[int]:
    """
    Извлекает числа из строки с датами и возвращает их в виде списка.

    >>> get_days_list("1,2,3,4,5") # 1,2,3,4,5
    [1, 2, 3, 4, 5]
    >>> get_days_list("1 по 2") # 1, 2
    [1, 2]

    :param days: Строка с датами.
    :return: Список чисел.
    """
    if "по" in days:
        days_range = days.split("по")
        if len(days_range) == 2:
            start_date = days_range[0].strip()
            end_date = days_range[1].strip()
            if start_date.isdigit() and end_date.isdigit():
                return list(range(int(start_date), int(end_date) + 1))

        # Если даты не валидны, то возвращаем пустой список
        # Если не получилось преобразовать дату, то возвращаем пустой список.
        return []

    if re.search(r"[и,]", days):
        days_range = re.split(r"\s*[и,]\s*", days)
        valid_days = []
        for day in days_range:
            if day.isdigit():
                valid_days.append(int(day))  # Если дата валидна, то добавляем ее в список
        return valid_days

    if days.isdigit():
        return [int(days)]

    return []


def find_dates_in_text(text: str) -> List[date]:
    """
    Ищет даты в тексте и возвращает список дат.
    :param text: Текст, в котором искать даты.
    """
    result: List[date] = []

    for line in text.split("\n"):
        match = re.findall(
            r"(?<!обновлено )\b(?:((?:\d+ ?[пдо,и]+ ?)*\d+)\s+?"
            r"(января|февраля|марта|апреля|мая|июня|июля|августа|сентрября|октября|ноября|декабря)|"
            r"(\d\d\.\d\d\.\d\d\d\d))",
            line,
        )

        if not match:
            continue

        for part in match:
            if len(part) != 3:
                continue

            days, month_verb, complex_date = part
            if complex_date:
                # Если найдена дата, то добавляем ее в список
                result.append(datetime.strptime(complex_date, "%d.%m.%Y").date())

            elif days and month_verb:
                # Если найдены дни и месяц, то добавляем все возможные даты в список
                month_num: int = MONTH_VERBS.get(month_verb, -1)
                current_year: int = datetime.now().year
                for day in get_days_list(days):
                    try:
                        result.append(date(current_year, month_num, int(day)))
                    except ValueError:
                        pass

    return result
