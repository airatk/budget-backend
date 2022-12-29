from typing import Generator

from sqlalchemy.orm import Session

from core.databases.sessions import PostgresSession


def define_postgres_session() -> Generator[Session, None, None]:
    with PostgresSession() as postgres_session:
        yield postgres_session
