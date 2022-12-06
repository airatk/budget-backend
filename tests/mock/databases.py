from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from models import User

from .settings import test_settings


test_postgres_engine: Engine = create_engine(url=test_settings.POSTGRES_URL)

TestPostgresSession: sessionmaker = sessionmaker(
    bind=test_postgres_engine,
    autocommit=False,
    autoflush=False
)


def fill_up_test_database():
    with TestPostgresSession() as test_postgres_session:
        test_user: User = User(  # noqa: S106
            username="test-user",
            password="test-password"
        )

        test_postgres_session.add_all([
            test_user
        ])
        test_postgres_session.commit()
