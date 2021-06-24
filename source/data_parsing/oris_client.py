import json

import requests


class OrisApiErrorException(Exception):
    pass


class OrisClient:
    """
    Small client for the ORIS API
    More information at https://oris.orientacnisporty.cz/API/
    """

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
            raise OrisApiErrorException()
        data = json.loads(response.content)
        return data
