from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from typing import Generator, Callable

from app.application.interface.database.database_handller import IDatabaseHandller
from app.application.interface.database.repository_factory import IRepositoryFactory
from app.infrastructure.database.repository_factory import RepositoryFactory


class DatabaseHandller(IDatabaseHandller):
    """
    データベースハンドラの実装クラス

    Attributes:
        _sessionLocal: セッションローカル
    """

    def __init__(self, host: str, user: str, password: str, name: str):
        url = f"postgresql+psycopg2://{user}:{password}@{host}/{name}"
        engine = create_engine(
            url,
            echo=True,
            encoding="utf-8",
            # pool_size=,
            # max_overflow=
        )
        self._sessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )

    def transaction(self, func: Callable[[IRepositoryFactory]]) -> None:
        """
        トランザクション

        Args:
            func: トランザクション内で実行する関数
        """
        try:
            with self.get_session() as session:
                func(RepositoryFactory(session))
        except Exception:
            raise

    @contextmanager
    def get_session(self) -> Generator[Session]:
        """
        セッション取得

        Returns:
            Generator[Session]: セッション
        """
        session = self._sessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
