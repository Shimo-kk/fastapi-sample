from datetime import datetime
from app.domain import BaseEntity


class PriorityEntity(BaseEntity):
    """
    優先度のエンティティクラス

    Attributes:
        name: 名称
    """

    def __init__(
        self,
        id: int = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        name: str = "",
    ):
        """
        Args:
            id: 主キー
            created_at: 作成日時
            updated_at: 更新日時
            name: 名称
        """
        BaseEntity.__init__(self, id, created_at, updated_at)
        self._name: str = name

    def __eq__(self, o: object) -> bool:
        """
        Args:
            o: オブジェクト
        """
        return BaseEntity.__eq__(o)

    @property
    def name(self) -> str:
        return self._name
