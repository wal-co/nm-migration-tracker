import os
import requests
from dotenv import load_dotenv

load_dotenv()

class EBirdClient:
    def __init__(self, region="US"):
        self.api_key = os.getenv("EBIRD_API_KEY")
        self.region = region

    def get_recent_observations(self):
        return self._make_request(f"data/obs/{self.region}/recent")

    def get_historic_observations(self, year, month, day):
        return self._make_request(f"data/obs/{self.region}/historic/{year}/{month}/{day}")

    def _make_request(self, endpoint):
        url = f"https://api.ebird.org/v2/{endpoint}"
        headers = {"X-eBirdApiToken": self.api_key}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e}")
            return []
        except requests.exceptions.ConnectionError:
            print("Connection error: Check your network")
            return []

    def get_taxonomy(self):
        return self._make_request("ref/taxonomy/ebird?fmt=json")


