import random
import json
import hashlib
from faker import Faker

fake = Faker("ru_RU")

UNIT_IDS = [34, 56, 176, 177, 178, 597]

BASE_PARAMS = {
    "basemap": "osm",
    "lastPage": "",
    "panel": 1,
    "weather": False,
    "layers": [326],
    "sound": True,
    "searchPanel": False,
    "chatAvailable": True,
    "chat": False,
    "userMonitoring": True,
    "userFires": True,
    "userTransport": True,
    "userMapLayers": True,
    "userRightsConfirmed": True,
    "accessToReports": True,
}

POSITIONS = [
    "Диспетчер",
    "Оператор",
    "Старший диспетчер",
    "Инженер",
    "Начальник смены",
    "Специалист",
]

def random_password_hash() -> str:
    raw = fake.password(length=12)
    return hashlib.sha1(raw.encode()).hexdigest()

def random_phone() -> str:
    return f"+7{random.randint(9000000000, 9999999999)}"

def random_params() -> str:
    params = BASE_PARAMS.copy()
    params["panel"] = random.randint(0, 2)
    params["weather"] = random.choice([True, False])
    params["sound"] = random.choice([True, False])
    return json.dumps(params, ensure_ascii=False)

def generate_users(count: int) -> list[dict]:
    rows = []

    for _ in range(count):
        rows.append({
            "unit": random.choice(UNIT_IDS),
            "name": fake.unique.user_name(),
            "password": random_password_hash(),
            "outputName": fake.name(),
            "permissions": random.randint(1, 5),
            "language": "ru",
            "blocked": 1 if random.random() < 0.2 else 0,  # 80/20
            "towers": None,
            "params": random_params(),
            "layoutColumns": 3,
            "layoutRows": 2,
            "email": fake.email(),
            "position": random.choice(POSITIONS),
            "mobile_number": random_phone(),
            "station_number": "",
            "close_session": 0,
            "sip_login": str(random.randint(1000, 2000)),
            "sip_password": fake.password(length=10),
            "sip_server": "1",
            "extent": random.choice(["null", "[]"]),
            "allowPrivateMessages": random.choice([0, 1]),
        })

    return rows