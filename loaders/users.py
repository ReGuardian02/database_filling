import random
from sqlalchemy import text, select


def load_users(conn, tables, rows: list[dict]) -> None:
    units = tables["units"]

    conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
    conn.execute(text("TRUNCATE TABLE users"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

    unit_ids = [
        r[0]
        for r in conn.execute(
            select(units.c.id)
        ).fetchall()
    ]

    if not unit_ids:
        raise RuntimeError("units пуст — users некуда привязывать")

    for row in rows:
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

    conn.execute(stmt, rows)
