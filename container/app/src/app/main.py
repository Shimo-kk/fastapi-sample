from dotenv import load_dotenv
from fastapi import FastAPI

# 環境変数の読み込み
load_dotenv()

# アプリケーション生成
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello world"}
