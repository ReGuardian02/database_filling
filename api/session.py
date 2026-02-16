import os
from urllib.parse import urljoin

import requests


_session = None

def get_session():
    global _session
    if _session is None:
        _session = requests.Session()
        login(_session)
    return _session


def login(session: requests.Session):
    url = urljoin(
        os.getenv("STAND_URL"),
        os.getenv("AUTH_PATH")
    )
    params = {
        "username": os.getenv("STAND_USERNAME"),
        "password": os.getenv("STAND_PASSWORD")
    }

    response = session.get(url, params=params)
    response.raise_for_status()

    if "PHPSESSID" not in session.cookies:
        raise RuntimeError("PHPSESSID не возвращена сервером")
