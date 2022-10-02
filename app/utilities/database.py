from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.utilities.constants import KEYS


engine: Engine = create_engine(
    "postgresql://"
    f"{KEYS['DATABASE.USERNAME']}:{KEYS['DATABASE.PASSWORD']}"
    "@"
    f"{KEYS['DATABASE.HOST']}:{KEYS['DATABASE.PORT']}"
    "/"
    f"{KEYS['DATABASE.NAME']}"
)
