from abc import ABC, abstractmethod
from app.domain.task.task_entity import TaskEntity


class ITaskRepository(ABC):
    """
    タスクのリポジトリインタフェース
    """

    @abstractmethod
    def insert(self, entity: TaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, user_id: int) -> list[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: TaskEntity) -> TaskEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        raise NotImplementedError
