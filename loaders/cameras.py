import logging
import os
import random
from urllib.parse import urljoin

from requests import Session
from sqlalchemy import select, insert, text
from db.tables import truncate_table


def load_cameras(conn, tables, session: Session, rows: list[dict]) -> None:
    truncate_table(conn, "cameras")
    headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
    regions = [r[0] for r in conn.execute(select(tables["regions"].c.id))]
    models = [r[0] for r in conn.execute(select(tables["camera_models"].c.id))]
    streams = [r[0] for r in conn.execute(select(tables["stream_servers"].c.id))]
    units = [r[0] for r in conn.execute(select(tables["units"].c.id))]

    if not all([regions, models, streams, units]):
        raise RuntimeError("Недостаточно FK-данных для cameras")

    for row in rows:
        row["region"] = random.choice(regions)
        row["model"] = random.choice(models)
        row["streamServer"] = random.choice(streams)
        row["unit"] = random.choice(units)

        response = session.post(url=urljoin(os.getenv("STAND_URL"), os.getenv("CAMERA_PATH")), headers=headers, data=row)
        response.raise_for_status()

    logging.info(f"Таблица cameras заполнена тестовыми данными в количестве {len(rows)} шт.")
