import json

import requests


class OrisClient():

    def __init__(self):
        self._base_url = "https://oris.orientacnisporty.cz/API/"

    def get(self, method: str, **kwargs):
        params = {
            "format": "json",
            "method": method,
            **kwargs
        }
        response = requests.get(self._base_url, params=params)
        if response.status_code != 200:
            raise Exception("TODO: Change exception")
        data = json.loads(response.content)
        return data
