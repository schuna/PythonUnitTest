import requests


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None


def protocol():
    while True:
        response = requests.get('http://localhost/api/holidays')
        if response == "completed":
            return response
