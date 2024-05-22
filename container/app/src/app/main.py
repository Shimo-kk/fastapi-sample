from dotenv import load_dotenv
from fastapi import FastAPI

from app.presentation.middleware.cors_middleware import CORSMiddleware

# 環境変数の読み込み
load_dotenv()

# アプリケーション生成
app = FastAPI()

# ミドルウェアの追加
app.add_middleware(CORSMiddleware)


@app.get("/")
async def root():
    return {"message": "Hello world"}
