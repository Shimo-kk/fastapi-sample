from abc import ABC, abstractmethod
from typing import Callable

from app.application.interface.database.repository_factory import IRepositoryFactory


class IDatabaseHandller(ABC):
    """
    データベースハンドラのインタフェース
    """

    @abstractmethod
    def transaction(func: Callable[[IRepositoryFactory]]) -> None:
        raise NotImplementedError
