from api.session import get_session
from db.engine import get_engine
from db.tables import reflect_tables

from generators.catalogs_forestries import generate_forestries
from generators.catalogs_forestry_districts import generate_forestry_districts
from generators.users import generate_users
from generators.cameras import generate_cameras
from generators.transport_location_owners import generate_owners

from loaders.catalogs_forestries import load_catalogs_forestries
from loaders.catalogs_forestry_districts import load_catalogs_forestry_districts
from loaders.users import load_users
from loaders.cameras import load_cameras
from loaders.transport_location_owners import load_owners


def main():
    engine = get_engine()
    session = get_session()

    with engine.begin() as conn:
        tables = reflect_tables(conn)

        # load_catalogs_forestries(conn, tables, generate_forestries(5))
        # load_catalogs_forestry_districts(conn, tables, generate_forestry_districts(20))
        # load_users(conn, tables, generate_users(5))
        load_cameras(conn, tables, session, generate_cameras(8))
        # load_owners(conn, tables, generate_owners(10))


if __name__ == "__main__":
    main()
