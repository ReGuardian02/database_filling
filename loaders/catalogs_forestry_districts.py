import logging
import random
from sqlalchemy import select

from db.tables import truncate_table


def load_catalogs_forestry_districts(conn, tables, rows: list[dict]) -> None:
    forestries = tables["catalogs_forestries"]
    districts = tables["catalogs_forestry_districts"]

    truncate_table(conn, "catalogs_forestry_districts")

    forestry_ids = [
        r[0]
        for r in conn.execute(
            select(forestries.c.id)
        ).fetchall()
    ]

    if not forestry_ids:
        raise RuntimeError("catalogs_forestries пуст — districts некуда привязывать")

    for row in rows:
        row["forestry_id"] = random.choice(forestry_ids)

    conn.execute(districts.insert().values(rows))
    logging.info(f"Таблица catalogs_forestry_districts заполнена тестовыми данными в количестве {len(rows)} шт.")
