import random
from seeds import catalogs_forestries_seed, catalogs_forestry_districts_seed, users_seed, cameras_seed
from sqlalchemy import create_engine, MetaData, Table, text, select, insert

# ---- Настройка подключения ----
engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/forestguardian_test")
metadata = MetaData()

with engine.begin() as conn:  # автоматически commit/rollback
    # Отражаем существующие таблицы
    metadata.reflect(bind=conn)
    catalogs_forestries_table = Table("catalogs_forestries", metadata, autoload_with=conn)
    catalog_land_category_table = Table("catalogLandCategory", metadata, autoload_with=conn)
    catalogs_forestry_districts_table = Table("catalogs_forestry_districts", metadata, autoload_with=conn)
    users_table = Table("users", metadata, autoload_with=conn)
    units_table = Table("units", metadata, autoload_with=conn)
    cameras_table = Table("cameras", metadata, autoload_with=conn)
    stream_servers_table = Table("stream_servers", metadata, autoload_with=conn)
    regions_table = Table("regions", metadata, autoload_with=conn)
    camera_models_table = Table("camera_models", metadata, autoload_with=conn)

    # =======================================
    # ЗАПОЛНЕНИЕ catalogs_forestries
    # =======================================
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE catalogs_forestries"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    land_cat_result = conn.execute(select(catalog_land_category_table.c.code))
    land_category_codes = [row[0] for row in land_cat_result.fetchall()]

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

    # =======================================
    # ЗАПОЛНЕНИЕ catalogs_forestry_districts
    # =======================================
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE catalogs_forestry_districts"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    forestries_result = conn.execute(select(catalogs_forestries_table.c.id))
    forestry_ids = [row[0] for row in forestries_result.fetchall()]

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
    # ================
    # ЗАПОЛНЕНИЕ users
    # ================
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE users"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    units_result = conn.execute(select(units_table.c.id))
    unit_ids = [row[0] for row in units_result.fetchall()]

    if not unit_ids:
        raise RuntimeError("units пуст — некуда привязывать users.unit")

    users = users_seed.generate_users(5)
    for row in users:
        row["unit"] = random.choice(unit_ids)

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

    # ==========================
    # ЗАПОЛНЕНИЕ ТАБЛИЦЫ CAMERAS
    # ==========================
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE camstat"))
    conn.execute(text("TRUNCATE TABLE cameras"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    region_ids = [r[0] for r in conn.execute(select(regions_table.c.id)).fetchall()]
    model_ids = [r[0] for r in conn.execute(select(camera_models_table.c.id)).fetchall()]
    stream_server_ids = [r[0] for r in conn.execute(select(stream_servers_table.c.id)).fetchall()]
    unit_ids = [r[0] for r in conn.execute(select(units_table.c.id)).fetchall()]
    user_ids = [r[0] for r in conn.execute(select(users_table.c.id)).fetchall()]

    if not all([region_ids, model_ids, stream_server_ids, unit_ids]):
        raise RuntimeError("Недостаточно данных для FK cameras")

    # ---- Генерация сидов ----
    cameras = cameras_seed.generate_cameras(5)

    # ---- Дополнение FK и зависимых полей ----
    for row in cameras:
        row["region"] = random.choice(region_ids)
        row["model"] = random.choice(model_ids)
        row["streamServer"] = random.choice(stream_server_ids)
        row["unit"] = random.choice(unit_ids)

        # lockuid логика
        if row["locked"] == 1:
            row["lockuid"] = random.choice(user_ids)
        else:
            row["lockuid"] = -1

        # zbxhttpitemid = zbxicmpitemid - 1
        row["zbxhttpitemid"] = row["zbxicmpitemid"] - 1

    # ---- Вставка ----
    stmt = insert(cameras_table).values(cameras)
    conn.execute(stmt)
    print("Таблица cameras успешно заполнена")