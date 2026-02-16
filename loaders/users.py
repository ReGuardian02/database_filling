import logging
import random
from sqlalchemy import select

from db.tables import truncate_table


def load_users(conn, tables, rows: list[dict]) -> None:
    units = tables["units"]
    users = tables["users"]

    truncate_table(conn, "users")

    unit_ids = [
        r[0]
        for r in conn.execute(
            select(units.c.id)
        ).fetchall()
    ]

    if not unit_ids:
        raise RuntimeError("units пуст — users некуда привязывать")

    for row in rows:
        row["unit"] = random.choice(unit_ids)

    conn.execute(users.insert().values(rows))
    logging.info(f"Таблица users заполнена тестовыми данными в количестве {len(rows)} шт.")
