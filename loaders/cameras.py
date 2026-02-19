import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import select
from api import cameras
from db.tables import truncate_table
from config import MAX_WORKERS


def clear_cameras():
    logging.info("Запуск очистки камер...")
    all_cameras = cameras.get_all_cameras()
    cids = [camera["cid"] for camera in all_cameras]

    if not all_cameras:
        logging.info("Список камер пуст")
        return

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(cameras.delete_camera, cid) for cid in cids]

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logging.error(f"Ошибка при удалении камеры! {e}")
                raise

    logging.info(f"Очистка всех камер завершена")

def load_cameras(conn, tables, rows: list[dict]) -> None:
    logging.info("Запуск заполнения таблицы камер...")
    clear_cameras()
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

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(cameras.create_camera, row) for row in rows]

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logging.error(f"Ошибка при создании камеры: {e}")
                raise

    logging.info(f"Таблица cameras заполнена тестовыми данными в количестве {len(results)} шт.")