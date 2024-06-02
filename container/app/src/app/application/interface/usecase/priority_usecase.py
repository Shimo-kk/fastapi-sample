from abc import ABC, abstractmethod
from app.application.model.priority_model import PriorityReadModel


class IPriorityUsecase(ABC):
    """
    優先度ユースケースのインタフェース
    """

    @abstractmethod
    def get_all_priority(self) -> list[PriorityReadModel]:
        raise NotImplementedError
