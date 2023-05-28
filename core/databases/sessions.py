from sqlalchemy.engine import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session

from core.settings import settings


postgres_engine: Engine = create_engine(url=settings.POSTGRES_URL)  # type: ignore [arg-type]

PostgresSession: sessionmaker[Session] = sessionmaker(
    bind=postgres_engine,
    autocommit=False,
    autoflush=False,
)
