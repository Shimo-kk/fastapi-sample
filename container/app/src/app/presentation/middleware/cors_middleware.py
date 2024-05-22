import os
from starlette.middleware.cors import CORSMiddleware, ALL_METHODS
from starlette.types import ASGIApp


class CORSMiddleware(CORSMiddleware):
    """
    CROSを処理するミドルウェア
    """

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(
            app,
            allow_origins=os.environ["ALLOW_ORIGINS"],
            allow_methods=ALL_METHODS,
            allow_headers=os.environ["ALLOW_HEADERS"],
            allow_credentials=True,
        )
