import random
from seeds import catalogs_forestries_seed, catalogs_forestry_districts_seed, users_seed
from sqlalchemy import create_engine, MetaData, Table, text, select


# ---- Настройка подключения ----
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/forestguardian_test")
metadata = MetaData()

with engine.begin() as conn:  # автоматически commit/rollback
    # Отражаем существующие таблицы
    metadata.reflect(bind=conn)
    catalogs_forestries_table = Table("catalogs_forestries", metadata, autoload_with=conn)
    catalog_land_category_table = Table("catalogLandCategory", metadata, autoload_with=conn)
    catalogs_forestrty_districts_table = Table("catalogs_forestry_districts", metadata, autoload_with=conn)
    users_table = Table("users", metadata, autoload_with=conn)

    # ==== ЗАПОЛНЕНИЕ catalogs_forestrty_districts ====
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

    # ==== ЗАПОЛНЕНИЕ catalogs_forestrty_districts ====
    # ---- Получаем все forestry_id ----
    result = conn.execute(select(catalogs_forestries_table.c.id))
    forestry_ids = [row[0] for row in result.fetchall()]

    if not forestry_ids:
        raise RuntimeError("catalogs_forestries пуст — некуда привязывать districts")

    # ---- Генерируем участковые лесничества ----
    districts = catalogs_forestry_districts_seed.generate_forestry_districts(50)

    # ---- Рандомно назначаем forestry_id ----
    for row in districts:
        row["forestry_id"] = random.choice(forestry_ids)

    # ---- Вставка ----
    stmt = text("""
            INSERT INTO catalogs_forestry_districts
                (forestry_id, name, code, code_lv)
            VALUES
                (:forestry_id, :name, :code, :code_lv)
        """)

    conn.execute(stmt, districts)

    print("Каталог участковых лесничеств успешно инициализирован")

    # ==== ЗАПОЛНЕНИЕ users ====
    users = users_seed.generate_users(5)

    stmt = text("""
        INSERT INTO users (
            unit, name, password, outputName, permissions, language,
            blocked, towers, params, layoutColumns, layoutRows,
            email, position, mobile_number, station_number,
            close_session, sip_login, sip_password, sip_server,
            extent, allowPrivateMessages
        )
        VALUES (
            :unit, :name, :password, :outputName, :permissions, :language,
            :blocked, :towers, :params, :layoutColumns, :layoutRows,
            :email, :position, :mobile_number, :station_number,
            :close_session, :sip_login, :sip_password, :sip_server,
            :extent, :allowPrivateMessages
        )
    """)

    conn.execute(stmt, users)

    print("Таблица users успешно инициализирована")