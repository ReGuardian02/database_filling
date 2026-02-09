import random
from sqlalchemy import text, select


def load_catalogs_forestries(conn, tables, rows: list[dict]) -> None:
    land_categories = tables["catalogLandCategory"]

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE catalogs_forestries"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    land_codes = [
        r[0]
        for r in conn.execute(
            select(land_categories.c.code)
        ).fetchall()
    ]

    if not land_codes:
        raise RuntimeError("catalogLandCategory пуст")

    for row in rows:
        row["land_category"] = random.choice(land_codes)

    stmt = text("""
        INSERT INTO catalogs_forestries
            (name, code, code_lv, code_oiv, polygon, land_category)
        VALUES
            (:name, :code, :code_lv, :code_oiv,
             ST_GeomFromText(:polygon), :land_category)
    """)

    conn.execute(stmt, rows)
