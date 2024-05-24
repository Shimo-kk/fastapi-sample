from abc import ABC, abstractmethod
from typing import Type, TypeVar

T = TypeVar("T")


class IRepositoryFactory(ABC):
    """
    リポジトリファクトリのインタフェース
    """

    @abstractmethod
    def get_repository(self, interface_cls: Type[T]) -> T:
        raise NotImplementedError
