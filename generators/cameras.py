import os
import random
from urllib.parse import quote
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("ru_RU")


LAT_MIN, LAT_MAX = 54, 60
LON_MIN, LON_MAX = 30, 40


def random_date(start_days: int, end_days: int) -> str:
    date = datetime.now() + timedelta(days=random.randint(start_days, end_days))
    return date.strftime("%Y-%m-%d")


def generate_cameras(count: int) -> list[dict]:
    rows = []
    ids = random.sample(range(1, 5000), count)
    directions = ['верх', 'низ', 'право', 'лево']

    for _ in range(count):
        cam_id = ids.pop()
        ip_last = random.randint(0, 255)
        port = random.randint(100, 999)
        direction = random.choice(directions)

        encoded_username = quote(fake.user_name(), safe='')
        encoded_password = quote(fake.password(length=10), safe='')

        local_address = f"192.168.201.{ip_last}"

        row = {
            "id": cam_id,
            "name": f"{cam_id} Стенд - {direction} - {fake.word().capitalize()}",
            "streamName": f"RU.{os.getenv("SYSTEM_NUMBER")}.{cam_id}",
            "localAddress": local_address,
            "manageUrl": f"http://{local_address}",
            "rtspPort": port,
            "userName": encoded_username,
            "password": encoded_password,
            "latitude": random.randint(LAT_MIN, LAT_MAX),
            "longitude": random.randint(LON_MIN, LON_MAX),
            "height": random.randint(1, 100),
            "action": "save"
        }

        rows.append(row)

    return rows

def generate_valid_camera() -> dict:
    cam_id = random.randint(5001, 10000)

    encoded_username = quote(os.getenv("CAMERA_USERNAME"), safe='')
    encoded_password = quote(os.getenv("CAMERA_PASSWORD"), safe='')

    row = {
        "id": cam_id,
        "name": "Тестовая валидная камера",
        "streamName": f"RU.{os.getenv("SYSTEM_NUMBER")}.{cam_id}",
        "localAddress": os.getenv("CAMERA_LOCAL_ADDRESS"),
        "manageUrl": f"http://{os.getenv('CAMERA_LOCAL_ADDRESS')}",
        "rtspPort": os.getenv("CAMERA_PORT"),
        "userName": encoded_username,
        "password": encoded_password,
        "latitude": random.randint(LAT_MIN, LAT_MAX),
        "longitude": random.randint(LON_MIN, LON_MAX),
        "height": random.randint(1, 100),
        "action": "save"
    }

    return row