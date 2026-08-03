from network.base_client import BaseNetworkClient
import requests

class ItemClient(BaseClient):
    None

    def _fetch_raw(self, dst):
        url = f""

        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.json()

    def _parse(self, raw):
        pass