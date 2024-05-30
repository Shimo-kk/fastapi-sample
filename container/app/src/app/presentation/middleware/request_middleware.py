from fastapi import Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RequestMiddleware(BaseHTTPMiddleware):
    """
    HTTPリクエストを処理するミドルウェア
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
        try:
            response: Response = await call_next(request)
            return response

        except HTTPException as e:
            detail = {
                "detail": e.detail,
            }
            return JSONResponse(detail, status_code=e.status_code)
        except Exception as e:
            detail = {
                "detail": str(e),
            }
            return JSONResponse(detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
