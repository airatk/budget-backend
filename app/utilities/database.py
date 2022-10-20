from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from app.utilities.constants import KEYS


engine: Engine = create_engine(
    "postgresql://"
    f"{KEYS['DATABASE.USERNAME']}:{KEYS['DATABASE.PASSWORD']}"
    "@"
    f"{KEYS['DATABASE.HOST']}:{KEYS['DATABASE.PORT']}"
    "/"
    f"{KEYS['DATABASE.NAME']}"
)

LocalSession = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)
