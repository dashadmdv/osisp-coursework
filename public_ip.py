from requests import get
from geopy.geocoders import Nominatim


def public_ip() -> str:
    try:
        return get('https://api.ipify.org/').text
    except Exception:
        return '127.0.0.1'


def geo_ip(ip) -> (list, bool):
    try:
        req = get(url=f'http://ip-api.com/json/{ip}').json()
        return [req['lat'], req['lon']]
    except Exception:
        return


def get_city(coords: list) -> (list):
    try:
        return Nominatim(user_agent="GetLoc").reverse(coords).address
    except Exception:
        return "Не удалось получить местоположение!"


if __name__ == "__main__":
    ip = public_ip()
    print(ip)
    coordinates = geo_ip(ip)
    print(coordinates)
    print(get_city(coordinates))