import random

from seeds import catalogs_forestries_seed
from sqlalchemy import create_engine, MetaData, Table, text, select

# ---- Настройка подключения ----
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/forestguardian_test")
metadata = MetaData()

with engine.begin() as conn:  # автоматически commit/rollback
    # Отражаем существующие таблицы
    metadata.reflect(bind=conn)
    catalogs_forestries_table = Table("catalogs_forestries", metadata, autoload_with=conn)
    catalog_land_category_table = Table("catalogLandCategory", metadata, autoload_with=conn)

    # Получаем все существующие коды land_category
    result = conn.execute(select(catalog_land_category_table.c.code))
    land_category_codes = [row[0] for row in result.fetchall()]

    if not land_category_codes:
        raise RuntimeError("В таблице catalogLandCategory нет записей!")

    # Генерация тестовых записей
    forestries = catalogs_forestries_seed.generate_forestries(15)

    # Присваиваем каждой записи случайный land_category
    for row in forestries:
        row["land_category"] = random.choice(land_category_codes)

    # Вставка с конверсией WKT в GEOMETRY
    stmt = text("""
        INSERT INTO catalogs_forestries (name, code, code_lv, code_oiv, polygon, land_category)
        VALUES (:name, :code, :code_lv, :code_oiv, ST_GeomFromText(:polygon), :land_category)
    """)

    conn.execute(stmt, forestries)
    print("Каталог лесничеств успешно сгенерирован и инициализирован")
