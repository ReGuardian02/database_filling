import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("ru_RU")


LAT_MIN, LAT_MAX = 54.0, 60.0
LON_MIN, LON_MAX = 30.0, 40.0


def random_date(start_days: int, end_days: int) -> str:
    date = datetime.now() + timedelta(days=random.randint(start_days, end_days))
    return date.strftime("%Y-%m-%d")


def generate_cameras(count: int) -> list[dict]:
    rows = []
    ids = random.sample(range(1, 5000), count)

    for _ in range(count):
        cam_id = ids.pop()
        ip_last = f"{random.randint(0, 255):03d}"
        port = random.randint(100, 999)

        username = fake.user_name()
        password = fake.password(length=10)

        local_address = f"192.168.201.{ip_last}"

        row = {
            "id": cam_id,
            "uuid": str(uuid.uuid4()),
            "streamName": f"RU.01.{cam_id}",
            "localAddress": local_address,
            "localMask": random.choice(["", "255.255.255.0"]),
            "localGateway": random.choice(["", "192.168.0.1"]),
            "name": f"Стенд - {random.choice(['верх', 'низ'])} - {fake.word().capitalize()}",
            "userName": username,
            "password": password,
            "latitude": round(random.uniform(LAT_MIN, LAT_MAX), 12),
            "longitude": round(random.uniform(LON_MIN, LON_MAX), 12),
            "manageUrl": f"http://{local_address}:{port}",
            "height": random.randint(1, 100),
            "ownerInformation": fake.sentence(),
            "rtspPort": str(port),
            "streamInput": (
                f"rtsp://{username}:{password}@"
                f"{local_address}:{port}/axis-media/media.amp"
            ),
            "infoMountAddress": fake.address(),
            "installationDate": random_date(-120, -90),
            "warrantyPeriod": random_date(30, 365 * 5),
        }

        rows.append(row)

    return rows
