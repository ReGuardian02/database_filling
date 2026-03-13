from sqlalchemy import select


def generate_mp_land_categories(conn, tables) -> list[dict]:
    rows = []
    catalogs_categories_table = tables["catalogLandCategory"]
    all_catalogs_categories = conn.execute(select(catalogs_categories_table)).mappings().all()

    if not all_catalogs_categories:
        raise Exception("Таблица каталогов 'Категории земель' пустая")

    for catalogs_row in all_catalogs_categories:
        row = {
            "code": catalogs_row["code"],
            "name": catalogs_row["name"],
            "short": catalogs_row["short"]
        }
        rows.append(row)

    return rows
