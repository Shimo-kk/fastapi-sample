from abc import ABC, abstractmethod

from app.domain.user.user_entity import UserEntity


class IUserRepository(ABC):
    """
    ユーザーのリポジトリインターフェース
    """

    @abstractmethod
    def insert(self, entity: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def NotExists(self, email: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, id: int) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, id: int) -> None:
        raise NotImplementedError
