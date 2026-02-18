import logging
import os
from urllib.parse import urljoin

import requests
from requests import Session


CAMERAS_URL = urljoin(os.getenv("STAND_URL"), os.getenv("CAMERA_PATH"))
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def get_all_cameras() -> list[dict]:
    params = {"action": "list", "accessToken": ACCESS_TOKEN}
    response = requests.get(url=CAMERAS_URL, params=params)

    logging.info(f"Get list response: status {response.status_code}, body {response.text}")

    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "result" in data:
        return data["result"]

    raise ValueError(f"Unexpected response format: {data}")

def create_camera(camera_data: dict) -> dict:
    params = {"accessToken": ACCESS_TOKEN}
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}

    logging.info(f"Camera data {camera_data}")
    response = requests.post(url=CAMERAS_URL, headers=headers, data=camera_data, params=params)

    logging.info(f"Create response: status {response.status_code}, body {response.text}")
    response.raise_for_status()
    if "error" in response.json().keys():
        raise ValueError(f"Ошибка при создании камеры: {response.json()['error']}")

    return response.json()

def delete_camera(camera_id: int):
    params = {"action": "delete", "cid": camera_id, "accessToken": ACCESS_TOKEN}
    response = requests.get(url=CAMERAS_URL, params=params)

    logging.info(f"Delete response: status {response.status_code}, body {response.text}")

    response.raise_for_status()

    return response.json()