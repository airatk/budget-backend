from typing import Generator

from fastapi import Depends, Header
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.dependencies.sessions import define_postgres_session
from core.databases.models import User

from .databases import TestPostgresSession


def define_test_postgres_session() -> Generator[Session, None, None]:
    with TestPostgresSession() as test_postgres_session:
        yield test_postgres_session


def identify_test_user(
    session: Session = Depends(define_postgres_session),
    test_username: str = Header(default="test-user"),
) -> User:
    return session.scalar(
        select(User).where(User.username == test_username),
    )
