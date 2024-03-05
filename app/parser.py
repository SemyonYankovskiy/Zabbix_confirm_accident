import logging
import re
from datetime import datetime, date
from typing import Tuple, List, Optional

import bs4
import requests
from bs4 import BeautifulSoup

from app.address_convert import divide_by_address_and_house_numbers
from app.datetime_convert import update_datetime_pair, find_dates_in_text
from app.request import request_get


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
    town_children_under_padding = True
    current_time_ranges = origin_times

    for tag in content.find_all(True):
        datetime_modified = False
        if tag.name not in ("p", "div"):
            continue

        tag_text = tag.text.strip() if tag.text else ""

        # Если нужно уточнить даты отключения.
        new_dates_match = find_dates_in_text(tag_text)
        if new_dates_match:
            datetime_modified = True
            valid_time_ranges = []
            # Проходим по всем начальным диапазонам отключения.
            for time_range_pair in origin_times:
                if time_range_pair[0].date() in new_dates_match:
                    valid_time_ranges.append(time_range_pair)
            current_time_ranges = valid_time_ranges

        # Если указан другой временной диапазон в формате: с 08:00 до 13:00
        # Также учитываем возможную ошибку символа `с` на англ. и рус.
        if re.search(r"[сc]\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", tag_text):
            datetime_modified = True
            current_time_ranges = [update_datetime_pair(pair, tag_text) for pair in current_time_ranges]

        # Если было уточнение временного диапазона отключения, то пропускаем текущий блок.
        if datetime_modified:
            continue

        # Если в теге имеется тег <strong>, значит необходимо выполнить отдельную проверку
        if "strong" in str(tag) and tag_text:
            strong_tag = tag.find("strong")

            if not re.search(r"\d", tag_text):
                # Если нет ни одной цифры в тексте тега, значит это название поселка (села).
                match = re.search(r"[а-яА-Я. ]+", tag_text)
                town = match.group(0) if match else ""
                continue

            if strong_tag and strong_tag.text.strip() and strong_tag.text != tag_text:
                # Если текст, который в теге <strong> не содержит весь текст тега,
                # то это означает, что в теге имеется как указание поселка, так и его улицы.
                # Необходимо рассматривать этот тег далее без префикса населенного пункта.
                town = ""

        elif tag_text:
            # Если указано село или поселок не в strong
            # Также учитываем возможную ошибку символа `с` на англ. и рус.
            town_math = re.match(r"([cс]\.|по[cс]\.|г\.|п\.)\s*([а-яА-Я]+)[:;]?$", tag_text)
            if town_math:
                town = town_math.group(2)
                continue

        address, houses = divide_by_address_and_house_numbers(tag.text)

        if "padding-left" in str(tag.get_attribute_list("style")):
            # Если в стилях тега имеется отступ, то это означает,
            # что данная запись относится к ранее указанному населенному пункту.
            town_children_under_padding = True

        elif town and town_children_under_padding:
            # Если имеется ранее указанный населенный пункт и требуется искать улицу в отступе, но его нет,
            # значит будем учитывать, что последующие записи населенного пункта будут до следующей пустой строчки.
            town_children_under_padding = False

        if town and not town_children_under_padding:
            # Если нет отступа, то будем учитывать,
            # что последующие записи населенного пункта будут до следующей пустой строчки.
            if not address:
                town = ""

        # Пропускаем пустой адрес
        if not address:
            continue

        # Добавляем населенный пункт, если он есть.
        if town:
            address = town + ", " + address

        result.append((address, houses, current_time_ranges))

    return result


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

    return [f'{site}{link.attrs["href"]}' for link in links if link.attrs.get("href")]


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


def get_current_outages_urls() -> List[str]:
    links_for_today = []

    resp = requests.get("https://sevenergo.net/news/incident.html", timeout=10)
    if resp.status_code == 200:
        today = date.today()

        soup = BeautifulSoup(resp.text, "lxml")
        blog = soup.find("div", {"class": "blog"})
        if not blog:
            return []

        for link in blog.findAll("a"):
            # Проверяем, что ссылка на текущую дату
            if today in find_dates_in_text(link.text) and link.attrs.get("href"):
                links_for_today.append(f"https://sevenergo.net/{link.attrs['href']}")

    return links_for_today


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
