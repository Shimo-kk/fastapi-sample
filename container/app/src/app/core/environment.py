import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# CORS関連
ALLOW_ORIGINS: list = os.environ["ALLOW_ORIGINS"]
ALLOW_HEADERS: list = os.environ["ALLOW_HEADERS"]

# DB関連
DB_HOST: str = os.environ["DB_HOST"]
DB_USER: str = os.environ["DB_USER"]
DB_PASS: str = os.environ["DB_PASS"]
DB_NAME: str = os.environ["DB_NAME"]
DB_HOST_TEST: str = os.environ["DB_HOST_TEST"]
DB_USER_TEST: str = os.environ["DB_USER_TEST"]
DB_PASS_TEST: str = os.environ["DB_PASS_TEST"]
DB_NAME_TEST: str = os.environ["DB_NAME_TEST"]

# 認証関連
CSRF_KEY: str = os.environ["CSRF_KEY"]
JWT_KEY: str = os.environ["JWT_KEY"]
JWT_ALGORITHM = "HS256"

# デバッグモード
DEBUG: bool = os.environ["DEBUG"]
