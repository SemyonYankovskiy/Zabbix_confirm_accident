import re
from datetime import datetime
from typing import List


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


def str_to_datetime_ranges(text: str) -> List[List[datetime]]:
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

    times_of_outages: List[List[datetime]] = []

    if times[0] > times[1]:
        night_start = f"{dates[0]} {times[0]}"
        night_stop = f"{dates[1]} {times[1]}"
        times_of_outages.append(
            [
                datetime.strptime(night_start, "%d.%m.%Y %H:%M"),
                datetime.strptime(night_stop, "%d.%m.%Y %H:%M"),
            ]
        )
        return times_of_outages

    if len(dates) > 1:
        dates = add_intermediate_dates(dates)

    for item_date in dates:
        pair: List[datetime] = []
        for item_time in times:
            cut = f"{item_date} {item_time}"
            pair.append(datetime.strptime(cut, "%d.%m.%Y %H:%M"))
        times_of_outages.append(pair)

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
