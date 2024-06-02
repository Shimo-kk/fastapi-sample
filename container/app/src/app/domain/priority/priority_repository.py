from abc import ABC, abstractmethod
from app.domain.priority.priority_entity import PriorityEntity


class IPriorityRepository(ABC):
    """
    優先度のリポジトリインタフェース
    """

    @abstractmethod
    def find_all(self) -> list[PriorityEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> PriorityEntity:
        raise NotImplementedError
