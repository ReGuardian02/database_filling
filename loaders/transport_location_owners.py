import logging
import random
from sqlalchemy import select, insert

from db.tables import truncate_table


def load_owners(conn, tables, rows: list[dict]) -> None:
    owners = tables["transport_location_owner"]
    owner_types = tables["transport_location_owner_type"]

    truncate_table(conn, "transport_location_owner")
    owner_type_ids = [
        r[0]
        for r in conn.execute(
            select(owner_types.c.id)
        ).fetchall()
    ]

    if not owner_type_ids:
        raise RuntimeError("Нет данных из таблицы transport_location_owner_types")

    for row in rows:
        row["type"] = random.choice(owner_type_ids)

    conn.execute(insert(owners).values(rows))
    logging.info(f"Таблица transport_location_owners заполнена тестовыми данными в количестве {len(rows)} шт.")
