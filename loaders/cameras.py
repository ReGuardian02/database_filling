import logging
import random
from requests import Session
from sqlalchemy import select
from api import cameras
from db.tables import truncate_table


def clear_cameras(session: Session):
    logging.info("Запуск очистки камер...")
    all_cameras = cameras.get_all_cameras(session)

    if not all_cameras:
        logging.info("Список камер пуст")
        return

    for camera in all_cameras:
        logging.info(f"Current camera: {camera}")
        delete_response = cameras.delete_camera(session, camera['cid'])
        assert not delete_response, f"Ошибка при удалении камеры: {delete_response}"

    logging.info("Очистка всех камер завершена")

def load_cameras(conn, tables, session: Session, rows: list[dict]) -> None:
    logging.info("Запуск заполнения таблицы камер...")
    clear_cameras(session)
    truncate_table(conn, "camstat")

    regions = [r[0] for r in conn.execute(select(tables["regions"].c.id))]
    models = [r[0] for r in conn.execute(select(tables["camera_models"].c.id))]
    streams = [r[0] for r in conn.execute(select(tables["stream_servers"].c.id))]
    if not all([regions, models, streams]):
        raise RuntimeError("Недостаточно FK-данных для cameras")

    for row in rows:
        row["region"] = random.choice(regions)
        row["model"] = random.choice(models)
        row["streamServer"] = random.choice(streams)

        logging.info(f"Данные камеры для создания: {row}")
        cameras.create_camera(session, row)

    logging.info(f"Таблица cameras заполнена тестовыми данными в количестве {len(rows)} шт.")
