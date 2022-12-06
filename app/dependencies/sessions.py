from typing import Generator

from core.databases import PostgresSession


def define_postgres_session() -> Generator[PostgresSession, None, None]:
    with PostgresSession() as postgres_session:
        yield postgres_session
