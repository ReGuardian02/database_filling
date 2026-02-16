import logging

from faker import Faker
from sqlalchemy import MetaData, Table, text, inspect, insert


fake = Faker("ru_RU")

def reflect_tables(conn) -> dict[str, Table]:
    metadata = MetaData()
    metadata.reflect(bind=conn)

    return {table.name: table for table in metadata.tables.values()}

def add_unique_id(base_str: str, upper: bool = True, use_dash: bool = True):
    pattern = "^^-^^" if use_dash else "^^^^"
    return fake.hexify(text=f"{base_str}{pattern}", upper=upper)

def truncate_table(conn, table_name: str):
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text(f"TRUNCATE TABLE {table_name}"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    logging.info(f"Таблица {table_name} была сброшена")

def direct_sql_insert(conn, table_name: str, rows: list[dict]):
    """
    Универсальная функция для вставки данных в любую таблицу.

    :param conn: активное SQLAlchemy соединение
    :param table_name: имя таблицы
    :param rows: iterable словарей, где ключи = имена колонок
    """
    rows = list(rows)
    if not rows:
        return  # нечего вставлять

    columns = list(rows[0].keys())
    column_list = ", ".join(f"`{col}`" for col in columns)
    values_list = ", ".join(f":{col}" for col in columns)

    stmt = text(f"""
        INSERT INTO `{table_name}` ({column_list})
        VALUES ({values_list})
    """)

    conn.execute(stmt, rows)