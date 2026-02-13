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

def safe_insert(conn, table: Table, rows: list[dict]):
    if not rows:
        return

    mapper = inspect(table)
    table_columns = set(c.name for c in mapper.columns)
    auto_inc_keys = {c.name for c in mapper.columns if c.primary_key and c.autoincrement}

    filtered_rows = [
        {k: v for k, v in row.items() if k in table_columns and k not in auto_inc_keys}
        for row in rows
    ]

    stmt = insert(table)
    conn.execute(stmt.values(filtered_rows))
