from abc import ABC, abstractmethod
from app.domain.category.category_entity import CategoryEntity


class ICategoryRepository(ABC):
    """
    カテゴリのリポジトリインターフェース
    """

    @abstractmethod
    def insert(self, entity: CategoryEntity) -> CategoryEntity:
        raise NotImplementedError

    @abstractmethod
    def find_all(self, user_id: int) -> list[CategoryEntity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> CategoryEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: CategoryEntity) -> CategoryEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        raise NotImplementedError
