import re
from datetime import datetime

# when = """Дата
#
# 19.01.2024 08:00 - 16:00
# """
# when2 = """Дата
#
#     01.11.2023 08:00 - 03.11.2023 17:00"""


def str_to_datetime(text:str):

    dates = re.findall(r'\d{2}\.\d{2}\.\d{4}', text)
    times = re.findall(r'\d{2}:\d{2}', text)

    print(dates)
    print(times)
    times_of_outages = []

    if times[0]>times[1]:
        night_start = f"{dates[0]} {times[0]}"
        times_of_outages.append(datetime.strptime(night_start, "%d.%m.%Y %H:%M"))
        night_stop = f"{dates[1]} {times[1]}"
        times_of_outages.append(datetime.strptime(night_stop, "%d.%m.%Y %H:%M"))
        return times_of_outages

    if len(dates)>1:
        dates = add_intermediate_dates(dates)


    for item_date in dates:
        for item_time in times:
            cut = f"{item_date} {item_time}"
            times_of_outages.append(datetime.strptime(cut, "%d.%m.%Y %H:%M"))


    return times_of_outages


def add_intermediate_dates(dates):
    start_date = [int(i) for i in dates[0].split('.')]
    end_date = [int(i) for i in dates[1].split('.')]
    all_dates = []

    while start_date != end_date:
        all_dates.append('.'.join([str(i).zfill(2) for i in start_date]))
        if start_date[0] < 31:
            start_date[0] += 1
        elif start_date[1] < 12:
            start_date[0] = 1
            start_date[1] += 1
        else:
            start_date[0] = 1
            start_date[1] = 1
            start_date[2] += 1

    all_dates.append('.'.join([str(i).zfill(2) for i in end_date]))
    return all_dates



when = "Дата\n\n19.01.2024 08:00 - 16:00\n"
when2 = "Дата\n\n01.11.2023 08:00 - 03.11.2023 17:00\n"
when3 = "Дата\n\n01.11.2023 - 03.11.2023 08:00 - 17:00\n"
when4 = "06.07.2023 по 14.07.2023 с 08:30 до 17:30"
when5 = "с 23:00 03.07.2023г. до 06:00 04.07.2023г."

print(str_to_datetime(when))
print(str_to_datetime(when2))
print(str_to_datetime(when3))
print(str_to_datetime(when4))
print(str_to_datetime(when5))


