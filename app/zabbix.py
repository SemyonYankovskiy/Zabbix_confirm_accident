import urllib3
from pyzabbix import ZabbixAPI
from requests import Session
from urllib3.exceptions import InsecureRequestWarning

from app.misc import get_environ

urllib3.disable_warnings(category=InsecureRequestWarning)


class ZabbixAPIConnection:
    """Конфигурация для работы с Zabbix API"""

    ZABBIX_URL: str = get_environ("ZABBIX_URL")
    ZABBIX_USER: str = get_environ("ZABBIX_USER")
    ZABBIX_PASSWORD: str = get_environ("ZABBIX_PASSWORD")

    def __init__(self, timeout: int = 2):
        self.timeout = timeout
        self._zabbix_connection: ZabbixAPI = ZabbixAPI()
        self._session = self.get_session()

    @staticmethod
    def get_session() -> Session:
        session = Session()
        # Отключаем проверку сертификата (для самоподписного).
        session.verify = False
        return session

    def connect(self) -> ZabbixAPI:
        self._zabbix_connection = ZabbixAPI(
            server=self.ZABBIX_URL, session=self._session, timeout=self.timeout
        )
        self._zabbix_connection.login(user=self.ZABBIX_USER, password=self.ZABBIX_PASSWORD)
        return self._zabbix_connection


def event_acknowledge(event_id: str, message_text: str):
    with ZabbixAPIConnection().connect() as zbx:
        zbx.event.acknowledge(eventids=event_id, action="4", message=message_text)
