import logging
import os
from urllib.parse import urljoin
from requests import Session


CAMERAS_URL = urljoin(os.getenv("STAND_URL"), os.getenv("CAMERA_PATH"))

def get_all_cameras(session: Session) -> list[dict]:
    params = {"action": "list"}
    response = session.get(url=CAMERAS_URL, params=params)

    logging.info(f"Get list response: status {response.status_code}, body {response.text}")

    response.raise_for_status()
    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "result" in data:
        return data["result"]

    raise ValueError(f"Unexpected response format: {data}")

def create_camera(session: Session, camera_data: dict) -> dict:
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    response = session.post(url=CAMERAS_URL, headers=headers, data=camera_data)

    logging.info(f"Create response: status {response.status_code}, body {response.text}")
    response.raise_for_status()
    if "error" in response.json().keys():
        raise ValueError(f"Ошибка при создании камеры: {response.json()['error']}")

    return response.json()

def delete_camera(session: Session, camera_id: int):
    params = {"action": "delete", "cid": camera_id}
    response = session.get(url=CAMERAS_URL, params=params)

    logging.info(f"Delete response: status {response.status_code}, body {response.text}")

    response.raise_for_status()

    return response.json()