import requests
from constants import WOLT_URL


def check_if_restaurant_is_open(restaurant_id: str, lat: float, lon: float) -> bool:
    wolt_url = (
        WOLT_URL.replace("<RESTAURANT_ID>", restaurant_id)
        .replace("<LATITUDE>", str(lat))
        .replace("<LONGITUDE>", str(lon))
    )
    try:
        response = requests.get(wolt_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()
        return data["venue"]["open_status"]["is_open"]

    except requests.exceptions.RequestException:
        return False
