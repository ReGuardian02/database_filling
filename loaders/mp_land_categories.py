import logging


def load_mp_land_categories(conn, tables, rows):
    mp_land_categories_table = tables["mp_land_categories"]

    conn.execute(mp_land_categories_table.insert().values(rows))
    logging.info(f"Таблица catalogs_forestry_districts заполнена тестовыми данными в количестве {len(rows)} шт.")