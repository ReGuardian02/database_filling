import logging
import random
from sqlalchemy import select, insert, func

from db.tables import truncate_table


def load_catalogs_forestries(conn, tables, rows: list[dict]) -> None:
    forestries = tables["catalogs_forestries"]
    land_categories = tables["catalogLandCategory"]

    truncate_table(conn, "catalogs_forestries")

    land_codes = [
        r[0]
        for r in conn.execute(
            select(land_categories.c.code)
        ).fetchall()
    ]

    if not land_codes:
        raise RuntimeError("catalogLandCategory пуст")

    for row in rows:
        row["land_category"] = random.choice(land_codes)
        row["polygon"] = func.ST_GeomFromText(row["polygon"])

    conn.execute(insert(forestries).values(rows))
    logging.info(f"Таблица catalogs_forestries заполнена тестовыми данными в количестве {len(rows)} шт.")
