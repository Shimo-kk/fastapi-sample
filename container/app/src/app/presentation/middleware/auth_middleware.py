from fastapi import Request, Response, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from app.presentation.auth import auth_csrf
from app.presentation.auth import auth_jwt

CSRF_AUTH_EXCLUSION_METHOD: list[str] = [
    "GET",
]

AWT_AUTH_EXCLUSION_PATH: list[str] = [
    "/",
    "/favicon.ico",
    "/docs",
    "/openapi.json",
    "/api/csrf",
    "/api/auth/signup",
    "/api/auth/signin",
]


class AuthMiddleware(BaseHTTPMiddleware):
    """
    認証処理を行うミドルウェア
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        ミドルウェアの処理

        Args:
            request (Request): リクエスト情報
            call_next (method): 次の処理

        Returns:
            Response: レスポンス
        """

        # CSRF認証
        if request.method not in CSRF_AUTH_EXCLUSION_METHOD:
            try:
                await auth_csrf.validate_csrf(request)
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="CSRFトークンの認証に失敗しました。: " + str(e)
                )

        # JWT認証除外の場合は次の処置へ
        if request.url.path in AWT_AUTH_EXCLUSION_PATH:
            return await call_next(request)

        # CookieからJWTトークンを取得
        access_token: str = request.cookies.get("access_token")
        if not access_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが設定されていません。")

        scheme, _, token = access_token.partition(" ")
        if scheme != "Bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが設定されていません。")

        # JWTトークンのデコード
        subject = auth_jwt.decode_jwt(token)
        if subject is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="JWTトークンが不正か、有効期限が切れています。"
            )

        # 次の処理を実行
        response: Response = await call_next(request)

        # JWTトークンを更新
        jwt_token = auth_jwt.encode_jwt(subject)
        response.set_cookie(
            key="access_token", value=f"Bearer {jwt_token}", httponly=True, samesite="none", secure=True
        )

        return response
