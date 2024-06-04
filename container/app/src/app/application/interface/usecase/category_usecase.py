from abc import ABC, abstractmethod
from app.application.model.category_model import CategoryCreateModel, CategoryReadModel, CategoryUpdateModel


class ICategoryUsecase(ABC):
    """
    カテゴリユースケースのインタフェース
    """

    @abstractmethod
    def create_category(self, user_email: str, data: CategoryCreateModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all_category(self, user_email: str) -> list[CategoryReadModel]:
        raise NotImplementedError

    @abstractmethod
    def update_category(self, data: CategoryUpdateModel) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_category(self, id: int) -> None:
        raise NotImplementedError
