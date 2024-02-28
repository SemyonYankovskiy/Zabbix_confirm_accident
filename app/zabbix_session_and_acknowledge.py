import os
from datetime import date

from app.address_to_verbose import get_info_from_zabbix_node
from app.has_outages import has_outages


from app.zabbix import ZabbixAPIConnection
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)


def event_acknowledge(event_id: str, message_text: str):
    with ZabbixAPIConnection().connect() as zbx:
        zbx.event.acknowledge(eventids=event_id, action="4", message=message_text)