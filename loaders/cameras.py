import logging
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlalchemy import select

import generators.cameras
from api import cameras
from db.tables import truncate_table


def clear_cameras():
    logging.info("Запуск очистки камер...")
    all_cameras = cameras.get_all_cameras()
    cids = [camera["cid"] for camera in all_cameras]

    if not all_cameras:
        logging.info("Список камер пуст")
        return

    results = []
    workers = min(5, len(cids))
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(cameras.delete_camera, cid) for cid in cids]

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logging.error(f"Ошибка при удалении камеры! {e}")
                raise

    logging.info("Очистка всех камер завершена")

def load_cameras(conn, tables, rows: list[dict]) -> None:
    logging.info("Запуск заполнения таблицы камер...")
    clear_cameras()
    valid_camera_data = generators.cameras.generate_valid_camera()
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
    workers = min(5, len(rows))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(cameras.create_camera, row) for row in rows]

        for future in as_completed(futures):
            try:
                results.append(future.result())
            except Exception as e:
                logging.error(f"Ошибка при создании камеры: {e}")
                raise

    logging.info(f"Таблица cameras заполнена тестовыми данными в количестве {len(results)} шт.")

    valid_camera_data["region"] = random.choice(regions)
    valid_camera_data["model"] = random.choice(models)
    valid_camera_data["streamServer"] = random.choice(streams)

    response = cameras.create_camera(valid_camera_data)
    if "error" in response.keys():
        raise ValueError(f"Ошибка при создании камеры: {response['error']}")

    logging.info(f"В таблицу cameras добавлена валидная камера")