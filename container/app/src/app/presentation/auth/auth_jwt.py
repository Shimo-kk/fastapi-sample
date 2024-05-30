import jwt
from datetime import datetime, timedelta, UTC
from app.core.environment import JWT_KEY, JWT_ALGORITHM


def encode_jwt(subject: str) -> str:
    payload = {
        "exp": datetime.now(UTC) + timedelta(days=1, minutes=0),
        "iat": datetime.now(UTC),
        "sub": subject,
    }
    return jwt.encode(payload, JWT_KEY, algorithm=JWT_ALGORITHM)


def decode_jwt(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[JWT_ALGORITHM])
        return payload["sub"]
    except Exception:
        return None
