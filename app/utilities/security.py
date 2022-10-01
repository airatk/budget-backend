from jwt import encode
from jwt import decode
from jwt import InvalidTokenError

from app.utilities.constants import KEYS


def create_token(*, user_id: int) -> str:
    payload: dict[str, int] = {
        "user_id": user_id,
    }

    return encode(
        payload=payload,
        key=KEYS["JWT.ACCESS_SECRET_KEY"],
        algorithm=KEYS["JWT.ALGORITHM"]
    )

def decode_token(token: str, /) -> tuple[int | None, str | None]:
    try:
        payload: dict[str, int] = decode(
            jwt=token,
            key=KEYS["JWT.ACCESS_SECRET_KEY"],
            algorithms=[ KEYS["JWT.ALGORITHM"] ]
        )
    except InvalidTokenError:
        return (None, "Token is invalid")

    return (payload["user_id"], None)
