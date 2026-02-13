import random
from sqlalchemy import select, insert
from db.tables import truncate_table, safe_insert
import uuid


def load_cameras(conn, tables, rows: list[dict]) -> None:
    cameras = tables["cameras"]
    # truncate_table(conn, "cameras")
    #
    # regions = [r[0] for r in conn.execute(select(tables["regions"].c.id))]
    # models = [r[0] for r in conn.execute(select(tables["camera_models"].c.id))]
    # streams = [r[0] for r in conn.execute(select(tables["stream_servers"].c.id))]
    # units = [r[0] for r in conn.execute(select(tables["units"].c.id))]
    # users = [r[0] for r in conn.execute(select(tables["users"].c.id))]
    #
    # if not all([regions, models, streams, units]):
    #     raise RuntimeError("Недостаточно FK-данных для cameras")
    #
    # for row in rows:
    #     row["region"] = random.choice(regions)
    #     row["model"] = random.choice(models)
    #     row["streamServer"] = random.choice(streams)
    #     row["unit"] = random.choice(units)
    #
    #     if row["locked"] == 1:
    #         row["lockuid"] = random.choice(users)
    #     else:
    #         row["lockuid"] = -1
    #
    #     row["zbxhttpitemid"] = row["zbxicmpitemid"] - 1
    #
    # # conn.execute(insert(cameras).values(rows))
    # safe_insert(conn, cameras, rows)
    # Пример данных для вставки
    row = {
        "id": 999999,  # твой уникальный id
        "uuid": str(uuid.uuid4()),  # обязательно уникальный
        "region": 1,  # обязательное поле
        "model": 1,  # обязательное поле
        "userName": "operator_test",  # обязательное поле
        "password": "test_password",  # обязательное поле
        "latitude": 0.0,  # обязательное поле без дефолта
        "longitude": 0.0,  # обязательное поле без дефолта
        "manageUrl": "http://localhost",  # обязательное поле без дефолта
        "remoteTourServerAddress": "",  # обязательное поле без дефолта
        "remoteTourServer": 0,  # обязательное поле без дефолта
        "orderIndex": 0,  # обязательное поле без дефолта
        "state": 1  # обязательное поле без дефолта
    }

    # Вставка через SQLAlchemy
    conn.execute(cameras.insert().values(row))

