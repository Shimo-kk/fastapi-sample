from abc import ABC, abstractmethod
from typing import Generator
from contextlib import contextmanager
from app.application.interface.database.repository_factory import IRepositoryFactory


class IDatabaseHandller(ABC):
    """
    データベースハンドラのインタフェース
    """

    @abstractmethod
    @contextmanager
    def begin_transaction(self) -> Generator[IRepositoryFactory, None, None]:
        raise NotImplementedError
