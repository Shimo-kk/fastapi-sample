import pytest
import alembic
import alembic.config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from injector import Injector
from app.core.environment import DB_HOST_TEST, DB_USER_TEST, DB_PASS_TEST, DB_NAME_TEST
from app.config.dependency import DependencyModule
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


@pytest.fixture(scope="function")
def injector():
    db_url = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"

    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    alembic.command.upgrade(alembic_cfg, "head")

    injector = Injector([DependencyModule(DB_HOST_TEST, DB_USER_TEST, DB_PASS_TEST, DB_NAME_TEST)])
    yield injector

    # alembic.command.downgrade(alembic_cfg, "base")


@pytest.fixture(scope="function")
def client():
    db_url = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"

    alembic_cfg = alembic.config.Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    alembic.command.upgrade(alembic_cfg, "head")

    client = TestClient(app)
    yield client

    alembic.command.downgrade(alembic_cfg, "base")
