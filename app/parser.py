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


class ContentParser:  # pylint: disable=too-few-public-methods
    """
    Находит в содержимом адреса и приводит их к формату (адрес, перечень номеров домов).
    Учитывает, что в блоке может быть указан также посёлок.
    Также в содержимом может содержаться уточнение временного диапазона отключения, в таком случае
    будет скорректировано на основе основного времени.
    """

    def __init__(self, content: bs4.Tag, origin_times: List[Tuple[datetime, datetime]]):
        self._content: bs4.Tag = content
        self._origin_times: List[Tuple[datetime, datetime]] = origin_times

        self._result: List[Tuple[str, str, List[Tuple[datetime, datetime]]]] = []
        self._town: str = ""
        self._town_children_under_padding: bool = True
        self._current_time_ranges: List[Tuple[datetime, datetime]] = origin_times

    class SkipIterationException(Exception):
        pass

    def _find_and_set_new_dates(self, text: str) -> bool:
        # Если нужно уточнить даты отключения.
        dates = find_dates_in_text(text)
        if dates:
            valid_time_ranges = []
            # Проходим по всем начальным диапазонам отключения.
            for time_range_pair in self._origin_times:
                if time_range_pair[0].date() in dates:
                    valid_time_ranges.append(time_range_pair)
            self._current_time_ranges = valid_time_ranges
        return len(dates) > 0

    def _find_and_set_new_times(self, text: str) -> bool:
        # Если указан другой временной диапазон в формате: с 08:00 до 13:00
        # Также учитываем возможную ошибку символа `с` на англ. и рус.
        match = re.search(r"[сc]\s+(\d\d:\d\d)\s+до\s+(\d\d:\d\d)", text)
        if match:
            self._current_time_ranges = [
                update_datetime_pair(pair, text) for pair in self._current_time_ranges
            ]
        return match is not None

    def _find_and_set_times_and_dates(self, text: str):
        found_dates = self._find_and_set_new_dates(text)
        found_times = self._find_and_set_new_times(text)
        if found_dates or found_times:
            raise self.SkipIterationException

    def _process_strong_tag(self, tag: bs4.Tag):
        tag_text = tag.text.strip()
        strong_tag = tag.find("strong")
        strong_tag_text = strong_tag.text.strip()

        if not re.search(r"\d", tag_text) and strong_tag_text == tag_text:
            # Если нет ни одной цифры в тексте тега, значит это название поселка (села).
            self._find_and_set_new_town(r"([а-яА-Я. ]+)", tag_text)

        if strong_tag and strong_tag.text.strip() and strong_tag_text != tag_text:
            # Если текст, который в теге <strong> не содержит весь текст тега,
            # то это означает, что в теге имеется как указание поселка, так и его улицы.
            # Необходимо рассматривать этот тег далее без префикса населенного пункта.
            try:
                self._find_and_set_new_town(r"([а-яА-Я. ]+)", strong_tag.text)
            except self.SkipIterationException:
                pass

    def _find_and_set_new_town(self, pattern: str, text: str) -> None:
        town_math = re.match(pattern, text)
        if town_math:
            self._town = town_math.group(1)
            raise self.SkipIterationException

    def _check_keyword(self, tag: bs4.Tag) -> None:
        keywords = ["профилактическим", "ремонтом", "подстанции"]
        # Разделяем строку на слова
        words_in_string = tag.text.split()
        # Проверяем, есть ли хотя бы одно слово из массива в переменной
        if any(word in keywords for word in words_in_string):
            raise self.SkipIterationException

    def _check_tag(self, tag: bs4.Tag) -> None:
        if tag.name not in ("p", "div"):
            raise self.SkipIterationException

    def _find_addresses(self, text: str):
        for line in text.split(";"):
            if not line.strip():
                continue

            address, houses = divide_by_address_and_house_numbers(line)
            if address:
                if self._town and not address.startswith(self._town):
                    # Добавляем населенный пункт, если он есть.
                    address = self._town + ", " + address

                self._result.append((address, houses, self._current_time_ranges))

    def _process_town(self, tag: bs4.Tag) -> None:
        if "padding-left" in str(tag.get_attribute_list("style")):
            # Если в стилях тега имеется отступ, то это означает,
            # что данная запись относится к ранее указанному населенному пункту.
            self._town_children_under_padding = True

        elif self._town_children_under_padding:
            # Если имеется ранее указанный населенный пункт и требуется искать улицу в отступе, но его нет,
            # значит будем учитывать, что последующие записи населенного пункта будут до следующей пустой строчки.
            self._town_children_under_padding = False
            if self._town:
                self._town = ""

        if self._town and not self._town_children_under_padding:
            # Если нет отступа, то будем учитывать,
            # что последующие записи населенного пункта будут до следующей пустой строчки.
            if not tag.text.strip():
                self._town = ""

    def _check_notag_exp(self):
        html_string = str(self._content)

        # Разбиваем строку на строки по тегу <br>
        lines = html_string.split("<br/>")

        # Оборачиваем каждую строку в теги <p>
        wrapped_lines = [f"<p>{line.strip()}</p>" for line in lines]

        # Соединяем строки обратно в одну строку
        processed_html = "\n".join(wrapped_lines)
        new_str = processed_html[3:]
        new_str2 = new_str[:-4]

        self._content = BeautifulSoup(new_str2, "html.parser")

    def _process_tag(self, tag):
        try:
            self._check_keyword(tag)
            self._check_tag(tag)
            tag_text = re.sub("\xa0", " ", tag.text.strip()) if tag.text else ""

            self._find_and_set_times_and_dates(tag_text)

            # Если в теге имеется тег <strong>, значит необходимо выполнить отдельную проверку
            if "strong" in str(tag) and tag_text:
                self._process_strong_tag(tag)
            elif tag_text:
                # Ищем село или поселок в тексте тега.
                # Также учитываем возможную ошибку символа с на англ. и рус.
                self._find_and_set_new_town(r"(?:[cс]\.|по[cс]\.|г\.|п\.)\s*([а-яА-Я]+)[:;]?$", tag_text)

            self._process_town(tag)
            self._find_addresses(tag_text)

        except self.SkipIterationException:
            pass

    def parse(self) -> List[Tuple[str, str, List[Tuple[datetime, datetime]]]]:
        for tag in self._content.find_all(True):
            self._process_tag(tag)

        if not self._result:
            self._check_notag_exp()
            for tag in self._content.find_all(True):
                self._process_tag(tag)

        return self._result


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

    parser = ContentParser(content, origin_times)
    return parser.parse()


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

    resp = request_get("https://sevenergo.net/news/incident.html")
    if resp.status_code == 200:
        today = date.today()

        soup = BeautifulSoup(resp.text, "lxml")
        blog = soup.find("div", {"class": "blog"})
        if not isinstance(blog, bs4.Tag):
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

    return None
