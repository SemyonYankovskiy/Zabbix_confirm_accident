import os

from pyzabbix import ZabbixAPI
from requests import Session


class ZabbixAPIConnection:
    """Конфигурация для работы с Zabbix API"""

    ZABBIX_URL: str = os.getenv("ZABBIX_URL")
    ZABBIX_USER: str = os.getenv("ZABBIX_USER")
    ZABBIX_PASSWORD: str = os.getenv("ZABBIX_PASSWORD")

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
