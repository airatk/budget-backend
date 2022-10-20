from app.utilities.database import LocalSession


def define_local_session():
    with LocalSession() as local_session:
        yield local_session
