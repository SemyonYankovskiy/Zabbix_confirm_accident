import json
import random
import re
from dataclasses import dataclass

import requests

from app.request import USER_AGENTS


@dataclass
class SuggestParams:
    # callback=id_170832263824960787936&v=5&search_type=all&part=Севастополь%2C%20село%20Штурмовое%2C%20улица%20Дагджи%2C%204&
    # lang=ru_RU&n=5&origin=jsapi2Geocoder&bbox=33.215581084197936%2C44.51190712146701%2C34.086934233612%2C44.708104806690265&local_only=0
    part: str
    callback: str = f"id_17083226382496{random.randint(1_000_000, 9_999_999)}"

    def get_param_string(self) -> str:
        return (
            f"callback={self.callback}&v=5&search_type=all&part={self.part}&lang=ru_RU&n=5&origin=jsapi2Geocoder&"
            f"bbox=33.366881084197936%2C44.38760712146701%2C34.086934233612%2C44.708104806690265&local_only=0"
        )


class YaMap:

    def __init__(self):
        self._suggest_url = "https://suggest-maps.yandex.ru/suggest-geo"
        self._session = requests.Session()

    def get_coords(self, address: str) -> tuple[float, float] | None:
        random_id_1 = random.randint(1_000_000, 9_999_999)
        random_id_2 = random.randint(100_000, 9_999_999)

        resp = self._session.get(
            self._suggest_url
            + "?"
            + "add_chains_loc=1&add_coords=1&add_rubrics_loc=1&bases=geo%2Cbiz%2Ctransit&"
            f"client_reqid=170834{random_id_1}_{random_id_2}&custom_ranking=gdu_target_3&fullpath=1&lang=ru_RU&"
            "ll=33.627615%2C44.566920574566176&origin=maps-search-form&outformat=json&"
            f"part={address}&pos=38&spn=0.16334275918802632%2C0.005859354433738417&"
            f"ull=33.526405%2C44.556976&v=9&yu=4181228601708344234",
            headers={
                "User-Agent": random.choice(USER_AGENTS),
            },
            timeout=10,
        )
        if resp.status_code != 200:
            print(address, resp.status_code, resp.url, resp.text)
            return None

        position: list[str] = resp.json()["results"][0]["pos"].split(",")
        return float(position[1]), float(position[0])

    def suggest_address(self, address: str) -> str:
        resp = self._session.get(self._suggest_url + "?" + SuggestParams(part=address).get_param_string())
        if resp.status_code != 200:
            return ""
        data = json.loads(re.sub(r"^id_\d+\(|\)$", "", resp.text))
        return data[-1][0][2]
