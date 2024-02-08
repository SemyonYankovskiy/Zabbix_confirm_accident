import re
from datetime import datetime
from typing import List, Tuple, Sequence


def check_date_format(date_str):
    # Паттерн для формата даты и времени: dd.mm.yyyy hh:mm - hh:mm
    pattern = r"\d{2}\-\d{2}\.\d{2}\.\d{4} \d{2}:\d{2} - \d{2}:\d{2}"

    # Ищем совпадение паттерна
    match = re.search(pattern, date_str)

    # Если найдено совпадение, возвращаем True, иначе False
    if match:
        return False
    else:
        return True


def str_to_datetime_ranges(text: str) -> List[Tuple[datetime, datetime]]:
    dates = []
    times = []

    if check_date_format(text):
        dates = re.findall(r"\d{2}\.\d{2}\.\d{4}", text)
        times = re.findall(r"\d{2}:\d{2}", text)
    else:
        pattern = r"(\d{2})-(\d{2})\.(\d{2}\.\d{4}) (\d{2}:\d{2}) - (\d{2}:\d{2})"
        # Ищем совпадения в строке
        match = re.search(pattern, text)
        if match:
            # Извлекаем данные из совпадения
            day_start, day_end, month_year, time_start, time_end = match.groups()
            # Преобразуем формат даты
            start_date = f"{day_start}.{month_year}"
            end_date = f"{day_end}.{month_year}"

            dates = [start_date, end_date]
            times = [time_start, time_end]

        else:
            print("Некорректный формат даты")

    times_of_outages: List[Tuple[datetime, datetime]] = []

    if times[0] > times[1]:
        times_of_outages.append(
            (
                datetime.strptime(f"{dates[0]} {times[0]}", "%d.%m.%Y %H:%M"),
                datetime.strptime(f"{dates[1]} {times[1]}", "%d.%m.%Y %H:%M"),
            )
        )
        return times_of_outages

    if len(dates) > 1:
        dates = add_intermediate_dates(dates)

    for item_date in dates:
        times_of_outages.append(
            (
                datetime.strptime(f"{item_date} {times[0]}", "%d.%m.%Y %H:%M"),
                datetime.strptime(f"{item_date} {times[1]}", "%d.%m.%Y %H:%M"),
            )
        )

    return times_of_outages


def add_intermediate_dates(dates: List[str]) -> List[str]:
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
    return all_dates


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