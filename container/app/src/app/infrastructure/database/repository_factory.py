from sqlalchemy.orm.session import Session
from typing import Type, TypeVar
from app.application.interface.database.repository_factory import IRepositoryFactory
from app.infrastructure.database.repository.user_repository import UserRepository  # NOQA
from app.infrastructure.database.repository.category_repository import CategoryReoisitory  # NOQA
from app.infrastructure.database.repository.priority_repository import PriorityRepository  # NOQA

T = TypeVar("T")


class RepositoryFactory(IRepositoryFactory):
    """
    リポジトリファクトリの実装クラス

    Attributes:
        db_session: DBセッション
    """

    def __init__(self, session: Session):
        self._db_session: Session = session

    def get_repository(self, interface_cls: Type[T]) -> T:
        implementation_cls = interface_cls.__subclasses__()[0]
        return implementation_cls(self._db_session)
