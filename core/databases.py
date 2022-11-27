from sqlalchemy.engine import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings


postgres_engine: Engine = create_engine(url=settings.POSTGRES_URL)

PostgresSession: sessionmaker = sessionmaker(
    bind=postgres_engine,
    autocommit=False,
    autoflush=False
)
