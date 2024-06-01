import jwt
from fastapi import Request, Response, HTTPException, status
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


def get_subject_from_cookie(request: Request) -> str:
    # CookieからJWTトークンを取得
    access_token: str = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが設定されていません。")

    scheme, _, token = access_token.partition(" ")
    if scheme != "Bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが設定されていません。")

    # JWTトークンのデコード
    subject = decode_jwt(token)
    if subject is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが不正か、有効期限が切れています。"
        )

    return subject


def set_token_to_cookie(subject: str, response: Response) -> None:
    token: str = encode_jwt(subject=subject)
    response.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True)


def clear_token_to_cookie(response: Response) -> None:
    response.set_cookie(key="access_token", value="", httponly=True, samesite="none", secure=True)
