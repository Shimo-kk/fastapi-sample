from abc import ABC, abstractmethod
from app.application.model.task_model import TaskCreateModel, TaskReadModel, TaskUpdateModel


class ITaskUsecase(ABC):
    """
    タスクユースケースのインタフェース
    """

    @abstractmethod
    def create_task(self, user_email: str, data: TaskCreateModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_task(self, user_email: str) -> list[TaskReadModel]:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, data: TaskUpdateModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def done_task(self, id: int) -> None:
        raise NotImplementedError
