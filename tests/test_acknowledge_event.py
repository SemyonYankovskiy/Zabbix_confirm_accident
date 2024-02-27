import os
import re
from datetime import date

from app.address_to_verbose import get_info_from_zabbix_node
from app.has_outages import json_opener, has_outages


os.environ.setdefault("ZABBIX_URL", "")
os.environ.setdefault("ZABBIX_USER", "")
os.environ.setdefault("ZABBIX_PASSWORD", "")


from app.zabbix import ZabbixAPIConnection
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def event_acknowledge(event_id, message_text):
    with ZabbixAPIConnection().connect() as zbx:
        zbx.event.acknowledge(eventids=event_id, action="4", message=message_text)


def main():
    """
    Сюда нужно передать имя узла сети и event_id

    :return:
    """
    street, house = get_info_from_zabbix_node("SVSL-151-Kolobova18k2p3-SIP1")
    print(street, house)
    house = re.search(r'(\d+)', house).group(0)
    #data = json_opener(f"data-{date.today()}.json")
    data = [
        {
            "address": "Курчатова",
            "houses": [
                "1"
            ],
            "times": [
                [
                    "2024-02-27 08:00:00",
                    "2024-02-27 16:00:00"
                ]
            ]
        },
        {
            "address": "Колобова",
            "houses": [
                "1", "2", "3", "12", "18"
            ],
            "times": [
                [
                    "2024-02-27 08:00:00",
                    "2024-02-27 16:00:00"
                ]
            ]
        }
    ]
    text_outages = has_outages((street, house), data)

    if text_outages != "":
        print("Подтверждаю")
        event_id = 281668730
        event_acknowledge(event_id, text_outages)


if __name__ == "__main__":
    main()


