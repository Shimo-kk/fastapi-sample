from fastapi import FastAPI
from app.presentation.middleware.cors_middleware import CORSMiddleware
from app.presentation.middleware.request_middleware import RequestMiddleware
from app.presentation.middleware.auth_middleware import AuthMiddleware
from app.presentation.router import api_router

# アプリケーション生成
app = FastAPI()

# ミドルウェアの追加
app.add_middleware(AuthMiddleware)
app.add_middleware(RequestMiddleware)
app.add_middleware(CORSMiddleware)

# ルーターの追加
app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello world"}
