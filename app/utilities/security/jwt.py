from datetime import datetime, timedelta

from jwt import InvalidTokenError, decode, encode

from core.settings import settings


def create_access_token(*, user_id: int) -> str:
    payload: dict[str, int | datetime] = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=10),
    }

    return encode(
        payload=payload,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

def decode_access_token(token: str) -> tuple[int, str]:
    try:
        payload: dict[str, int] = decode(
            jwt=token,
            key=settings.JWT_ACCESS_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM,
            ],
        )
    except InvalidTokenError:
        return (0, "Token is invalid")

    return (payload["sub"], "")
