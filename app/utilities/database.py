from sqlalchemy import create_engine

from app.utilities.constants import KEYS


engine = create_engine(
    "postgresql://"
    f"{KEYS['DATABASE.USERNAME']}:{KEYS['DATABASE.PASSWORD']}"
    "@"
    f"{KEYS['DATABASE.HOST']}:{KEYS['DATABASE.PORT']}"
    "/"
    f"{KEYS['DATABASE.NAME']}"
)
