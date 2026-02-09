from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from config import *

def get_engine() -> Engine:
    url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(url, pool_pre_ping=True)
