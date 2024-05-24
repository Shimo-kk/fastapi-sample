from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from typing import Generator, Callable, NewType
from injector import inject, singleton
from app.application.interface.database.database_handller import IDatabaseHandller
from app.application.interface.database.repository_factory import IRepositoryFactory
from app.infrastructure.database.repository_factory import RepositoryFactory

DatabaseHost = NewType("DatabaseHost", str)
DatabaseUser = NewType("DatabaseUser", str)
DatabasePass = NewType("DatabasePass", str)
DatabaseName = NewType("DatabaseName", str)


@singleton
class DatabaseHandller(IDatabaseHandller):
    """
    データベースハンドラの実装クラス

    Attributes:
        _sessionLocal: セッションローカル
    """

    @inject
    def __init__(
        self,
        host: DatabaseHost,
        user: DatabaseUser,
        password: DatabasePass,
        name: DatabaseName,
    ):
        url = f"postgresql+psycopg2://{user}:{password}@{host}/{name}"
        engine = create_engine(
            url,
            echo=True,
            # pool_size=,
            # max_overflow=
        )
        self._sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def transaction(self, func: Callable[[IRepositoryFactory], None]) -> None:
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
    def get_session(self) -> Generator[Session, None, None]:
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
