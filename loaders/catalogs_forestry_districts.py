import random
from sqlalchemy import text, select


def load_catalogs_forestry_districts(conn, tables, rows: list[dict]) -> None:
    forestries = tables["catalogs_forestries"]

    forestry_ids = [
        r[0]
        for r in conn.execute(
            select(forestries.c.id)
        ).fetchall()
    ]

    if not forestry_ids:
        raise RuntimeError("catalogs_forestries пуст — districts некуда привязывать")

    for row in rows:
        row["forestry_id"] = random.choice(forestry_ids)

    stmt = text("""
        INSERT INTO catalogs_forestry_districts
            (forestry_id, name, code, code_lv)
        VALUES
            (:forestry_id, :name, :code, :code_lv)
    """)

    conn.execute(stmt, rows)
