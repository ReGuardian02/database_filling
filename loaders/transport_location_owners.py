import random
from sqlalchemy import select, insert


def load_owners(conn, tables, rows: list[dict]) -> None:
    owners = tables["transport"]
    owner_type_ids = [r[0] for r in conn.execute(select(tables["transport_location_owner_types"].c.id))]

    if not owner_type_ids:
        raise RuntimeError("Нет данных из таблицы transport_location_owner_types")

    for row in rows:
        row["type"] = random.choice(owner_type_ids)

    conn.execute(insert(owners).values(rows))
