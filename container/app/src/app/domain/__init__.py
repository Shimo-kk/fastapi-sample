from datetime import datetime


class BaseEntity:
    """
    エンティティクラスのベース

    Attributes:
        id: 主キー
        created_at: 作成日時
        updated_at: 更新日時
    """

    __abstract__ = True

    def __init__(self, id: int = None, created_at: datetime = None, updated_at: datetime = None):
        """
        Args:
            id: 主キー
            created_at: 作成日時
            updated_at: 更新日時
        """
        self._id: int = id
        self._created_at: datetime = created_at
        self._updated_at: datetime = updated_at

    def __eq__(self, o: object) -> bool:
        """
        Args:
            o: オブジェクト
        """
        if isinstance(o, BaseEntity):
            return self.id == o.id

        return False

    @property
    def id(self) -> int:
        return self._id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at
