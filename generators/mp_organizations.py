import random
from db.tables import add_unique_id
from faker import Faker


fake = Faker("ru_RU")

def generate_parent_mp_organizations(count: int) -> list[dict]:
    rows = []
    roles = [
        "emercom",
        "support",
        "forest_guard",
        "management"
    ]

    for _ in range(count):
        unique_id = add_unique_id("")
        row = {
            "name": f"Тестовая организация {unique_id}",
            "address": fake.address(),
            "roles": [random.choice(roles)],
            "short": f"ТО {unique_id}",
            "lon": round(random.uniform(30.0, 40.0), 4),
            "lat": round(random.uniform(54.0, 60.0), 4),
        }
        rows.append(row)

    return rows

def generate_child_mp_organizations(count: int, parent_ids: tuple[int]) -> list[dict]:
    rows = generate_parent_mp_organizations(count)
    for row in rows:
        row["parent_id"] = random.choice(parent_ids)

    return rows