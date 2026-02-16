from db.tables import add_unique_id
from faker import Faker

fake = Faker("ru_RU")


def generate_owners(count: int) -> list[dict]:
    rows = []

    for _ in range(count):
        row = {
            "name": add_unique_id("Тестовый держатель ресурсов ")
        }

        rows.append(row)

    return rows
