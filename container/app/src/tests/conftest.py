import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from fastapi import FastAPI
from fastapi.testclient import TestClient
from injector import Injector
from app.core.environment import DB_HOST_TEST, DB_USER_TEST, DB_PASS_TEST, DB_NAME_TEST
from app.config.dependency import DependencyModule
from app.presentation.middleware.cors_middleware import CORSMiddleware
from app.presentation.middleware.request_middleware import RequestMiddleware
from app.presentation.middleware.auth_middleware import AuthMiddleware
from app.presentation.router import api_router
from app.infrastructure.database.dto import Base
from seeds.seed import seed_data, seed_data_test

# アプリケーション生成
app = FastAPI()

# ミドルウェアの追加
app.add_middleware(AuthMiddleware)
app.add_middleware(RequestMiddleware)
app.add_middleware(CORSMiddleware)

# ルーターの追加
app.include_router(api_router, prefix="/api")

TEST_DB_URL: str = f"postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}/{DB_NAME_TEST}"


@pytest.fixture(scope="function")
def injector():
    engine = create_engine(TEST_DB_URL)
    alembic_cfg: Config = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    seed_data.seed(url=TEST_DB_URL)
    seed_data_test.seed(url=TEST_DB_URL)

    injector = Injector([DependencyModule(DB_HOST_TEST, DB_USER_TEST, DB_PASS_TEST, DB_NAME_TEST)])
    yield injector

    command.downgrade(alembic_cfg, "base")
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client():
    engine = create_engine(TEST_DB_URL)
    alembic_cfg: Config = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    seed_data.seed(url=TEST_DB_URL)
    seed_data_test.seed(url=TEST_DB_URL)

    client = TestClient(app)
    yield client

    command.downgrade(alembic_cfg, "base")
    Base.metadata.drop_all(bind=engine)
