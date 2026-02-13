import random
from sqlalchemy import text, select, insert

from db.tables import truncate_table


def load_catalogs_forestries(conn, tables, rows: list[dict]) -> None:
    cameras = tables["cameras"]
    land_categories = tables["catalogLandCategory"]
    truncate_table(conn, "catalogs_forestries")

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

    # stmt = text("""
    #     INSERT INTO catalogs_forestries
    #         (name, code, code_lv, code_oiv, polygon, land_category)
    #     VALUES
    #         (:name, :code, :code_lv, :code_oiv,
    #          ST_GeomFromText(:polygon), :land_category)
    # """)
    #
    # conn.execute(stmt, rows)
    conn.execute(insert(cameras).values(rows))
