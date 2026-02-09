from sqlalchemy import MetaData, Table

def reflect_tables(conn) -> dict[str, Table]:
    metadata = MetaData()
    metadata.reflect(bind=conn)

    return {table.name: table for table in metadata.tables.values()}
