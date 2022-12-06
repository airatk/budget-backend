from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from models import User

from .databases import TestPostgresSession


def define_test_postgres_session() -> Generator[TestPostgresSession, None, None]:
    with TestPostgresSession() as test_postgres_session:
        yield test_postgres_session


def identify_test_user(session: Session = Depends(define_test_postgres_session)):
    return session.query(User).\
        filter(User.username == "test-user").\
        one_or_none()
