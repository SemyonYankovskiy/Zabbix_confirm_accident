import logging
import re
from datetime import datetime
from typing import Tuple, List, Optional

import bs4
import requests
from bs4 import BeautifulSoup

from app.address_convert import (
    update_datetime_pair,
    divide_by_address_and_house_numbers,
)


def get_planned_outages_urls(site: str = "https://sevenergo.net") -> List[str]:
    """
    Опрашивает `site` и находит список ссылок плановых отключений.
    :return: Список URL.
    """
    resp = requests.get(site)
    if resp.status_code != 200:
        logging.error(f"site={site} statusCode={resp.status_code}")
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    if soup != "":
        logging.debug(f"parsing_all - Done")
        return []

    links = soup.findAll("a", class_="dp-module-upcoming-modal-disabled")

    return [
        f'https://sevenergo.net{link.attrs["href"]}'
        for link in links
        if link.attrs.get("href")
    ]


def get_planned_outage_data(url: str) -> Optional[Tuple[str, bs4.Tag]]:
    """
    Возвращает время и содержимое планового отключения.
    :param url: Абсолютная ссылка новости.
    :return: (строка диапазона времени отключения, содержимое).
    """
    logging.debug(f"try to go on outages links")
    resp = requests.get(url)
    if resp.status_code != 200:
        logging.error(f"URL={url} statusCode={resp.status_code}")
        return

    soup = BeautifulSoup(resp.text, "lxml")
    time_range = soup.find("div", {"id": "dp-event-information"})
    content = soup.find("div", {"id": "dp-event-container-content"})

    if isinstance(content, bs4.Tag):
        return time_range.text.strip(), content


def content_parser(
    content: bs4.Tag, origin_times: List[List[datetime]]
) -> List[Tuple[str, str, List[List[datetime]]]]:
    """
    Находит в содержимом адреса и приводит их к формату (адрес, перечень номеров домов).
    Учитывает, что в блоке может быть указан также посёлок.
    Также в содержимом может содержаться уточнение временного диапазона отключения, в таком случае
    будет скорректировано на основе основного времени.

    :param content: Содержимое
    :param origin_times: Список пар временных диапазонов отключения для данного содержимого.
    :return
    """

    result = []
    town = ""
    current_time_ranges = origin_times

    for paragraph in content.findAll("p"):

        if not isinstance(paragraph, bs4.Tag):
            continue

        if (
            "strong" in str(paragraph)
            and paragraph.text.strip()
            and not re.search(r"\d", paragraph.text)
        ):
            town = re.search(r"[а-яА-Я. ]+", paragraph.text).group(0)

        elif (
            "strong" in str(paragraph)
            and paragraph.text.strip()
            and re.search(r"\d", paragraph.text)
        ):
            current_time_ranges = [
                update_datetime_pair(pair, paragraph.text.strip())
                for pair in origin_times
            ]
            continue

        address, houses = divide_by_address_and_house_numbers(paragraph.text)
        if not (address and houses):
            continue

        if "padding-left" in str(paragraph.get_attribute_list("style")):
            address = town + ", " + address
        else:
            town = ""

        result.append((address, houses, current_time_ranges))

    return result


# response = connect_and_get_resp("https://sevenergo.net/news/kalendar-otklyuchenij-elektroenergii/697.html")
# outages = planned_parser(response)
# print(outages)

# def current_outages():
#     outages = ''
#     months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'август', 'сентября', 'октября', 'ноября',
#               'декабря']
#     resp = requests.get('https://sevenergo.net/news/incident.html')
#     if resp.status_code == 200:
#         today = date.today()
#
#         soup = BeautifulSoup(resp.text, 'lxml')
#         links = soup.findAll('a', string=compile(rf'[0]*{today.day} {months[today.month - 1]}'))
#
#         for l in links:
#             print(l.text, l.attrs)
#             resp = requests.get('https://sevenergo.net' + l.attrs['href'])
#             if resp.status_code == 200:
#                 soup = BeautifulSoup(resp.text, 'lxml')
#                 header = soup.find('div', {'class': 'article-header'})
#                 content = soup.find('div', {'itemprop': 'articleBody'})
#                 print(header.text.strip())
#                 print(content.text.strip())
#                 outages += str(header) + '<br>' + str(content) + '<br><hr>'
#     print(outages)
#     return outages
