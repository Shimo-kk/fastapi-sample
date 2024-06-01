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

        # JWT認証除外の場合は次の処理へ
        if request.url.path in AWT_AUTH_EXCLUSION_PATH:
            return await call_next(request)

        # JWTトークンからSubjectを取得
        subject: str = auth_jwt.get_subject_from_cookie(request=request)

        # 次の処理を実行
        response: Response = await call_next(request)

        # JWTトークンを更新
        auth_jwt.set_token_to_cookie(subject=subject, response=response)

        return response
