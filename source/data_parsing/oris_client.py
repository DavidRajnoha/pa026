import requests


class OrisClient():

    def __init__(self):
        self._base_url = "https://oris.orientacnisporty.cz/API/"

    def get(self, method: str, kwargs):
        params = {
            "format": "json",
            "method": method,
            **kwargs
        }
        requests.get(self._base_url, params=params)
