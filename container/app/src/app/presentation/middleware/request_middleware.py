from fastapi import Request, Response, status, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from http import HTTPStatus
from uuid import uuid4
from app.core import logger


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

        # リクエストIDを生成
        request_id: str = str(uuid4())

        # リクエストログ
        logger.request_log(
            request_id=request_id,
            lavel="Request",
            protocol="HTTP/" + request.scope["http_version"],
            host=request.client.host,
            url=request.url.path,
            method=request.method,
        )

        # リクエストを処理
        try:
            response: Response = await call_next(request)

        except HTTPException as e:
            detail = {
                "detail": e.detail,
            }

            response: Response = JSONResponse(detail, status_code=e.status_code)
        except Exception as e:
            # エラーログ
            logger.error_log(
                request_id=request_id,
                lavel=type(e).__name__,
                content=str(e),
            )

            detail = {
                "detail": str(e),
            }
            response: Response = JSONResponse(detail, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # レスポンスログ
        logger.response_log(
            request_id=request_id,
            lavel="Response",
            status=f"{response.status_code} {HTTPStatus(response.status_code).phrase}",
        )

        return response
