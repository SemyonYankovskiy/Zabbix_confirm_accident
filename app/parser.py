import logging
import re
from datetime import datetime, date
from typing import Tuple, List, Optional

import bs4
import requests
from bs4 import BeautifulSoup

from app.address_convert import divide_by_address_and_house_numbers
from app.datetime_convert import update_datetime_pair
from app.request import request_get


def get_planned_outages_urls(site: str = "https://sevenergo.net") -> List[str]:
    """
    Опрашивает `site` и находит список ссылок плановых отключений.
    :return: Список URL.
    """
    resp = request_get(site)
    if resp.status_code != 200:
        logging.error("site=%s statusCode=%s", site, resp.status_code)
        return []

    soup = BeautifulSoup(resp.text, "lxml")
    if not soup:
        logging.debug("parsing_all - Done")
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
    logging.debug("try to go on outages links")
    resp = request_get(url)
    if resp.status_code != 200:
        logging.error("URL=%s statusCode=%s", url, resp.status_code)
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    time_range = soup.find("div", {"id": "dp-event-information"})
    content = soup.find("div", {"id": "dp-event-container-content"})

    if isinstance(content, bs4.Tag) and isinstance(time_range, bs4.Tag):
        return time_range.text.strip(), content

    return None


def content_parser(
    content: bs4.Tag, origin_times: List[Tuple[datetime, datetime]]
) -> List[Tuple[str, str, List[Tuple[datetime, datetime]]]]:
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

    for tag in content.find_all(True):

        if tag.name == "p" or tag.name == "div":

            if "strong" in str(tag) and tag.text.strip():
                # Если в теге имеется тег <strong>, значит необходимо выполнить отдельную проверку
                strong_tag = tag.find("strong")

                if not re.search(r"\d", tag.text):
                    # Если нет ни одной цифры в тексте тега, значит это название поселка (села).
                    match = re.search(r"[а-яА-Я. ]+", tag.text)
                    town = match.group(0) if match else ""
                    continue

                if re.search(r"с\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", tag.text):
                    # Если указан другой временной диапазон в формате: с 08:00 до 13:00,
                    # то необходимо скорректировать начальные диапазоны.
                    current_time_ranges = [
                        update_datetime_pair(pair, tag.text.strip())
                        for pair in origin_times
                    ]
                    continue

                if (
                    strong_tag
                    and strong_tag.text.strip()
                    and strong_tag.text != tag.text
                ):
                    # Если текст, который в теге <strong> не содержит весь текст тега,
                    # то это означает, что в теге имеется как указание поселка, так и его улицы.
                    # Необходимо рассматривать этот тег далее без префикса населенного пункта.
                    town = ""

            address, houses = divide_by_address_and_house_numbers(tag.text)
            if not address:
                continue

            if "padding-left" in str(tag.get_attribute_list("style")):
                # Если в стилях тега имеется отступ, то это означает,
                # что данная запись относится к ранее указанному населенному пункту.
                address = town + ", " + address
            else:
                town = ""

            result.append((address, houses, current_time_ranges))

    return result


def current_outages():
    content = ''
    header = ''
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'август', 'сентября', 'октября', 'ноября', 'декабря']
    resp = requests.get('https://sevenergo.net/news/incident.html', timeout=10)
    if resp.status_code == 200:
        today = date.today()

        soup = BeautifulSoup(resp.text, 'lxml')
        links = soup.findAll('a', string=re.compile(rf'[0]*{today.day} {months[today.month - 1]}'))

        for l in links:
            resp = requests.get('https://sevenergo.net' + l.attrs['href'], timeout=10)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'lxml')
                header = soup.find('div', {'class': 'article-header'})
                content = soup.find('div', {'itemprop': 'articleBody'})

                # print(header.text.strip())
                # print(content.text.strip())
                #outages += str(header) + '<br>' + str(content) + '<br><hr>'
    return content, header


def get_current_outage_data(url: str) -> Optional[Tuple[str, bs4.Tag]]:
    """
    Возвращает время и содержимое планового отключения.
    :param url: Абсолютная ссылка новости.
    :return: (строка диапазона времени отключения, содержимое).
    """
    logging.debug("try to go on outages links")
    resp = request_get(url)
    if resp.status_code != 200:
        logging.error("URL=%s statusCode=%s", url, resp.status_code)
        return None

    soup = BeautifulSoup(resp.text, "lxml")
    time_range = soup.find("h4", {"itemprop": "headline"})
    content = soup.find("div", {"itemprop": "articleBody"})

    if isinstance(content, bs4.Tag) and isinstance(time_range, bs4.Tag):
        return time_range.text.strip(), content
