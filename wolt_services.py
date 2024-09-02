import requests
from constants import WOLT_URL
from wolt_exception import WoltException


def is_restaurant_open(restaurant_id: str, lat: float, lon: float) -> bool:
    wolt_url = WOLT_URL.format(restaurant_id=restaurant_id, lat=lat, lon=lon)

    try:
        response = requests.get(wolt_url)
        response.raise_for_status()

        data = response.json()
        return data["venue"]["open_status"]["is_open"]

    except requests.exceptions.RequestException:
        raise WoltException("Failed to connect to Wolt API")
