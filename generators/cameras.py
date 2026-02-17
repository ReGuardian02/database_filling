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

    for _ in range(count):
        cam_id = ids.pop()
        ip_last = random.randint(0, 255)
        port = random.randint(100, 999)

        encoded_username = quote(fake.user_name(), safe='')
        encoded_password = quote(fake.password(length=10), safe='')

        local_address = f"192.168.201.{ip_last}"

        row = {
            "id": cam_id,
            "name": f"Стенд - {random.choice(['верх', 'низ'])} - {fake.word().capitalize()}",
            "streamName": f"RU.01.{cam_id}",
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
