from datetime import datetime
from app.core.exceptions import ValidationError
from app.domain import BaseEntity
from app.domain.category.category_validator import CategoryValidator


class CategoryEntity(BaseEntity):
    """
    カテゴリのエンティティクラス

    Attributes:
        user_id: ユーザーID
        name: 名称
    """

    @staticmethod
    def create(user_id: int, name: str) -> "CategoryEntity":
        """
        エンティティの作成

        Args:
            user_id: ユーザーID
            name: 名称
        """

        # カテゴリ名のバリデーション
        valid_message: str = CategoryValidator.validate_name(value=name)
        if valid_message:
            raise ValidationError(valid_message)

        return CategoryEntity(user_id=user_id, name=name)

    def __init__(
        self,
        id: int = None,
        created_at: datetime = None,
        updated_at: datetime = None,
        user_id: int = 0,
        name: str = "",
    ):
        """
        Args:
            id: 主キー
            created_at: 作成日時
            updated_at: 更新日時
            user_id: ユーザーID
            name: 名称
        """
        BaseEntity.__init__(self, id, created_at, updated_at)
        self._user_id: int = user_id
        self._name: str = name

    def __eq__(self, o: object) -> bool:
        """
        Args:
            o: オブジェクト
        """
        return BaseEntity.__eq__(o)

    def change_name(self, name: str):
        """
        カテゴリ名の変更

        Args:
            name: カテゴリ名
        """

        # カテゴリ名のバリデーション
        valid_message: str = CategoryValidator.validate_name(value=name)
        if valid_message:
            raise ValidationError(valid_message)

        self._name = name

    @property
    def user_id(self) -> int:
        return self._user_id

    @property
    def name(self) -> str:
        return self._name
