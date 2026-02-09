import random
from sqlalchemy import text, select, insert


def load_cameras(conn, tables, rows: list[dict]) -> None:
    cameras = tables["cameras"]

    regions = [r[0] for r in conn.execute(select(tables["regions"].c.id))]
    models = [r[0] for r in conn.execute(select(tables["camera_models"].c.id))]
    streams = [r[0] for r in conn.execute(select(tables["stream_servers"].c.id))]
    units = [r[0] for r in conn.execute(select(tables["units"].c.id))]
    users = [r[0] for r in conn.execute(select(tables["users"].c.id))]

    if not all([regions, models, streams, units]):
        raise RuntimeError("Недостаточно FK-данных для cameras")

    for row in rows:
        row["region"] = random.choice(regions)
        row["model"] = random.choice(models)
        row["streamServer"] = random.choice(streams)
        row["unit"] = random.choice(units)

        if row["locked"] == 1:
            row["lockuid"] = random.choice(users)
        else:
            row["lockuid"] = -1

        row["zbxhttpitemid"] = row["zbxicmpitemid"] - 1

    conn.execute(insert(cameras).values(rows))
