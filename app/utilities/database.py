from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

from app.utilities.constants import KEYS


database_connection_url: URL = URL.create(
    drivername=KEYS['DATABASE.DRIVER'],
    username=KEYS['DATABASE.USERNAME'],
    password=KEYS['DATABASE.PASSWORD'],
    host=KEYS['DATABASE.HOST'],
    port=KEYS['DATABASE.PORT'],
    database=KEYS['DATABASE.NAME']
)

engine: Engine = create_engine(url=database_connection_url)

LocalSession: sessionmaker = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
