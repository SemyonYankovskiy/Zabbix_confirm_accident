from datetime import date
from re import findall, compile
from typing import Tuple, List

import bs4
import requests
from bs4 import BeautifulSoup


def get_planned_outages() -> List[Tuple[str, str, bs4.Tag]]:
    resp = requests.get('https://sevenergo.net')
    if resp.status_code != 200:
        return []

    outages = []
    today = date.today()
    soup = BeautifulSoup(resp.text, 'lxml')
    links = soup.findAll('a', class_='dp-module-upcoming-modal-disabled')

    for l in links:
        if findall(fr'отключение электроэнергии [0]*{today.day}\S*?\.0*{today.month}\S*?\.{today.year}', l.text):
            resp = requests.get('https://sevenergo.net' + l.attrs['href'])
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, 'lxml')
            header = soup.find('h2', {'id': 'dp-event-event-header'})
            when = soup.find('div', {'id': 'dp-event-information'})
            content = soup.find('div', {'id': 'dp-event-container-content'})
            if isinstance(content, bs4.Tag):
                outages.append((header.text.strip(), when.text.strip(), content))
    return outages


def current_outages():
    outages = ''
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'август', 'сентября', 'октября', 'ноября',
              'декабря']
    resp = requests.get('https://sevenergo.net/news/incident.html')
    if resp.status_code == 200:
        today = date.today()

        soup = BeautifulSoup(resp.text, 'lxml')
        links = soup.findAll('a', string=compile(rf'[0]*{today.day} {months[today.month - 1]}'))

        for l in links:
            print(l.text, l.attrs)
            resp = requests.get('https://sevenergo.net' + l.attrs['href'])
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'lxml')
                header = soup.find('div', {'class': 'article-header'})
                content = soup.find('div', {'itemprop': 'articleBody'})
                print(header.text.strip())
                print(content.text.strip())
                outages += str(header) + '<br>' + str(content) + '<br><hr>'
    print(outages)
    return outages


if __name__ == '__main__':
    print(type(get_planned_outages()[0][-1]))
