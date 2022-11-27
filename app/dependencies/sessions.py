from core.databases import PostgresSession


def define_postgres_session():
    with PostgresSession() as postgres_session:
        yield postgres_session
