from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from contextlib import contextmanager
from typing import Generator, NewType
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
        self._session_local: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @contextmanager
    def begin_transaction(self) -> Generator[IRepositoryFactory, None, None]:
        """
        トランザクション開始

        Returns:
            Generator[IRepositoryFactory, None, None]: リポジトリファクトリ
        """
        session: Session = self._session_local()
        repositoryFactory: IRepositoryFactory = RepositoryFactory(session)
        try:
            yield repositoryFactory
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
