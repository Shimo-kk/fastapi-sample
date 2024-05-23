from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.presentation.auth import auth_csrf

CSRF_AUTH_EXCLUSION_METHOD = [
    "GET",
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
                detail = {
                    "detail": e.detail,
                }
                return JSONResponse(detail, status_code=status.HTTP_403_FORBIDDEN)

        # 次の処理を実行
        response: Response = await call_next(request)

        return response
