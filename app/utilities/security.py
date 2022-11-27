from jwt import encode
from jwt import decode
from jwt import InvalidTokenError

from core.settings import settings


def create_token(*, user_id: int) -> str:
    payload: dict[str, int] = {
        "user_id": user_id,
    }

    return encode(
        payload=payload,
        key=settings.JWT_ACCESS_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

def decode_token(token: str, /) -> tuple[int | None, str | None]:
    try:
        payload: dict[str, int] = decode(
            jwt=token,
            key=settings.JWT_ACCESS_SECRET_KEY,
            algorithms=[ settings.JWT_ALGORITHM ]
        )
    except InvalidTokenError:
        return (None, "Token is invalid")

    return (payload["user_id"], None)
